import sys
import unittest

from peewee import *
from playhouse.sqlite_ext import *
try:
    from playhouse.sqlite_ext import CSqliteExtDatabase as SqliteExtDatabase
    from playhouse.sqlite_ext import register_json_contains
    HAVE_C_EXTENSION = True
except ImportError:
    from playhouse.sqlite_ext import SqliteExtDatabase
    HAVE_C_EXTENSION = False


class Query(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


def _json_contains(src_json, obj_json):
    stack = []
    try:
        stack.append((json.loads(obj_json), json.loads(src_json)))
    except:
        # Invalid JSON!
        return False

    while stack:
        obj, src = stack.pop()
        if isinstance(src, dict):
            if isinstance(obj, dict):
                for key in obj:
                    if key not in src:
                        return False
                    stack.append((obj[key], src[key]))
            elif isinstance(obj, list):
                for item in obj:
                    if item not in src:
                        return False
            elif obj not in src:
                return False
        elif isinstance(src, list):
            if isinstance(obj, dict):
                return False
            elif isinstance(obj, list):
                try:
                    for i in range(len(obj)):
                        stack.append((obj[i], src[i]))
                except IndexError:
                    return False
            elif obj not in src:
                return False
        elif obj != src:
            return False
    return True


class Graph(object):
    def __init__(self, database=None):
        if database is None:
            database = SqliteExtDatabase(':memory:')

        if HAVE_C_EXTENSION:
            register_json_contains(database)
        else:
            database.register_function(_json_contains, 'json_contains')

        self.database = database
        self.V, self.E = self.create_models()

    def create_models(self):
        class Vertex(Model):
            key = TextField(primary_key=True)
            metadata = JSONField()

            class Meta:
                database = self.database

            def connect(self, dest, label, weight=1., **metadata):
                return Edge.create(src=self, dest=dest, label=label,
                                   weight=weight, metadata=metadata)

            def disconnect(self, dest, label=None):
                query = (Edge
                         .delete()
                         .where((Edge.src == self) & (Edge.dest == dest)))
                if label is not None:
                    query = query.where(Edge.label == label)
                return query.execute()

            def _edges(self, query, label=None, **filters):
                if label is not None:
                    query = query.where(Edge.label == label)
                if filters:
                    pass
                return query

            def outE(self, label=None, **filters):
                return self._edges(self.outbound, label, **filters)

            def inE(self, label=None, **filters):
                return self._edges(self.inbound, label, **filters)


        class Edge(Model):
            src = ForeignKeyField(Vertex, backref='outbound')
            dest = ForeignKeyField(Vertex, backref='inbound')
            label = TextField()
            weight = FloatField(default=1.)
            metadata = JSONField()

            class Meta:
                database = self.database
                indexes = (
                    (('src', 'dest', 'label'), True),
                )

            def _vertices(self, query, **filters):
                if filters:
                    pass
                return query

            def outV(self, **filters):
                query = (Vertex
                         .select()
                         .join(Edge, on=(Edge.dest == Vertex.key)))
                return self._vertices(query, **filters)

            def inV(self, **filters):
                query = (Vertex
                         .select()
                         .join(Edge, on=(Edge.src == Vertex.key)))
                return self._vertices(query, **filters)

        return Vertex, Edge

    def create_tables(self):
        self.database.create_tables([self.V, self.E])

    def add_vertex(self, key, **metadata):
        query = (self.V
                 .insert(key=key, metadata=metadata)
                 .on_conflict('replace')
                 .execute())
        return self.V(key=key, metadata=metadata)

    def add_edge(self, src, dest, label, weight=1., **metadata):
        edge_id = (self.E
                   .insert(src=src, dest=dest, label=label, weight=weight,
                           metadata=metadata)
                   .on_conflict('replace')
                   .execute())
        return self.E(id=edge_id, src=src, dest=dest, label=label,
                      weight=weight, metadata=metadata)

    def __getitem__(self, key):
        return self.V.get(self.V.key == key)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.create_tables()

    def tearDown(self):
        self.graph.database.close()

    def test_simple(self):
        self.graph.add_vertex('charlie', kind='person')
        self.graph.add_vertex('huey', kind='cat')
        self.graph.add_vertex('zaizee', kind='cat')
        self.graph.add_vertex('mickey', kind='dog')

        self.graph.add_edge('charlie', 'huey', 'owns')
        self.graph.add_edge('charlie', 'mickey', 'owns')
        self.graph.add_edge('huey', 'zaizee', 'friends')
        self.graph.add_edge('huey', 'mickey', 'friends')
        self.graph.add_edge('zaizee', 'mickey', 'friends')
        self.graph.add_edge('zaizee', 'huey', 'friends')
        self.graph.add_edge('mickey', 'huey', 'friends')
        self.graph.add_edge('mickey', 'zaizee', 'friends')

        charlie = self.graph['charlie']
        self.assertEqual(charlie.metadata, {'kind': 'person'})

        out_edges = [(e.dest_id, e.label) for e in charlie.outE()]
        self.assertEqual(out_edges, [('huey', 'owns'), ('mickey', 'owns')])


if __name__ == '__main__':
    unittest.main(argv=sys.argv)

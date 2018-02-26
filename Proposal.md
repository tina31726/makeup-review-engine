## Overview

Finding top 10 makeup items by using twitter-streaming. 

Makeup is always the hottest topic in fashion world, most of people would like to try the hottest makeup which can make them more fashionable. Therefore, our motivation is help people follow up the hottest makeup on time.

## Data

Data Source: Use data from Tweeter. Search for tag about cosmetic. 

Problem: 

Cosmetic sales data

A. The data size is much more than the one single account access limitation. We need to find the way to switch account automatically.

B. We need to look for actually cosmetic products sales statistic.

## Method

We'll use sentiment analysis on tweets, like using chi-square to find key users and key words. NLTK provided the first trial on all the purpose.

No further plan to modify libraries. 

Here's roughly flowchart: https://goo.gl/13Cikh

## Related Work

[1] Lu, Rong, and Qing Yang. "Trend analysis of news topics on twitter." International Journal of Machine Learning and Computing 2.3 (2012): 327.

https://pdfs.semanticscholar.org/158e/7a6e62d3b8ea277476139274fa06dc6cbb58.pdf

[2] Yamaguchi, Yuto, Toshiyuki Amagasa, and Hiroyuki Kitagawa. "Tag-based user topic discovery using twitter lists." Advances in Social Networks Analysis and Mining (ASONAM), 2011 International Conference on. IEEE, 2011.

http://ieeexplore.ieee.org/abstract/document/5992580/

[3] Cataldi, Mario, Luigi Di Caro, and Claudio Schifanella. "Emerging topic detection on twitter based on temporal and social terms evaluation." Proceedings of the tenth international workshop on multimedia data mining. ACM, 2010.

https://dl.acm.org/citation.cfm?id=1814249

[4] Kim, Hwi-Gang, Seongjoo Lee, and Sunghyon Kyeong. "Discovering hot topics using Twitter streaming data social topic detection and geographic clustering." Advances in Social Networks Analysis and Mining (ASONAM), 2013 IEEE/ACM International Conference on. IEEE, 2013.

http://ieeexplore.ieee.org/abstract/document/6785858/

[5] Huang, Jeff, Katherine M. Thornton, and Efthimis N. Efthimiadis. "Conversational tagging in twitter." Proceedings of the 21st ACM conference on Hypertext and hypermedia. ACM, 2010.

https://dl.acm.org/citation.cfm?id=1810647

## Evaluation

We have two work for the project, finding product name and finding top 10. The evaluate tool we used is randomly checking 50 tweets whether they are makeup product or not. The baseline method we used is checking true sales number and comparing for our finding top 10 results. 

We use bar chart to visualize our result. Regarding performance metrics, for finding product name, we’ll use precision and recall.


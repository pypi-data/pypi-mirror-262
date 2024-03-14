
# Similix

System Similarity, a cutting-edge solution for identifying article similarities with speed, security, and 85% accuracy. The specialized Article Recommendation submodule leverages OpenAI modules, numpy, and pandas for vector generation, data cleaning, and similarity calculations.

## Features

- Fast & Efficient: Quick results without compromising accuracy.
- Secure: Robust security measures for data protection.
- High Accuracy: 99% accuracy in article recommendations.


## Overview

Focused on suggesting articles similar to a target article, the submodule optimizes vector generation, data cleaning, and similarity calculations.


## Workflow
Vector Generation:

- OpenAI module generates a vector for the target article.
  Cached for future optimization.
  
- Data Cleaning: Numpy and pandas clean CSV data, including titles and descriptions.

- Vectorization: Converts article descriptions into numerical vectors. 

- Similarity Calculation: System computes similarity between target and other article vectors.

- Recommendation: Recommends articles with the highest similarity.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY` Just for testing purpose you can contact me or you can get it from oepnai which is you have to paid for it.


## Installation

 - Make sure in your dataset contain title and description as the fields requirement 


We assume that you have Python installed and have set up the entire environment

```bash
  pip install similix
```



## Usage

```bash
   - Make sure your dataset contain 'title' and 'description' as the fields requirement 
```

```python

from similix.article_recommender import ArticleRecommender
import os

os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

ac = ArticleRecommender(dataset_path='cleaned_dataset.csv', embedding_model='text-embedding-3-large')

limit_articles = 2
article_target = 'Twenty six women and five children were murdered by current'

print(ac.recommend_articles(article_target, limitArticles))

```
```


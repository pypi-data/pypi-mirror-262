import os
import pickle
import pandas as pd
from similix.embeddings_utils import TextEmbeddingsAnalyzer

cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'article_recommender.pkl')
cache_directory = os.path.dirname(cache_path)
if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)

DISTANCE_METRIC = 'cosine'


class ArticleRecommender:
    def __init__(self, embedding_model, dataset_path, batch_size=100):
        """
        Initialize the ArticleRecommender.

        Parameters:
        - embedding_model: The embedding model to use.
        - dataset_path: Path to the dataset CSV file.
        - batch_size: Batch size for processing embeddings.
        """
        self.embedding_model = embedding_model
        self.dataset_path = dataset_path
        self.embedding_cache_path = cache_path
        self.batch_size = batch_size
        self.embedding_cache = self._load_embedding_cache_()
        self.embedder = TextEmbeddingsAnalyzer()

    def _load_embedding_cache_(self):
        """
        Load the embedding cache from the file.

        Returns:
        - The loaded embedding cache.
        """
        try:
            return pd.read_pickle(self.embedding_cache_path)
        except FileNotFoundError:
            return {}

    def _update_embedding_cache_(self, string):
        """
        Update the embedding cache with the embedding for the given string.

        Parameters:
        - string: The input string.
        """
        self.embedding_cache[string] = self.embedder.get_embedding(string)

        with open(self.embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(self.embedding_cache, embedding_cache_file)
            print(f'Data Inserted ! :{string}')

    def _embedding_from_string_(self, string):
        """
        Get the embedding for the given string from the cache or update the cache.

        Parameters:
        - string: The input string.

        Returns:
        - The embedding for the input string.
        """
        if string not in self.embedding_cache:
            self._update_embedding_cache_(string)

        return self.embedding_cache[string]

    def recommend_articles(self, user_target_title, k_nearest_neighbors=5):
        """
        Recommend articles based on the user's target title.

        Parameters:
        - user_target_title: The target title for recommendations.
        - k_nearest_neighbors: The number of nearest neighbors to retrieve.

        Returns:
        - A list of dictionaries containing recommended articles and their details.
        """
        df = pd.read_csv(self.dataset_path)
        article_recommendations = []

        # Obtain the embedding for the user's target title from the cache or update the cache if necessary
        user_input_embedding = self._embedding_from_string_(user_target_title)

        # Retrieve the list of article descriptions from the DataFrame
        article_descriptions = df["description"].tolist()

        # Process articles in batches to avoid memory issues
        for i in range(0, len(article_descriptions), self.batch_size):
            # Extract a batch of article descriptions
            batch_descriptions = article_descriptions[i:i + self.batch_size]

            # Get embeddings for the batch of article descriptions
            embeddings = [self._embedding_from_string_(description) for description in batch_descriptions]

            # Calculate distances between the user's input embedding and the batch of article embeddings
            distances = self.embedder.distances_from_embeddings(user_input_embedding, embeddings,
                                                                distance_metric=DISTANCE_METRIC)

            # Find indices of the nearest neighbors based on the calculated distances
            indices_of_nearest_neighbors = self.embedder.indices_of_nearest_neighbors_from_distances(distances)

            # Process the k nearest neighbors for each article in the batch
            for j in range(min(k_nearest_neighbors, len(indices_of_nearest_neighbors))):
                article_index = indices_of_nearest_neighbors[j]
                article_title = df.loc[article_index, 'title']
                article_description = df.loc[article_index, 'description']
                distance = distances[article_index]

                article_recommendations.append({'title': article_title, 'description': article_description, 'distance': f'{distance:0.3f}'})

        return article_recommendations

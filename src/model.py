import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from datasets import load_dataset

# Load the dataset
reviews_dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", name="raw_review_All_Beauty", trust_remote_code=True)

raw_meta_dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", name="raw_meta_All_Beauty", trust_remote_code=True)

# Convert to a pandas DataFrame
df = reviews_dataset["full"].to_pandas()
df.dropna(subset=['asin', 'title', 'text'], inplace=True)

df.drop_duplicates(subset=['asin','title','text','user_id'], inplace=True)

# Create mappings from IDs to indices
user_map = {u: i for i, u in enumerate(df['user_id'].unique())}
item_map = {i: j for j, i in enumerate(df['asin'].unique())}

# Map the user_id and product_id to indices
df['user_idx'] = df['user_id'].map(user_map)
df['item_idx'] = df['asin'].map(item_map)

# Build a sparse matrix
from scipy.sparse import csr_matrix

# we create a sparse form of user_item_matrix:
# sparse_matrix = csr_matrix((data, (row, col)), shape=(a, b)
sparse_matrix = csr_matrix(
    (df['rating'], (df['user_idx'], df['item_idx'])),
    shape=(len(user_map), len(item_map))
)



from sklearn.metrics.pairwise import cosine_similarity

item_similarity = cosine_similarity(sparse_matrix.T)

column_names = df['asin'].unique()
item_similarity_df = pd.DataFrame(item_similarity, index=column_names, columns=column_names)



def recommend_products(product_id, num_recommendations):
    sim_scores = item_similarity_df[product_id].sort_values(ascending=False)[1:num_recommendations+1]
    return sim_scores.index.tolist()

if __name__ == '__main__':
    recommend_products('B00YQ6X8EO', 5)
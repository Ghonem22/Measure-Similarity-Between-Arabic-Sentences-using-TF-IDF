from data_preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from tqdm import tqdm

tqdm.pandas()
vectorizer = TfidfVectorizer()

def get_similarity(df, vectors, keyword):
    traninput = vectorizer.transform([preprocess_text(keyword)])
    traninput = traninput.toarray()
    cosine_sim = cosine_similarity(traninput,vectors)

    df[keyword] = pd.DataFrame(cosine_sim).T[0]
    return df

# Read Data
# change this number if you want to take sample of data, very large number take all the data
n1 = 0
n2 = 10000000
df = pd.read_csv("1.txt", sep="\t", encoding='utf-8-sig').iloc[n1:n2]
#clean Data
df['clean_text']=df['Tweet Text'].progress_apply(preprocess_text)

# prepare Vector required for getting similarity using tf-idf
vectors = vectorizer.fit_transform(df['clean_text'])

#iterating over
for keyword in config['keywords']:
    df = get_similarity(df, vectors, keyword)
del df['clean_text']


# if we want to sort the result using any of the keywords
# df = df.sort_values(by=[config['keywords'][0]], ascending=False)


# save the result
df.to_csv('df_similarity.csv', encoding='utf-8-sig')
"""Content-based movie discovery using genres and recovered MovieLens tags."""
from pathlib import Path
import sys,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results,chart,plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
BASE=Path(__file__).resolve().parent

def recommend(movies,matrix,title,k=5):
    exact=movies.index[movies.title.str.casefold()==title.casefold()]
    if not len(exact):raise ValueError('Title must exactly match a title in data/movies.csv.gz')
    index=int(exact[0]);similarity=linear_kernel(matrix[index],matrix).ravel();similarity[index]=-1
    selected=sorted(range(len(similarity)),key=lambda i:(-similarity[i],int(movies.iloc[i].movieId)))[:k]
    assert index not in selected
    return [{'movieId':int(movies.iloc[i].movieId),'title':str(movies.iloc[i].title),'similarity':round(float(similarity[i]),6)} for i in selected]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--title',default='Toy Story (1995)');args=parser.parse_args()
    movies=pd.read_csv(BASE/'data/movies.csv.gz').reset_index(drop=True);tags=pd.read_csv(BASE/'data/tags.csv')
    # The recovered file was called ratings.csv but its schema is the tags table.
    assert 'tag' in tags and 'rating' not in tags and movies.movieId.is_unique
    joined=tags.dropna(subset=['tag']).groupby('movieId').tag.agg(' '.join)
    text=movies.genres.fillna('').str.replace('|',' ',regex=False)+' '+movies.movieId.map(joined).fillna('')
    vectorizer=TfidfVectorizer(stop_words='english',ngram_range=(1,2),min_df=1)
    matrix=vectorizer.fit_transform(text)
    result=recommend(movies,matrix,args.title)
    write_results(BASE,{'movies':len(movies),'tag_rows':len(tags),'vocabulary_size':len(vectorizer.vocabulary_),
        'query':args.title,'recommendations':result,'method':'TF-IDF over genres and tags, cosine similarity, deterministic movieId tie-break',
        'limits':'This is content similarity, not collaborative filtering. No ratings or held-out preference labels are available, so predictive recommendation accuracy is not claimed.'})
    pd.DataFrame(result).to_csv(BASE/'outputs/recommendations.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,4));ax.barh([x['title'] for x in result][::-1],[x['similarity'] for x in result][::-1]);ax.set(title=f'Similar content to {args.title}',xlabel='Cosine similarity')
    chart(BASE,'recommendations.svg',fig)
if __name__=='__main__':main()

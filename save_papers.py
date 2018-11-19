import openreview
from collections import Counter, defaultdict as dd
import datetime
import re 
import pickle

def all_papers():
    client = openreview.Client(baseurl='https://openreview.net')
    paper_iterator = openreview.tools.iterget_notes(client, invitation='ICLR.cc/2019/Conference/-/Blind_Submission')
    return list(paper_iterator)

def ratings_and_confidence():
    client = openreview.Client(baseurl='https://openreview.net')
    review_iterator = openreview.tools.iterget_notes(client, invitation='ICLR.cc/2019/Conference/-/Paper.*/Official_Review')
    ratings = dd(list)
    confidence = dd(list)
    for review in review_iterator:
        ratings[review.forum].append(int(re.findall(pattern='\d+', string=review.content['rating'])[0]))
        confidence[review.forum].append(int(re.findall(pattern='\d+', string=review.content['confidence'])[0]))
    return ratings, confidence

print('Downloading papers...')
papers = all_papers()
ratings, confidence = ratings_and_confidence()

def add_ratings(papers, ratings, confidence):
    for ix in range(len(papers)):
        forum = papers[ix].forum
        papers[ix].ratings = ratings.get(forum, [])
        papers[ix].confidence = confidence.get(forum, [])

add_ratings(papers, ratings, confidence)

with open('papers/papers_{}.pckl'.format(datetime.datetime.now().date()), 'wb+') as f:
    pickle.dump(papers, f)
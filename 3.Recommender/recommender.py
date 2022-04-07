"""
Content-based recommender for games in BGA, given game history, favorite games
or categories and mechanics the user likes
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer

#we load the data
data=pd.read_csv('3.Recommender/boardgames.csv')

#category columns
category_cols = [col for col in data.columns if 'Category:' in col]

#Mechanic columns
mechanic_cols = [col for col in data.columns if 'Mechanic:' in col]

#all these features are binaries
data_cat=data[category_cols]
data_mec=data[mechanic_cols]

def tfidf(df):
    "Given a data frame, returns the tfidf representation"
    tfidf=TfidfTransformer()
    tfidf.fit(df)
    return tfidf.transform(df).toarray()

def df_norml2(vector):
    "Given a vector, returns the l2 norm"
    if np.square(vector).sum()!=0:
        vector=vector/np.sqrt(np.square(vector).sum())
    return vector

data_cat_tdifd=tfidf(data_cat)
data_mec_tdifd=tfidf(data_mec)


def recommendation_content_based(user_data,case):#case: 0 history, 1 fav games 2 cat and mec
    """given the user data, and the case (0,1 or 2), returns a list of
    games sorted by score"""
    if case==0: #game history
        #we only keep games played more than 10 times
        user_data_aux=user_data[user_data[user_data.columns[1]]>10] #we can change this
        if user_data_aux.shape[0]==0:
            user_data_aux=user_data
    elif case==1: #favourite games
        user_data_aux=user_data
        user_data_aux['Weight']=1
    if case in (0,1):
        #we rename the colum of games played in the case 1
        user_data_aux=user_data_aux.rename(columns={user_data_aux.columns[1]:'Weight'})
        for value in ('Name','Nombre'):
            if user_data_aux.columns[0]==value:
                #we merge the two data frames, to keep all the games, here we drop from the user the games that no longer exists in bga
                user_data_weights=data.merge(user_data_aux,how='left',on=value)['Weight'] #we keep the weight column only
                #we fill in with 0 the other games
                user_data_weights=user_data_weights.fillna(0)
        #we compute the user profiles multiplying the transformed category and mechanic matrix with the user data weight vector
        user_profile_cat =data_cat_tdifd.T.dot(user_data_weights)
        user_profile_mec = data_mec_tdifd.T.dot(user_data_weights)
    else: #case 2, the user profiles consist in 1 if the user likes the cat/mec and 0 if not
        user_profile_cat=[1 if cat in user_data[0] else 0 for cat in category_cols]
        user_profile_mec=[1 if mec in user_data[1] else 0 for mec in mechanic_cols]
    #we compute the similarity scores between our cat and mec data and the user profile (all is in norm l2 so it is the cosine similarity)
    scores_cat = data_cat_tdifd.dot(df_norml2(user_profile_cat))
    scores_mec = data_mec_tdifd.dot(df_norml2(user_profile_mec))
    #we sum the two scores
    scores=scores_cat+scores_mec
    #we transform the numpy array into a panda Series
    scores = pd.Series(scores)
    #we concat the scores with Name, Nombre, url, Thumbnail and Bayes_average_rating (we will use these)
    scores2=pd.concat([data[['Name','Nombre','url','Thumbnail','Bayes_average_rating']],scores.rename('Score')], axis=1)
    #we add a percentage of the rating, that will depende on the score of the 10th game or the last game with no null score
    #number of games with no null score
    scores_not_null=scores2[scores2.Score>0].shape[0]
    #the score of the 10th game or the last game with no null score
    score_last=scores2.sort_values(by=['Score'],ascending=False).Score.iloc[min(9,scores_not_null-1)]
    #we change the scores adding a percentage of the rating
    scores2.Score=scores2.Score+scores2.Bayes_average_rating*(score_last/10)
    if case in (0,1):
        #we return the recommendation without the games that the user already knows
        for value in ('Name','Nombre'):
            if user_data_aux.columns[0]==value:
                recommendation_news= scores2[~scores2[value].isin(user_data[value])].sort_values(by=['Score'],ascending=False)
                return (recommendation_news[[value,'url','Thumbnail','Score']], scores_not_null)
    else:
        recommendation=scores2.sort_values(by=['Score'],ascending=False)
        if user_data[2]==0:
            return (recommendation[['Name','url','Thumbnail','Score']],scores_not_null)
        return (recommendation[['Name','url','Thumbnail','Score']],scores_not_null)

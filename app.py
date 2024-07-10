import streamlit as st
st.title("Anime Recommender system")
import streamlit as st
import pickle
import pandas as pd
import requests
headers = {
    "X-MAL-CLIENT-ID": "8a978395398e5e83bd3f3c2db5654746"
}
params = {
    "fields": "rank,mean,alternative_titles"
}

def fetch_poster(anime_id):
    headers = {
        "X-MAL-CLIENT-ID": "8a978395398e5e83bd3f3c2db5654746"
    }
    params = {
        "fields": "rank,mean,alternative_titles"
    }

    response=requests.get(f'https://api.myanimelist.net/v2/anime/{anime_id}',headers=headers,params=params)
    medium_picture_url=""
    if response.status_code == 200:
        print("API call successful!")

        # Parse the JSON response
        data = response.json()


        # Print the entire JSON response for debugging


        # Extract the medium main picture URL

        if 'main_picture' in data and 'medium' in data['main_picture']:
            medium_picture_url = data['main_picture']['medium']



    return medium_picture_url


cosine_sim=pickle.load(open('similarity.pkl','rb'))
anime_list=pickle.load(open("allanime.pkl",'rb'))
#function to fetch the recommendation
def genre_recommendations(title):
    idx = anime[anime['name']==title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:7]
    anime_indices = [i[0] for i in sim_scores]

    posters=[]
    for j in anime_indices:
        curr=fetch_poster(j)
        if curr!="":
            posters.append(curr)




    recommended_anime=anime['name'].iloc[anime_indices]
    return recommended_anime,posters


anime=pd.DataFrame(anime_list)
option = st.selectbox(
    "Enter the anime to recommend for",
    anime['name'].values)

st.write("You selected:", option)
import streamlit as st


if st.button("Recommend"):
    name,poster=genre_recommendations(option)
    

    row1 = st.columns(3)
    row2 = st.columns(3)
    all_columns=row1+row2
    # Loop through each column and corresponding image
    for col, image_url,animename in zip(all_columns, poster,name):
        with col:
            st.image(image_url, caption='Sample Image', use_column_width=True)
            st.header(animename)  # Add a balloon emoji as a title
             # Add some text content




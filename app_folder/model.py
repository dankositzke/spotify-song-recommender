import pandas as pd
from sklearn.neighbors import KDTree


def find_recommendations(input_feature_vector):

    # Read in spotify data from csv
    df_with_song_names = pd.read_csv(
        "https://raw.githubusercontent.com/dankositzke/spotify-song-recommender/heroku-deployment/app_folder/assets/spotify_songs_dataset.csv",
        sep=",",
    )

    # Reduce columns to 13 to match the song features that Spotify API will return to us
    cols_to_drop = [
        "name",
        "album",
        "artists",
    ]
    df = df_with_song_names.drop(cols_to_drop, axis=1)

    # Randomly sample 100,000 rows from the data to reduce latency for user
    df_sample = df.sample(n=100000)

    # Initialize KDTree model from sklearn
    tree = KDTree(df_sample)

    # Query the model using the features from the user's selected song
    # Model will return the indices of the 10 most similar songs that it finds within the 100,000 rows
    dist, ind = tree.query([input_feature_vector], k=10)

    # Convert 'indices' output from array type to list
    ind = list(ind[0])

    id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    song_list = []
    artist_list = []
    album_list = []

    for each in ind:
        song_list.append(df_with_song_names.iloc[each]["name"])
        artist_list.append(
            df_with_song_names.iloc[each]["artists"]
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
        )
        album_list.append(df_with_song_names.iloc[each]["album"])

    recommendations = list(zip(id_list, song_list, artist_list, album_list))

    return recommendations

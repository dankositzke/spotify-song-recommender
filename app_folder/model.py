from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.neighbors import KDTree

DB = SQLAlchemy()


class Recommendations(DB.Model):
    """
    Creates a Recommendations Table with SQlAlchemy.
    This is useful for jinja2 HTML formatting in the 'recommendations.html' file.

    """

    id = DB.Column(DB.BigInteger, primary_key=True)
    song = DB.Column(DB.String, nullable=False)
    artist = DB.Column(DB.String, nullable=False)
    album = DB.Column(DB.String, nullable=False)


def find_recommendations(input_feature_vector):
    url = 'https://github.com/JosiahLC/9sopt/blob/JosiahLC-patch-2/app_folder/spotify.csv'

    # Read in spotify data from csv
    df_with_song_names = pd.read_csv(url, error_bad_lines=False)

    # Reduce columns to 13 to match the song features that Spotify API will return to us
    cols_to_drop = [
        "year",
        "release_date",
        "explicit",
        "disc_number",
        "track_number",
        "artist_ids",
        "artists",
        "album_id",
        "album",
        "name",
        "id",
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

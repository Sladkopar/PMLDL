# Import necessary dependencies
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from search import TrackSearchEngine
from const import *
from preprocessor import TrackPreprocessor

class RecSys():
    """
    Recommend `k` tracks based on given track.
    
    Attributes
    ----------
    `client_id`: str = None
        Client ID from Spotify.
    `client_secret`: str = None
        Client Secret from Spotify.
    `pkl_path`: str = '../models/k_means.pkl'
        Path to ".pkl" K-Means model and Column Transformer.
    `db_path`: str = '../data/preprocessed_audio_features_clusters.csv'
        Path to ".csv" file that contains all preprocessed tracks.
    `track_preprocessor`: TrackPreprocessor
        Module for preprocessing new tracks.
    `search_engine`: TrackSearchEngine
        Search engine to retrieve features for new tracks based on Spotify API.
    """
    
    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        pkl_path: str = '../models/k_means.pkl',
        db_path: str = '../data/preprocessed_audio_features_clusters.csv'
    ) -> None:
        """
        Initialize `RecSys` class.
        
        Parameters
        ----------
        `client_id`: str = None
            Client ID from Spotify.
        `client_secret`: str = None
            Client Secret from Spotify.
        `pkl_path`: str = '../models/k_means.pkl'
            Path to ".pkl" K-Means model and Column Transformer.
        `db_path`: str = '../data/preprocessed_audio_features_clusters.csv'
            Path to ".csv" file that contains all preprocessed tracks.
        
        Returns
        ----------
        `self`: RecSys
            RecSys class object.
        """
        
        assert client_id is not None and client_secret is not None, (
            "`client_id`, and `client_secret` must be specified."
        )
        
        self.track_preprocessor = TrackPreprocessor(pkl_path=pkl_path)
        self.track_db = pd.read_csv(db_path, index_col='Unnamed: 0')
        self.track_db_features = self.track_db.drop(labels=['id', 'name', 'album', 'album_id', 'artists', 'artist_ids', 'track_number'], axis=1)
        
        self.search_engine = TrackSearchEngine(
            client_id=client_id,
            client_secret=client_secret
        )
        
    def recommend(self, track_name: str = None, top_k: int = 5) -> pd.DataFrame:
        """
        Recommend `top_k` tracks from `self.db_path` using K-Means clustering.
        
        Parameters
        ----------
        `track_name`: str = None
            The name of the track.
        `top_k`: int = 5
            The amount of most similar tracks to retrieve.
        
        Returns
        ----------
        `result`: pd.DataFrame
            A Data frame that contains `name`, `album`, `artists`, and `track_number` of retrieved tracks.
        """
        
        assert track_name is not None, (
            "`track_name` must be specified."
        )
        
        f = self.search_engine.find_track_features(track_name)

        form = self.search_engine.format_track(f)
        
        target_track_preprocessed = self.track_preprocessor.preprocess(form)
        
        retrieved_track_features = self.track_db_features.loc[self.track_db_features.loc[:, 'cluster'] ==
                                                              target_track_preprocessed.loc[:, 'cluster'].values[0], :].drop(labels=['cluster'], axis=1)
        
        retrieved_track_features['similarity'] = cosine_similarity(X=target_track_preprocessed.drop(labels=['cluster'], axis=1).values, Y=retrieved_track_features.values)[0]
        top_k_tracks = retrieved_track_features.nlargest(top_k, 'similarity')
        top_k_tracks_ids = top_k_tracks.index.values
        
        return self.track_db.loc[top_k_tracks_ids, ['name', 'album', 'artists', 'track_number']].reset_index(drop=True)
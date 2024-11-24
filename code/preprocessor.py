# Import necessary dependencies
import pandas as pd
import pickle

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

import numpy as np

from const import *

class TrackPreprocessor():
    """
    Preprocess given track using K-Means clustering and Column Transformer.
    
    Attributes
    ----------
    `k_means`: KMeans
        Clustering model.
    `column_transformer`: ColumnTransformer
        Standardizes specific track features.
    """
    
    def __init__(self, pkl_path: str = None) -> None:
        """
        Initialize `TrackPreprocessor` object.
        
        Parameters
        ----------
        `pkl_path`: str = None
            Path to ".pkl" K-Means model and Column Transformer.
        
        Returns
        ----------
        `self`: TrackPreprocessor
            TrackPreprocessor class object.
        """
        
        assert pkl_path is not None, (
            '`pkl_path` must be specified.'
        )
        
        with open(pkl_path, 'rb') as f:
            tools_dict = pickle.load(f)
    
        self.k_means = tools_dict.get('k_means')
        self.column_transformer = tools_dict.get('column_transformer')
        
    def preprocess(self, track_data: dict = None) -> pd.DataFrame:
        """
        Preprocess features of given track.
        
        Parameters
        ----------
        `track_data`: dict = None
            Dictionary with all features of given track.
        
        Returns
        ----------
        `preprocessed_target_track_df`: pd.DataFrame
            Data frame with all preprocessed track features.
        """
        
        assert track_data is not None, (
            '`track_data` must be specified.'
        )
        
        target_track_df = pd.DataFrame(data=track_data)
        
        # Encoder `explicit` column
        target_track_df['explicit'] = target_track_df.loc[:, 'explicit'].apply(lambda x: 1 if x else 0)
        
        # Encode `key` column
        target_track_df['key_sine'] = np.sin(2 * np.pi * target_track_df.loc[:, 'key'] / 12)
        target_track_df['key_cosine'] = np.cos(2 * np.pi * target_track_df.loc[:, 'key'] / 12)
        
        # Encode `time_signature` column
        target_track_df['time_signature'] = (target_track_df.loc[:, 'time_signature'] != 4.0).astype(int)
        
        preprocessed_target_track_data = self.column_transformer.transform(target_track_df)
        preprocessed_column_names = list(map(lambda x: x.split('__')[1], self.column_transformer.get_feature_names_out().tolist()))
        preprocessed_target_track_df = pd.DataFrame(data=preprocessed_target_track_data, columns=preprocessed_column_names)
        
        # Acquire `cluster` for target track
        preprocessed_target_track_df['cluster'] = self.k_means.predict(preprocessed_target_track_df)
        
        return preprocessed_target_track_df
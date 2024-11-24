import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class TrackSearchEngine():
    """
    Implementation of the Track Search Engine
    
    Attributes
    ----------
    `client_id`: str = None
        Spotify client id
    `client_secret`: str = None
        Spotify client secret
    """

    def __init__(self, client_id: str = None, client_secret: str = None) -> None:
        """
        Implementation of the Track Search Engine
        
        Attributes
        ----------
        `client_id`: str = None
            Spotify client id
        `client_secret`: str = None
            Spotify client secret

        Returns
        ----------
        `self`: TrackSearchEngine
            TrackSearchEngine class object with initialized Spotify Manager.
        """
        
        # Assertion error on initialization
        assert client_id is not None and client_secret is not None, (
            "`client_id` or `client_secret` must be specified."
        )
        
        self.client_id = client_id
        self.client_secret = client_secret
        
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def search_track(self, query):
        """
        Searching for a track via Spotify API
        
        Parameters
        ----------
        `query`: str
            Search query
        
        Returns
        ----------
        `result`: dict
            The dictionary containing features of a first track.
        """
        results = self.sp.search(q=query, type='track', limit=1)
        return results['tracks']['items'][0]

    def get_audio_features(self, track_id):
        """
        Extracting numerical audio features of one track.
        
        Parameters
        ----------
        `track_id`: str
            ID of the track on Spotify
        
        Returns
        ----------
        `features`: dict
            Dictionary containing features.
        """
        audio_info = self.sp.audio_features([track_id])[0]
        return audio_info

    def find_track_features(self, title, artist=None):
        """
        Combination of `search_track` and `get_audio_features`.
        
        Parameters
        ----------
        `title`: str
            Title of a track
        `artist`: str = None
            Name of the artist.
        
        Returns
        ----------
        `features`: dict
            Dictionary containing alphanumerical features.
        """
        if artist:
            query = f'track:{title} artist:{artist}'
        else:
            query = f'track:{title}'

        features = self.search_track(query)
        features = features | self.get_audio_features(features['id'])
        return features

    def format_track(self, info):
        """
        Formatting of features to the same format as in DataFrame.
        
        Parameters
        ----------
        `info`: dict
            Features of a track
        
        Returns
        ----------
        `features`: dict
            Dictionary containing all the necessary features.
        """
        features = dict({
            'id': info.get('id'),
            'name': info.get('name'),
            'album': info['album'].get('name') if info.get('album') else None,
            'album_id': info['album'].get('id') if info.get('album') else None,
            'artists': '',
            'artist_ids': '',
            'track_number': info.get('track_number'),
            'disc_number': info.get('disc_number'),
            'explicit': info.get('explicit'),
            'danceability': info.get('danceability'),
            'energy': info.get('energy'),
            'key': info.get('key'),
            'loudness': info.get('loudness'),
            'mode': info.get('mode'),
            'speechiness': info.get('speechiness'),
            'acousticness': info.get('acousticness'),
            'instrumentalness': info.get('instrumentalness'),
            'liveness': info.get('liveness'),
            'valence': info.get('valence'),
            'tempo': info.get('tempo'),
            'duration_ms': info.get('duration_ms'),
            'time_signature': info.get('time_signature'),
            'year': info['album']['release_date'].split('-')[0] if info.get('album') and info['album'].get('release_date') else None,
            'release_date': info['album'].get('release_date') if info.get('album') else None,

            'popularity': info.get('popularity')
            })
        
        artists_names = [artist['name'] for artist in info['artists']]
        features['artists'] = artists_names
        artists_ids = [artist['id'] for artist in info['artists']]
        features['artist_ids'] = artists_ids
        return features
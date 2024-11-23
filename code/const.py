PREPROCESSED_FEATURES = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo', 'duration_ms', 'year', 'explicit', 'mode', 'key_sine', 'key_cosine', 'time_signature']

AUDIO_FEATURES = ['danceability', 'energy', 'loudness', 'speechiness', 
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
NUMERIC_FEATURES = ['duration_ms', 'year']
BINARY_FEATURES = ['explicit', 'mode']
CYCLIC_FEATURES = ['key']
TIME_SIGNATURE_FEATURES = ['time_signature']

K_CLUSTERS = 33
from Model.Track import Track
from Controller.SpotifyAPI import get_spotify_client

class AudioFeature:
  """Represents the audio features of a given track"""
  
  audio_features_cache = {} # trackID : audioFeature dictionary previously fetched
  
  def __init__(self, trackObjet : Track) -> None:
    client = get_spotify_client()
    
    # Check if the audio features are already cached
    if trackObjet.id in AudioFeature.audio_features_cache:
      print("Building AudioFeature object from cache")
      audioFeature_dict = AudioFeature.audio_features_cache[trackObjet.id]
    else:
      audioFeature_dict = client.audio_features(trackObjet.id)[0] # Assuming only one track is returned
    
    self.danceability = audioFeature_dict['danceability']
    self.energy = audioFeature_dict['energy']
    self.duration_ms = audioFeature_dict['duration_ms']
    self.instrumentalness = audioFeature_dict['instrumentalness']
    self.key = audioFeature_dict['key']
    self.liveness = audioFeature_dict['liveness']
    self.loudness = audioFeature_dict['loudness']
    self.mode = audioFeature_dict['mode']
    self.speechiness = audioFeature_dict['speechiness']
    self.tempo = audioFeature_dict['tempo']
    self.time_signature = audioFeature_dict['time_signature']
    self.valence = audioFeature_dict['valence']

    # Caching
    AudioFeature.audio_features_cache[trackObjet.id] = audioFeature_dict


class AudioFeatureAverage:
  
  def __init__(self, audioFeaturesList : list[AudioFeature]) -> None:
    self.danceability = sum([audioFeature.danceability for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.energy = sum([audioFeature.energy for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.duration_ms = sum([audioFeature.duration_ms for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.instrumentalness = sum([audioFeature.instrumentalness for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    # self.key = sum([audioFeature.key for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.liveness = sum([audioFeature.liveness for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.loudness = sum([audioFeature.loudness for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    # self.mode = sum([audioFeature.mode for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.speechiness = sum([audioFeature.speechiness for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.tempo = sum([audioFeature.tempo for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.time_signature = sum([audioFeature.time_signature for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
    self.valence = sum([audioFeature.valence for audioFeature in audioFeaturesList]) / len(audioFeaturesList)
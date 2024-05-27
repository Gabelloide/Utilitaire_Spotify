
class HistoryTrack:
  """
  Class to represent a track in the Spotify history.
  This is useful to use attributes to fill the SQL database.
  """
  def __init__(self, trackDict):
    self.ts = trackDict.get('ts', None)
    self.username = trackDict.get('username', None)
    self.platform = trackDict.get('platform', None)
    self.ms_played = trackDict.get('ms_played', None)
    self.conn_country = trackDict.get('conn_country', None)
    self.ip_addr_decrypted = trackDict.get('ip_addr_decrypted', None)
    self.user_agent_decrypted = trackDict.get('user_agent_decrypted', None)
    self.master_metadata_track_name = trackDict.get('master_metadata_track_name', None)
    self.master_metadata_album_artist_name = trackDict.get('master_metadata_album_artist_name', None)
    self.master_metadata_album_album_name = trackDict.get('master_metadata_album_album_name', None)
    self.spotify_track_uri = trackDict.get('spotify_track_uri', None)
    self.episode_name = trackDict.get('episode_name', None)
    self.episode_show_name = trackDict.get('episode_show_name', None)
    self.spotify_episode_uri = trackDict.get('spotify_episode_uri', None)
    self.reason_start = trackDict.get('reason_start', None)
    self.reason_end = trackDict.get('reason_end', None)
    self.shuffle = trackDict.get('shuffle', None)
    self.skipped = trackDict.get('skipped', None)
    self.offline = trackDict.get('offline', None)
    self.offline_timestamp = trackDict.get('offline_timestamp', None)
    self.incognito_mode = trackDict.get('incognito_mode', None)
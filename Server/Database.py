import json, os, mysql.connector
from datetime import datetime
from HistoryTrack import HistoryTrack

class Database:
  
  def __init__(self, host, user, password, database, port) -> None:
    
    self.mySQL = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database,
      port=port)


  def create_history_table(self) -> None :
    cursor = self.mySQL.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS History \
                  (ts DATETIME, username VARCHAR(255), \
                  platform VARCHAR(255), ms_played INT, \
                  conn_country VARCHAR(255), \
                  ip_addr_decrypted VARCHAR(255), \
                  user_agent_decrypted VARCHAR(255), \
                  master_metadata_track_name VARCHAR(255), \
                  master_metadata_album_artist_name VARCHAR(255), \
                  master_metadata_album_album_name VARCHAR(255), \
                  spotify_track_uri VARCHAR(255), \
                  episode_name VARCHAR(255), \
                  episode_show_name VARCHAR(255), \
                  spotify_episode_uri VARCHAR(255), \
                  reason_start VARCHAR(255), \
                  reason_end VARCHAR(255), \
                  shuffle VARCHAR(255), \
                  skipped VARCHAR(255), \
                  offline VARCHAR(255), \
                  offline_timestamp VARCHAR(255), \
                  incognito_mode VARCHAR(255), \
                  userID VARCHAR(255),  \
                  PRIMARY KEY (ts, username, spotify_track_uri), \
                  FOREIGN KEY(userID) REFERENCES User(userID))" #! One line is a track, listened at one unique date by one unique user.
                  )
    self.mySQL.commit()


  def create_user_table(self) -> None :
    cursor = self.mySQL.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS User (userID VARCHAR(255), username VARCHAR(255), PRIMARY KEY(userID) )")
    self.mySQL.commit


  def create_friends_table(self) -> None:
    cursor = self.mySQL.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Friends (userID VARCHAR(255), friendID VARCHAR(255), PRIMARY KEY(userID, friendID), FOREIGN KEY(userID) REFERENCES User(userID), FOREIGN KEY(friendID) REFERENCES User(userID))")
    self.mySQL.commit()


  def populate_history_table(self, tracklist:list[HistoryTrack]) -> None:
    """tracklist : list of HistoryTrack objects, which are made to be inserted in the database"""
    cursor = self.mySQL.cursor()
    for history_track in tracklist:
      # Convert the timestamp from ISO 8601 to MySQL compatible format
      if history_track.ts:
          mysql_ts = datetime.strptime(history_track.ts, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
      else:
          mysql_ts = None
      
      sql = "INSERT INTO History (ts, username, platform, ms_played, conn_country, \
      ip_addr_decrypted, user_agent_decrypted, master_metadata_track_name, \
      master_metadata_album_artist_name, master_metadata_album_album_name, \
      spotify_track_uri, episode_name, episode_show_name, spotify_episode_uri, \
      reason_start, reason_end, shuffle, skipped, offline, offline_timestamp, incognito_mode) VALUES \
      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  
      values = (mysql_ts, 
                history_track.username, 
                history_track.platform, 
                history_track.ms_played, 
                history_track.conn_country,
                history_track.ip_addr_decrypted,
                history_track.user_agent_decrypted,
                history_track.master_metadata_track_name,
                history_track.master_metadata_album_artist_name,
                history_track.master_metadata_album_album_name,
                history_track.spotify_track_uri,
                history_track.episode_name,
                history_track.episode_show_name,
                history_track.spotify_episode_uri,
                history_track.reason_start,
                history_track.reason_end,
                history_track.shuffle,
                history_track.skipped,
                history_track.offline,
                history_track.offline_timestamp,
                history_track.incognito_mode)
      cursor.execute(sql, values)

    self.mySQL.commit()


  def check_history_table_existence(self) -> bool:
    cursor = self.mySQL.cursor()
    cursor.execute("SHOW TABLES LIKE 'History'")
    tables = cursor.fetchall()
    if len(tables) > 0:
      return True
    return False


  def check_user_exists(self, userID) -> bool:
    """Checks if the userID is present in the User table"""
    cursor = self.mySQL.cursor()
    sql = "SELECT * FROM User WHERE userID = %s"
    values = (userID,)
    cursor.execute(sql, values)
    user = cursor.fetchone()
    if user:
      return True
    return False 
  
  
  def insert_user(self, userID, username) -> bool:
    """Inserts a user in the database, table User
    Returns True/False depending of the success of the operation."""
    try:
      if self.check_user_exists(userID): # If the user is already in the database, we don't insert it again, and it's OK.
        return True
      
      cursor = self.mySQL.cursor()
      sql = "INSERT INTO User (userID, username) VALUES (%s, %s)"
      values = (userID, username)
      cursor.execute(sql, values)
      self.mySQL.commit()
      return True
    except Exception as e:
      print(f"Error during user insertion in database: {e}")
      return False
    
    
  def get_friends(self, userID) -> list[str]:
    """Returns the list of friends of a user given its userID"""
    cursor = self.mySQL.cursor()
    sql = "SELECT friendID FROM Friends WHERE userID = %s"
    values = (userID,)
    cursor.execute(sql, values)
    friends = cursor.fetchall()
    return [friend[0] for friend in friends] # first element of each tuple in the list because fetchall returns a list of tuples (userID,)
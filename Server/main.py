import zipfile, os, json, shutil, socket

from Database import Database
from HistoryTrack import HistoryTrack

# Constants
SAVE_PATH = f"{os.getcwd()}\\received_zips"
ZIP_DESTINATION = f"{os.getcwd()}\\received_data"


def create_random_seed():
  """Create a random seed of 10 characters to put at the end of filenames (prevent overwriting)"""
  import random, string
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def clean_data(data):
  """
  Clean the data from the json files.
  We want to keep only the tracks that were played for more than 30 seconds. (30_000 ms)
  We also want to keep only the tracks, not the episodes.
  Also eliminating perfect duplicates (every attributes identical)
  """
  tracklist = [HistoryTrack(track) for track in data]
  tracklist = [track for track in tracklist if track.ms_played > 30_000 and track.spotify_track_uri is not None]
  track_tuples = [tuple(vars(track).values()) for track in tracklist] # Convert each HistoryTrack to a tuple of its attributes
  unique_track_tuples = list(set(track_tuples)) # Use a set to remove duplicates
  tracklist = [HistoryTrack(dict(zip(vars(tracklist[0]).keys(), track_tuple))) for track_tuple in unique_track_tuples] # Convert each tuple of attributes back to a HistoryTrack
  return tracklist


def main():
  # Create a socket object, to bind it to the server
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    
    print("Server is listening on {0}".format(server_socket.getsockname()))

    while True:
      connection, adress = server_socket.accept()
      with connection:
        print(f"Connected by {adress}")

        # Check if the save path exists, if not create it
        if not os.path.exists(SAVE_PATH):
          os.makedirs(SAVE_PATH)

        # Receive the zip file
        saved_zip_path = SAVE_PATH + f"\\spotify_zip_{create_random_seed()}.zip"
        with open(saved_zip_path, 'wb') as received_file:
          while True:
            data = connection.recv(1024)
            if not data:
              break
            received_file.write(data)

        # Extract the zip file
        try:
          with zipfile.ZipFile(saved_zip_path, 'r') as zip_ref:
            zip_ref.extractall(ZIP_DESTINATION)

          # Check how many json files are in the zip to process them
          folder_inside_zip = "Spotify Extended Streaming History" # The folder inside the zip file
          json_files = [f for f in os.listdir(f"{ZIP_DESTINATION}\\{folder_inside_zip}") if f.endswith('.json')]
          # Load the json files
          data = []
          for file in json_files:
            with open(f"{ZIP_DESTINATION}/{folder_inside_zip}/{file}", 'r', encoding='utf-8') as f:
              data.append(json.load(f))
          
          # Flatten the list of dictionaries : eliminate the list of dictionaries and keep only the dictionaries in one list
          data = [item for sublist in data for item in sublist]

          # Clean the data
          tracklist = clean_data(data)
          
          # Fetch that into the database
          try:
            db = Database("localhost", "root", "root", "spotify_history")
            
            if not db.check_history_table_existence():
              print("The table 'History' doesn't exist in the database, creating it...")
              db.create_history_table()

            db.populate_history_table(tracklist)
            print(f"Inserted {len(tracklist)} tracks in the database.")
            
          except Exception as e:
            print(f"An error occured with the database : {e}")

        except Exception as e:
          print(f"An error occured with this connection : {e}")
        finally:
          connection.close()
          # Clean the zip file and the extracted folders
          shutil.rmtree(SAVE_PATH)
          shutil.rmtree(ZIP_DESTINATION)


if __name__ == "__main__":
  main()
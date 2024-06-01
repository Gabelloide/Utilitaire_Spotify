import socket, pickle, json, threading, os
import constants

# SOCKET PORT : 23456

lock = threading.Lock()

def wait_for_track():
  """This function is used to wait for a track to be sent by the client. This track is then inserted into a shared trend dict, which contains the added tracks."""

  trendDict = {}
  
  # Looking for the trends.json file, if it doesn't exist, create it
  if not os.path.exists("trends.json"):
    with open("trends.json", "w") as file:
      json.dump({}, file)
  
  # Filling back the trendDict from trends.json file to be up to date
  try:
    with open("trends.json", "r") as file:
      trendDict = json.load(file)
  except Exception as e:
    print("Error in reading trends.json file")
    print(e)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((constants.SERVER_ADDRESS, constants.SERVER_TREND_PORT))
    server_socket.listen()
    
    print(f"trendReceiverThread is listening on {server_socket.getsockname()}")
    
    while True:
      connection, adress = server_socket.accept()
      with connection:
        print(f"Connected by {adress}")

        # Process received data w/ pickle
        # Data received is a tuple of (trackID, userID)
        
        data = receive_all(connection)
        try:
          trackID, userID = pickle.loads(data)

          # Acquiring the lock before modifying the shared trendDict json file
          with lock: # With block is charged of acquiring and releasing the lock
            if trackID in trendDict:
              trendDict[trackID]["upvotes"] += 1
              # Original user that added remains unchanged
            else:
              trendDict[trackID] = {"upvotes": 1, "addedBy": userID}

            # Save the updated trendDict to trends.json
            try:
              with open("trends.json", "w") as file:
                json.dump(trendDict, file, indent=4)
            except Exception as e:
              print("Error in writing to trends.json file")
              print(e)

        except Exception as e:
          print("Exception in trendReceiverThread")
          print(e)
        
      connection.close()


def receive_all(sock):
    """This function is used to receive all data from a socket"""
    data = b''
    while True:
        part = sock.recv(1024)
        data += part
        if len(part) < 1024:
            # either 0 or end of data
            break
    return data
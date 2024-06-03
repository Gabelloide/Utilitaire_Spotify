import socket, pickle, json, threading, os
import constants

# SOCKET PORT : 23458

lock = threading.Lock()

def wait_for_upvote():
  """Will wait for a message to upvote a track"""
  global trendDict

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((constants.SERVER_ADDRESS, constants.SERVER_TREND_UPVOTING_PORT))
    server_socket.listen()
    
    print(f"trendUpvoterThread is listening on {server_socket.getsockname()}")
    
    while True:
      connection, adress = server_socket.accept()
      with connection:
        print(f"Connected by {adress}")
        
        # Looking for the trends.json file, if it doesn't exist, create it
        if not os.path.exists("trends.json"):
          with open("trends.json", "w") as file:
            json.dump({}, file)
        
        # Filling back the trendDict from trends.json file to be up to date
        try:
          if os.path.getsize("trends.json") > 0:
            with open("trends.json", "r") as file:
              trendDict = json.load(file)
        except Exception as e:
          print("Error in reading trends.json file")
          print(e)

        # Process received data w/ pickle
        # Data received is a tuple (trackID, userID)
        
        data = receive_all(connection)
        try:
          trackID, userID = pickle.loads(data)
          
          # Acquiring the lock before modifying the shared trendDict json file
          with lock:
            if trackID in trendDict:
              if userID in trendDict[trackID]["upvotedBy"]:
                # User has already upvoted the track
                # Remove the upvote
                trendDict[trackID]["upvotes"] -= 1
                trendDict[trackID]["upvotedBy"].remove(userID)
              else:
                # User hasn't upvoted the track
                # Add the upvote
                trendDict[trackID]["upvotes"] += 1
                trendDict[trackID]["upvotedBy"].append(userID)
              
            try:
              with open("trends.json", "w") as file:
                json.dump(trendDict, file, indent=4)
            except Exception as e:
              print("Error in writing to trends.json file")
              print(e)
          
        except Exception as e:
          print("Exception in trendUpvoterThread")
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
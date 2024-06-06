import socket, pickle, json, threading, os
import constants, utils

# SOCKET PORT : 23456


def trendThreadMainLoop():
  """Will wait for differents messages to perform specific actions on trends
  - Add a track to the trends
  - Perform upvoting on a track
  - Send trends to the client"""
  global trendDict
  
  lock = threading.Lock()

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((constants.SERVER_ADDRESS, constants.SERVER_TREND_PORT))
    server_socket.listen()
    
    print(f"trendThread is listening on {server_socket.getsockname()}")
    
    while True:
      connection, adress = server_socket.accept()
      with connection:
        print(f"Connected by {adress}")
      
        # Looking for the trends.json file, if it doesn't exist, create it
        if not os.path.exists("trends.json"):
          with open("trends.json", "w") as file:
            json.dump({}, file)

        # ---- WAIT FOR CORRECT ASKING MESSAGES TO RESPOND ----
        data = utils.receive_all(connection)
        
        try:

          # ---- CLIENT ASKS FOR TRENDS ----
          if data == b"ASKING_TRENDS":
            print("client asked for trends")
            # Client asked for trends, sending them
            with lock:
              try:
                with open("trends.json", "r") as file:
                  trendDict = json.load(file)
                  connection.sendall(json.dumps(trendDict).encode()) # Send the trend dict to the client
              except Exception as e:
                print("Error in trendThread, while reading trends.json file")
                print(e)


          # ---- CLIENT ADDS A TRACK ----
          elif data == b"SEND_TRACK":
            print("client asked to send a track")
            # Tell the client that we are ready to receive the track
            connection.sendall(b"READY")
            
            # Opening trends.json file to update the trendDict
            with lock:
              try:
                with open("trends.json", "r") as file:
                  trendDict = json.load(file)
              except Exception as e:
                print("Error in trendThread, while reading trends.json file")
                print(e)
            
            # Process received data w/ pickle
            # Data received is a tuple of (trackID, userID)
            data = utils.receive_all(connection)
            try:
              trackID, userID = pickle.loads(data)

              # Acquiring the lock before modifying the shared trendDict json file
              with lock: # With block is charged of acquiring and releasing the lock
                if trackID in trendDict:
                  # Original user that added remains unchanged
                  # The user that upvoted is added to the list of upvoters
                  if userID not in trendDict[trackID]["upvotedBy"]:
                    trendDict[trackID]["upvotes"] += 1
                    trendDict[trackID]["upvotedBy"].append(userID)
                else:
                  trendDict[trackID] = {"upvotes": 1, "addedBy": userID, "upvotedBy": [userID]} # The user that added the track is the first to upvote it

                # Save the updated trendDict to trends.json
                try:
                  with open("trends.json", "w") as file:
                    json.dump(trendDict, file, indent=4)
                except Exception as e:
                  print("Error in writing to trends.json file")
                  print(e)
                  
            except Exception as e:
              print("Exception while receiving track in trendThread")
              print(e)


          # ---- CLIENT UPVOTES A TRACK ----
          elif data == b"ASKING_UPVOTE":
            print("client asked to upvote a track")
            # Tell the client that we are ready to receive the upvote
            connection.sendall(b"READY")
            
            # Opening trends.json file to update the trendDict
            with lock:
              try:
                with open("trends.json", "r") as file:
                  trendDict = json.load(file)
              except Exception as e:
                print("Error in trendThread, while reading trends.json file")
                print(e)
            
            # Process received data w/ pickle
            # Data received is a tuple (trackID, userID)
            data = utils.receive_all(connection)
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
                    # If the track has no more upvotes, remove it from the trends
                    if trendDict[trackID]["upvotes"] == 0:
                      del trendDict[trackID]
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
            
            

        except Exception as e:
          print(f"Error in trendThreadMainLoop: {e}")
import socket, threading, json
import constants
# This thread will be in charge of sending the trend dict to the client side
# This client will be charged to fetch all tracks again from the ids and display them correctly.

lock = threading.Lock()

def wait_to_send():
  
  # Create a socket object, to bind it to the server
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((constants.SERVER_ADDRESS, constants.SERVER_TREND_FETCHING_PORT))
    server_socket.listen()
    
    print("trendSenderThread is listening on {0}".format(server_socket.getsockname()))
    
    while True:
      connection, adress = server_socket.accept()
      with connection:
        print(f"Connected by {adress}")

        # Upon connection, fetch the trend dict from the trends.json file & send it to the client
        # Locking the file to avoid reading it while it's being written to
        with lock:
          try:
            with open("trends.json", "r") as file:
              trendDict = json.load(file)
              connection.sendall(json.dumps(trendDict).encode()) # Send the trend dict to the client
          except Exception as e:
            print("Error in reading trends.json file")
            print(e)
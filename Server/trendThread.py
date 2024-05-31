import socket

# Key: (trackObject, userThatAddedTrack)
# Value: (upvoteNumber)
trendDict = {}

# SOCKET PORT : 23456

def wait_for_track():
  """This function is used to wait for a track to be sent by the client. This track is then inserted into a shared trend dict, which contains the added tracks."""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 23456))
    server_socket.listen()
    
    print(f"trendThread is listening on {server_socket.getsockname()}")
    
    while True:
      connection, adress = server_socket.accept()
      with connection:
        print(f"Connected by {adress}")

        # Process received data
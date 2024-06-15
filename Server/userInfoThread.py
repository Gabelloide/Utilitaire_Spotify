import socket, pickle
import constants
import entrypoint

def log_user_in_database():
  
  # Create a socket object, to bind it to the server
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((constants.SERVER_ADDRESS, constants.SERVER_USERINFO_PORT))
    server_socket.listen()
    
    print(f"userinfo thread is listening on {server_socket.getsockname()}")
    
    while True:
      connection, address = server_socket.accept()
      
      with connection:
        print(f"Connected by {address}")
        
        # ---- WAIT FOR CORRECT ASKING MESSAGES TO RESPOND ----
        data = receive_all(connection)

        try:
          if data == b"SEND_USERINFO":
            print("Client asked to send userinfo")
            # Tell the client that we are ready to receive userinfo
            connection.sendall(b"READY")
            
            # Processing received data
            data = receive_all(connection)
            userID, username = pickle.loads(data)

            database = entrypoint.getDatabaseObject()
            if database.insert_user(userID, username):
              connection.sendall(b"SQL_OK")
        
          elif data == b"GET_FRIENDS":
            print("Client asked for friends list")
            # Tell the client that we are ready to send the friends list
            connection.sendall(b"READY")
            
            # Waiting for the user ID
            userID = receive_all(connection).decode()
            
            # Get friends list from the database (SQL)
            database = entrypoint.getDatabaseObject()
            friendsList = database.get_friends(userID)
            
            # Send the friends list to the client
            serialized_friendsList = pickle.dumps(friendsList)
            connection.sendall(serialized_friendsList)
            
          elif data == b"SEARCH_USERS":
            print("Client asked to search users")
            # Tell the client that we are ready to receive the query
            connection.sendall(b"READY")
            
            # Waiting for the query
            query = receive_all(connection).decode()
            
            # Get the users list from the database (SQL), according to the query
            database = entrypoint.getDatabaseObject()
            usersIDs = database.search_users(query)
            
            # Send the users list to the client
            serialized_usersIDs = pickle.dumps(usersIDs)
            connection.sendall(serialized_usersIDs)

        
        except Exception as e:
          print(f"Error in userinfo thread: {e}")



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
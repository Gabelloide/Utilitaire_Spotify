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
            
            print(userID)
            print(username)
            
            #TODO : sql ici pour insérer dans la talbe user
            #TODO : renvoyer un message au client pour dire que le sql est bon
        
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
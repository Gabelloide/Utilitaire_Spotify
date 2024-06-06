import constants

def connect_to_trends_server():
  """Binds and returns a socket to the server's trend port"""
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((constants.SERVER_ADDRESS, constants.SERVER_TREND_PORT))
  return s
  

def connect_to_zip_server():
  """Binds and returns a socket to the server's zip port"""
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((constants.SERVER_ADDRESS, constants.SERVER_ZIP_PORT))
  return s
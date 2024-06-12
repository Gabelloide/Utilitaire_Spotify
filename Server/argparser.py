import argparse
import constants

def init_argparser():
  parser = argparse.ArgumentParser(description="Server")
  
  # Server
  parser.add_argument('--zip_port', type=int, help='The port for the ZIP server')
  parser.add_argument('--trend_port', type=int, help='The port for the trend server')
  parser.add_argument('--server_address', type=str, help='The address of the server')
  
  # Database
  parser.add_argument('--db_address', type=str, help='The address of the database')
  parser.add_argument('--db_user', type=str, help='The user of the database')
  parser.add_argument('--db_password', type=str, help='The password of the database')
  parser.add_argument('--db_port', type=int, help='The port of the database')
  
  args = parser.parse_args()
  
  if args.zip_port:
    constants.SERVER_ZIP_PORT = args.zip_port
  if args.trend_port:
    constants.SERVER_TREND_PORT = args.trend_port
  if args.server_address:
    constants.SERVER_ADDRESS = args.server_address
  if args.db_address:
    constants.DB_ADDRESS = args.db_address
  if args.db_user:
    constants.DB_USER = args.db_user
  if args.db_password:
    constants.DB_PASSWORD = args.db_password
  if args.db_port:
    constants.DB_PORT = args.db_port
  
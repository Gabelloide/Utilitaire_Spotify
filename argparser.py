import argparse
import constants

def init_argparser():
  parser = argparse.ArgumentParser()

  parser.add_argument('--zip_port', type=int, help='The port for the ZIP server')
  parser.add_argument('--trend_port', type=int, help='The port for the trend server')
  parser.add_argument('--userinfo_port', type=int, help='The port for the user info server')
  parser.add_argument('--server_address', type=str, help='The address of the server')

  args = parser.parse_args()

  if args.zip_port:
    constants.SERVER_ZIP_PORT = args.zip_port
  if args.trend_port:
    constants.SERVER_TREND_PORT = args.trend_port
  if args.userinfo_port:
    constants.SERVER_USERINFO_PORT = args.userinfo_port
  if args.server_address:
    constants.SERVER_ADDRESS = args.server_address
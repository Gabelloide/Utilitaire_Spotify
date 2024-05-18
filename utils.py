import os

def load_env():
	"""Loads environment variables from .env file."""
	with open('.env', 'r') as file:
		lines = file.readlines()
		os.environ['SPOTIPY_CLIENT_ID'] = lines[0].split('=')[1].strip()
		os.environ['SPOTIPY_CLIENT_SECRET'] = lines[1].split('=')[1].strip()

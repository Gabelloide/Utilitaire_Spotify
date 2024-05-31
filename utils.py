import os

def load_env():
  """Loads environment variables from .env file."""
  with open('.env', 'r') as file:
    lines = file.readlines()
    os.environ['SPOTIPY_CLIENT_ID'] = lines[0].split('=')[1].strip()
    os.environ['SPOTIPY_CLIENT_SECRET'] = lines[1].split('=')[1].strip()


def check_cache_folder():
  """Checks if the cache folder exists, if not, creates it."""
  if not os.path.exists('cache'):
    os.mkdir('cache')


def save_to_cache(filename, data, extension='jpg'):
  """Saves the data to the cache folder."""
  check_cache_folder()
  with open(f'cache/{filename}.{extension}', 'wb') as file:
    file.write(data)


def exists_in_cache(filename, extension='jpg'):
  """Checks if the file exists in the cache folder."""
  return os.path.exists(f'cache/{filename}.{extension}')


def load_from_cache(filename, extension='jpg'):
  """Loads the data from the cache folder."""
  with open(f'cache/{filename}.{extension}', 'rb') as file:
    return file.read()
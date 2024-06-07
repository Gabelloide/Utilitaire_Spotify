import os
import unicodedata

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


def set_format_duration(duration_ms : int)-> str:
    # Convertir les millisecondes en secondes
    duration_s = duration_ms // 1000
    # Obtenir les minutes et les secondes
    minutes, seconds = divmod(duration_s, 60)
    # Retourner la durée formatée
    return f"{minutes}:{seconds:02d}"


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


def remove_accents(string):
  # Normalize the string to separate accented characters into base characters + diacritics
  normalized_string = unicodedata.normalize('NFD', string)
  # Filter out diacritics (accents) by keeping only the base characters
  string_without_accents = ''.join(c for c in normalized_string if unicodedata.category(c) != 'Mn')
  return string_without_accents
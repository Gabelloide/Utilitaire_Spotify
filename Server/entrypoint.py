import Database, constants

database = None

def initialize_database():
  global database
  """Create the database object, try to create the two required tables if they don't exist, and return the database object for future use."""
  try:
    database = Database.Database(constants.DB_ADDRESS, constants.DB_USER, constants.DB_PASSWORD, "spotify_history", constants.DB_PORT)
    database.create_user_table()
    database.create_friends_table()
    database.create_history_table()
    return database
  except Exception as e:
    print("Exception during initialize database :")
    print(e)
    return None


def getDatabaseObject():
  return database
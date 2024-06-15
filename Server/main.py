import threading
from zipThread import wait_for_zip_file
from trendThread import trendThreadMainLoop
from userInfoThread import log_user_in_database
import argparser, entrypoint

if __name__ == "__main__":
  
  trendDict = {} # Shared dict between threads
  
  argparser.init_argparser()
  
  database = entrypoint.initialize_database()
  
  # Upon connection, listen for the user's infos to add them to the database if necessary
  # Creating one thread for this purpose
  threading.Thread(target=log_user_in_database).start()
  
  # Create one thread for zip file reception
  # Create one thread for trends
  threading.Thread(target=wait_for_zip_file).start()
  threading.Thread(target=trendThreadMainLoop).start()

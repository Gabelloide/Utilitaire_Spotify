import threading
from zipThread import wait_for_zip_file
from trendThread import trendThreadMainLoop
import argparser

if __name__ == "__main__":
  
  trendDict = {} # Shared dict between threads
  
  argparser.init_argparser()
  
  # Create one thread for zip file reception
  # Create one thread for trends
  threading.Thread(target=wait_for_zip_file).start()
  threading.Thread(target=trendThreadMainLoop).start()
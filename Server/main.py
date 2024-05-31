import threading
from zipThread import wait_for_zip_file
from trendThread import wait_for_track

if __name__ == "__main__":
  
  # Create one thread for zip file reception
  # Create one thread for trends
  
  threading.Thread(target=wait_for_zip_file).start()
  threading.Thread(target=wait_for_track).start()
from PyQt6.QtGui import QPixmap
import requests
import threading

import utils

class AbstractImageSetter:
    def __init__(self):
        pass
    
    def downloadAndSetImage(self, url, filename):
        """Downloads the image from the internet and sets it to the QLabel.
        - Checks for the image existence in the cache.
        - If the image is not in the cache, it downloads it in a separate thread.
        """
        if url is None:
        # Fallback on the image placeholder
            with open("Assets/icons/user_placeholder.png", "rb") as file:
                data = file.read()
                self.setImage(data)
                return
        if utils.exists_in_cache(filename):
            data = utils.load_from_cache(filename)
            self.setImage(data)
        else:
            # Downloading the image in a separate thread
            threading.Thread(target=self.thread_download, args=(url, filename)).start()


    def thread_download(self, url, filename):
        """Used by a separate thread to download the image from the internet.
        - Gets the image data from the URL via a GET request.
        - Saves the image data to the cache.
        - Sets the image to the QLabel using the data downloaded.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.content
            utils.save_to_cache(filename, data)
            self.setImage(data)

        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
        


    def setImage(self, data):
        """Sets the image to the QLabel."""
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
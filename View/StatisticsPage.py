from PyQt6.QtWidgets import QWidget

from Model.User import User

class StatisticsPage(QWidget):
  """This class is responsible for displaying the user's statistics page.
  This is a big page that contains all the statistics of the user :
  - Number of tracks listened
  - Number of artists listened
  - Number of albums listened
  - Hours when music is listened
  - ...
  """
  
  def __init__(self, user:User, parentView) -> None:
    pass
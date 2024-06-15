from Model.User import User
from View.RecommendationPage import RecommendationPage


class ControllerRecommendationPage:
  
  def __init__(self, user:User, view: RecommendationPage):
    self.view = view
    self.user = user

    
    def setFocusedIcon(self, focusedButton):
      for button in self.view.buttonsNaviguation:
        if button == focusedButton:
          button.setStyleSheet(self.view.focusedButtonStyleSheet)
        else:
          button.setStyleSheet(self.view.buttonStyleSheet)
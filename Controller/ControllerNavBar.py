from View.NavBar import NavBar

class ControllerNavBar:
  def __init__(self, navBar: NavBar):
    self.navBar = navBar

    self.navBar.btnProfile.clicked.connect(self.showProfilePage)
    self.navBar.btnSearch.clicked.connect(self.showSearchPage)
    self.navBar.btnTrend.clicked.connect(self.showTrendPage)
    self.navBar.btnFriends.clicked.connect(self.showFriendsPage)
    self.navBar.btnStats.clicked.connect(self.showStatsPage)

  def showStatsPage(self):
    self.navBar.parentView.showPage("StatisticsPage")
    self.setFocusedIcon(self.navBar.btnStats)

  def showProfilePage(self):
    self.navBar.parentView.showPage("ProfilePage")
    self.setFocusedIcon(self.navBar.btnProfile)
    
  def showSearchPage(self):
    pass

  def showTrendPage(self):
    pass
  
  def showFriendsPage(self):
    pass
  
  def setFocusedIcon(self, focusedButton):
    for button in self.navBar.buttons:
      if button == focusedButton:
        button.setStyleSheet(self.navBar.focusedButtonStyleSheet)
      else:
        button.setStyleSheet(self.navBar.buttonStyleSheet)
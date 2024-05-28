from View.NavBar import NavBar

class ControllerNavBar:
  def __init__(self, navBar: NavBar):
    self.navBar = navBar

    self.navBar.btnProfile.clicked.connect(self.showProfilePage)
    self.navBar.btnSearch.clicked.connect(self.showSearchPage)
    self.navBar.btnTrend.clicked.connect(self.showTrendPage)
    self.navBar.btnFriends.clicked.connect(self.showFriendsPage)
    self.navBar.btnStats.clicked.connect(self.showStatsPage)
    self.navBar.btnReco.clicked.connect(self.showRecoPage)

  def showStatsPage(self):
    self.navBar.parentView.showPage("StatisticsPage")
    self.setFocusedIcon(self.navBar.btnStats)

  def showProfilePage(self):
    self.navBar.parentView.showPage("ProfilePage")
    self.setFocusedIcon(self.navBar.btnProfile)
    
  def showSearchPage(self):
    self.navBar.parentView.showPage("SearchPage")
    self.setFocusedIcon(self.navBar.btnSearch)
  
  def showRecoPage(self):
    self.navBar.parentView.showPage("RecommendationPage")
    self.setFocusedIcon(self.navBar.btnReco)

  def showTrendPage(self):
    self.navBar.parentView.showPage("TrendingPage")
    self.setFocusedIcon(self.navBar.btnTrend)
  
  def showFriendsPage(self):
    self.navBar.parentView.showPage("FriendsPage")
    self.setFocusedIcon(self.navBar.btnFriends)
  
  def setFocusedIcon(self, focusedButton):
    for button in self.navBar.buttons:
      if button == focusedButton:
        button.setStyleSheet(self.navBar.focusedButtonStyleSheet)
      else:
        button.setStyleSheet(self.navBar.buttonStyleSheet)
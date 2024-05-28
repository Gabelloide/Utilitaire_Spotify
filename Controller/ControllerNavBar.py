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

  def showProfilePage(self):
    self.navBar.parentView.showPage("ProfilePage")
    
  def showSearchPage(self):
    pass

  def showTrendPage(self):
    pass
  
  def showFriendsPage(self):
    pass
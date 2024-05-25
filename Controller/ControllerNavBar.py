class ControllerNavBar:
    def __init__(self, navBar):
        self.navBar = navBar

        self.navBar.btnProfile.clicked.connect(self.showProfilePage)
        self.navBar.btnSearch.clicked.connect(self.showSearchPage)
        self.navBar.btnTrend.clicked.connect(self.showTrendPage)
        self.navBar.btnFriends.clicked.connect(self.showFriendsPage)

    """
    def showProfilePage(self):
        #TODO 

    def showSearchPage(self):
        #TODO 

    def showTrendPage(self):
        #TODO 

    def showFriendsPage(self):
        #TODO 
    """
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import os
import random
import win32gui

# I recommend running the project firstly and creating your own whiteList after the update() function finishes, using the output given after a complete run.
# Must have window in background/foreground, not minimized.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Instagram:
    driverPath = "chromedriver.exe"
    followerList, followingList = [], []

    with open('whiteList.txt') as f:
        whiteList = f.read().splitlines()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(Instagram.driverPath)

        self.browser.get("https://www.instagram.com/")
        time.sleep(3)

        # Minimizing screen size.
        chrome = win32gui.FindWindow(None, 'Instagram - Google Chrome')

        # Getting Window Coords/Dimensions
        # x, y, x2, y2 = win32gui.GetWindowRect(chrome)
        # w = x - x2 # width
        # h = y - y2 # height

        x = 10
        y = 10
        w = 516
        h = 531

        win32gui.MoveWindow(chrome, x, y, w, h, True)

    def signIn(self):

        usernameTextBox = self.browser.find_element_by_name("username")
        passwordTextBox = self.browser.find_element_by_name("password")
        usernameTextBox.send_keys(username)
        passwordTextBox.send_keys(password)
        passwordTextBox.send_keys(Keys.ENTER)
        time.sleep(5)

    def getFollowers(self):
        
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(3)
        # to get # of followers, take string from xpath and convert to int
        # Just easier to copy regular xpath from Firefox inspector (Chromedriver won't show/return correct pathing.)
        # In case testing without being logged in
        # header/section not included in 
        try:
            self.browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div/div/button/span").click()
        except:
            print("Log in banner not found. Moving on...")
            
        self.following = self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/ul/li[2]").text.split()[0]
        
        # string literal contains comma
        self.following = int(self.following.replace(',', ''))
        # click followers list
        self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/ul/li[2]").click()
        time.sleep(3)

        scroll = self.browser.find_element_by_xpath("/html/body/div[4]/div")
        # css_selector sometimes errors when browser is smaller.
        # scroll = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        count = len(scroll.find_elements_by_tag_name("li"))
        hoverOver = self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[1]")

        action = webdriver.ActionChains(self.browser)
        # Must prevent random following.
        # Hangs after first click
        clickTwice = 0
        # Count ends up being sub 1 following total.
        while count+1 < self.following:
            if clickTwice < 2:
                # Errors in smallest window size - mouse in middle of screen - move from over names to "Followers banner".
                action.move_to_element(hoverOver).perform()
                scroll.click()
                clickTwice = clickTwice + 1
                action.move_to_element(hoverOver).perform()

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            count = len(scroll.find_elements_by_tag_name("li"))

        followers = self.browser.find_element_by_class_name("PZuss").find_elements_by_tag_name("li")

        # Grabs username of individuals from href
        for user in followers:
            link = str(user.find_element_by_tag_name("a").get_attribute("href"))
            link = link.split("/")
            self.followerList.append(link[3])

    def getFollowing(self):

        # Same as getFollowers, except using li[3], instead of li[2]
        self.browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3,5))

        self.followers = self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/ul/li[3]").text.split()[0]
        self.followers = int(self.followers.replace(',', ''))
        self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/ul/li[3]").click()
        time.sleep(3)

        scroll = self.browser.find_element_by_xpath("/html/body/div[4]/div")
        # css_selector sometimes errors when browser is smaller.
        # scroll = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        count = len(scroll.find_elements_by_tag_name("li"))
        hoverOver = self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[1]")

        action = webdriver.ActionChains(self.browser)
        clickTwice = 0
        while count < self.followers:
            if clickTwice < 2:
                action.move_to_element(hoverOver).perform()
                scroll.click()
                clickTwice = clickTwice + 1
                action.move_to_element(hoverOver).perform()

            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            count = len(scroll.find_elements_by_tag_name("li"))

        followings = self.browser.find_element_by_class_name("PZuss").find_elements_by_tag_name("li")

        for user in followings:
            link = str(user.find_element_by_tag_name("a").get_attribute("href"))
            link = link.split("/")
            self.followingList.append(link[3])

    def update(self):

        self.getFollowers()
        self.getFollowing()

        unfollowers = []

        for unfollower in self.followingList:
            if unfollower not in self.followerList and unfollower not in self.whiteList:
                print(unfollower)
                unfollowers.append(unfollower)

        print("*************")
        print(f"{str(len(unfollowers))} to be unfollowed back. ")
        print("Updating unfollower list...")

        # Replace data.
        try:
            with open('unfollowers.txt', "r") as f:
                data = f.read()
        except:
            print("No file found. I can create one however.")

        with open('unfollowers.txt', 'w') as f:
            for unfollower in unfollowers:
                f.write('%s\n' % unfollower)
        print("Update complete.")
        print("*************")

    def unfollow(self):

        with open('unfollowers.txt') as f:
            unfollowers = f.read().splitlines()

        unfollowed = []
    
        for unfollower in unfollowers:
            if len(unfollowed) == 60:
                # Sleep an additional mins to be safe.
                time.sleep(300)
                print("Napping for 5 mins, ZZZ.")

            self.browser.get(f"https://www.instagram.com/{unfollower}/")
            time.sleep(3) 

            # In case unfollower list is outdated.
            try:
                checkFollow = self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/div/div/div[2]/div/span/span[1]/button/div/span").get_attribute("aria-label") 

            except:
                print(f"Skipping {unfollower}, because following status not found.")
                checkFollow = ""

            if (checkFollow == "Following"):
                # Following Button
                self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/div/div/div[2]/div/span/span[1]/button").click()
                time.sleep(1)
                # Confirm Unfollow 
                self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[1]").click()
                unfollowed.append(unfollower)
                # Based on guideline: 60/hr, 25-30 sec in between unfollows. Let's just do ~1unf/min
                print(f"{unfollower} unfollowed.")
                time.sleep(random.randrange(50,60))
        
        print("*************")
        print(f"Unfollowed a total of {len(unfollowed)} accounts:")
        for unfollower in unfollowed:
            print(unfollower)

        print("*************")
        print("Purge complete! Updating unfollowers list...")
        print("*************")

        self.update()

    def __del__(self):
        time.sleep(2)
        self.browser.close()

# I don't plan to have an import version.
if __name__ == "__main__":
    updateUnfollowers = True

    # Replace
    username = "*****"
    password = "*****"
    follower = 0
    following = 0

    app = Instagram(username, password)
    
    app.signIn()

    # In case there have been drastic change to ratio.
    if updateUnfollowers:
        app.update()
        app.unfollow()
    # Otherwise, run from existing unfollower list.
    else:
        app.unfollow()

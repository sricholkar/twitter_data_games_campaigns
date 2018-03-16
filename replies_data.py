from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import pymysql.cursors
#from xvfbwrapper import Xvfb

# =============================================================================
# display = Xvfb()
# display.start()
# 
# =============================================================================
#profiles = ["BlackRiddles", "InterabangEnt", "virgovszodiac", "retroepic", "buddysystemla","popcannibal", "TeamGotham", "Mobius_Games", 
#            "Phoenix_Point", "Inxile_Ent", "WorldofEternity", "JotunGame", "KingdomsCastles", "2ndStudioAni",
#            "OwlcatGames", "Snapshot_Games", "BannerSaga", "failbettergames"]

#profiles = ["InterabangEnt", "virgovszodiac", "retroepic", "buddysystemla", "TeamGotham", "Mobius_Games", 
#            "Phoenix_Point", "Inxile_Ent", "WorldofEternity", "popcannibal", "OwlcatGames", "Snapshot_Games", "BannerSaga", "failbettergames"]

profiles = ["explodingkittens", "zungle", "baubax", "lifeonpurple", "starcitizen", "bragi", "sondorsebike", "gloomhaven", "oculusrift", "picobrewbeer", 
 					"fidgetcube", "getsequent", "hyper", "vmullerdesigner", "livwatches", "ridehelix", "gramovox", "teamkano", "elevationlab", "korindesign", 
 					"getbetterback", "pebble", "oculusrift", "pono", "worldofeternity", "theveronicamarsmovie", "lifeonpurple", "shenmue_3"]
def connection():
		conn = pymysql.connect(host="localhost", user="root", password="1234", db="twitter", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
		return conn

def createTable(profile, cnxn):
		cursor = cnxn.cursor()
		cursor.execute('DROP TABLE IF EXISTS ' + profile) #or die(mysql_error());
		print("Creating a table " + profile.upper())
		cursor.execute("CREATE TABLE "+ profile +" (id int PRIMARY KEY AUTO_INCREMENT, user varchar(500), num varchar(32), tweet varchar(500))")
		cnxn.commit()
		print(profile.upper() + " table created Successfully")

##commits the given query
def commit(cnxn):
    cnxn.commit()
    print("committed")

	##closes connection to database
def closeCon(cnxn):
	cnxn.close()
	print("Connection Successfully Closed!")

    


def window_scroll(profile, cnxn, last_height=0):
    try:
        browser.execute_script("window.scroll(0, document.body.scrollHeight);")
        new_height = browser.execute_script("return document.body.scrollHeight")
        time.sleep(3)
        print(str(last_height))
        if (last_height == new_height):
            print("End of Scroll")
            raise Exception("End of Scroll")
        else:
            print(str(new_height))
            last_height = new_height
            window_scroll(profile, cnxn, last_height)
    except Exception:
        ol_tag = browser.find_elements(By.XPATH, "//div[@class='stream']/ol[@id='stream-items-id']/li")
        unique_tweet_ids = []
        for i in range(1, len(ol_tag)+1):
            if (browser.find_element(By.XPATH, "//div[@class='stream']/ol[@id='stream-items-id']/li[" + str(i)+"]/div").get_attribute("data-screen-name") == profile):
                i = browser.find_element(By.XPATH, "//div[@class='stream']/ol[@id='stream-items-id']/li[" + str(i)+"]")
                tweet_id_ = i.get_attribute("id")
                tweet_id = tweet_id_.split("-")[3]
                unique_tweet_ids.append(tweet_id)
        collect_replies(profile, cnxn, unique_tweet_ids)
        print(len(ol_tag))
        closeCon(cnxn)

##inserts tweets into the MySQL database sequentuelly with time
def insert(profile, cnxn, user, num, tweet):
    print("In insert method")
#    print(profile + " " + user + " " + str(num) + " "  + tweet)
    query = "INSERT INTO " + profile + " (user, num, tweet) VALUES (%s, %s, %s)"
    cursor = cnxn.cursor()
    cursor.execute(query, (user, num, tweet.encode('utf8')))
#    print("/")
    commit(cnxn)
    
def collect_replies(profile, cnxn, list_of_ids):
#    print(list_of_ids)
#    print(len(list_of_ids))
    browser.get(twitter_url + "/status/")
    for tweet_id in list_of_ids:
        browser.get(twitter_url + "/status/" + str(tweet_id))
        update = "//div[@role='main']/div[1]/div/div[2]/p"
        try:
            browser.find_element_by_xpath(update)
        except NoSuchElementException:
            continue
        users = browser.find_elements(By.XPATH, "//div[@class='content']/div[@class='stream-item-header']/a/span[@class='username u-dir u-textTruncate']")
        replies = browser.find_elements(By.XPATH, "//div[@class='js-tweet-text-container']/p")
        userrs = []
        userrs.append(browser.find_element(By.XPATH, "//div[@class='content clearfix']/div[@class='permalink-header']/a/span[@class='username u-dir u-textTruncate']"))
        for user in users:
            if  not (user.text):
                continue
            userrs.append(user)
        for i, user, reply in zip(range(0,len(userrs)), userrs, replies):
#            print(profile + " " + str(i) + " " + user.text.strip() + " / " + reply.text)
            insert(profile, cnxn, user.text.strip(), str(i), reply.text)
    
for profile in profiles:
    cnxn = connection()
    createTable(profile, cnxn)
    twitter_url = "https://twitter.com/" + profile
#    browser = webdriver.Firefox("C:\Firefox Driver")
    browser = webdriver.PhantomJS(executable_path=r"C:\phantomjs\bin\phantomjs.exe")
    browser.get(twitter_url)
    window_scroll(profile, cnxn)
    browser.quit()
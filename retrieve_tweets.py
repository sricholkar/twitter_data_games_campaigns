# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 04:11:32 2018

@author: Srivardhan
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time, re
import pymysql.cursors


    
##establishes connection
def connection():
		conn = pymysql.connect(host="localhost", user="root", password="1234", db="twitter", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
		return conn

##commits the given query
def commit(cnxn):
	cnxn.commit()

##closes connection to database
def closeCon(cnxn):
	cnxn.close()
	print("Connection Successfully Closed!")

def retrieveTweets(campaign):
    query = "Select id, user, num, tweet from "+ campaign
    con = connection()
    cursor = con.cursor()
    cursor.execute(query)
    tweets_info = cursor.fetchall()
    commit(con)
    closeCon(con)
#    num_of_tweets = len(tweets_info) + 1
    with open("Data/" + campaign + "_tweets.txt", "a", encoding="UTF-8") as camp:
        for tweet in tweets_info:
            camp.write(str(tweet['id']) + "§" + tweet['user'] + "§" + str(tweet['num']) + "§" + tweet['tweet'] + "\n")

campaign_twitter_profiles= ["InterabangEnt", "virgovszodiac", "retroepic", "buddysystemla", "TeamGotham", "Mobius_Games", 
            "Phoenix_Point", "Inxile_Ent", "WorldofEternity", "popcannibal", "OwlcatGames", "Snapshot_Games", "BannerSaga", "failbettergames"]

for campaign in campaign_twitter_profiles:
	# campaign = ''.join(e for e in campaign if e.isalnum())
    retrieveTweets(campaign)
# =============================================================================
# 		for num, tweet in zip(range(1,num_of_tweets),tweets_info):
# 			print(str(num) + "," +tweet['tweets'] + "\n")
# 			camp.write(str(num) + "," +tweet['tweets'] + "\n")
# =============================================================================
	 


# =============================================================================
# campaigns_twitter_profile = ["antoniasaintny", 'baubax', 'bragi', "brydgekeyboards", "coolestcooler", "edgeofbelgravia", "elevationlab", "emotiv", "explodingkittens", "fidgetcube", "getbetterback", "getbetterback", 
# 	"getsequent", "giflybike", "gloomhaven", "glowheadphones", "gramovox", "g_rotogether", "hellobragi",
# 	"hickies", "ikamper_inc", "junosmartmirror", "korindesign", "lifeonpurple", "livwatches", "nebia",
# 	"noriacool", "northaware", "oculusrift", "pebble", "picobrewbeer", "pono", "ridehelix", "shenmue_3",
# 	"sleepkokoon", "sondorsebike", "starcitizen", "tagabikes", "teamkano", "theveronicamarsmovie", "vmullerdesigner",
# 	"worldofeternity", "zungle"]
# =============================================================================



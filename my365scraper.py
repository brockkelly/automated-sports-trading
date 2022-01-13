from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt
import time
import pandas as pd

SPORT = "Basketball"
LEAGUE = "NBA"
MARKET = "Game Lines"

web = 'https://www.bet365.com/'
path = '/Users/brockkelly/Desktop/Personal Projects/chromedriver'

driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window() #Headless = False
time.sleep(5) #add implicit wait, if necessary

# Choose Sport

# grab table of sports
try:
    sports = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wn-PreMatchGroup"))
    )
    sport = sports.find_elements_by_class_name("wn-PreMatchItem")

except:
    driver.quit()

# clicks link for that sport
for link in sport:
    if link.text == SPORT:
        link.click()
        break


# Choose League and Bet
# grabs table of leagues
try:
    
    leagues = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sm-SplashModule"))
    )

    open_tabs = leagues.find_elements_by_xpath("//*[contains(text(), 'Game Lines')]")
    league = leagues.find_elements_by_class_name("sm-SplashMarketGroupButton_Text")

    # iterate over links and make sure they are all closed
    # find open tabs
    for open in open_tabs:
        grandparent1 = open.find_element_by_xpath('../..')
        grandparent2 = grandparent1.find_element_by_xpath('../..')
        grandparent3 = grandparent2.find_element_by_xpath('../..')
        child = grandparent3.find_element_by_class_name("sm-SplashMarketGroupButton_Text")
        child.click()

    time.sleep(3)

    for link in league:

        if link.text == LEAGUE:
            
            link.click()
            time.sleep(1)
            parent = link.find_element_by_xpath('./..')
            grandparent = parent.find_element_by_xpath('./..')
            markets = grandparent.find_elements_by_class_name("sm-CouponLink_Title")
            break

    for market in markets:
        if market.text == MARKET:
            market.click()
            break

except:
    driver.quit()

# grabs table of odds data
try:

    total = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "gl-MarketGroupContainer"))
    )

except:
    driver.quit()

# defining empty lists for data
teams = []
handicaps = []
odds = []
moneylines = []
times = []

# subsetting whole table for individual types of bets and teams
all_livetimes = total.find_elements_by_class_name("pi-CouponParticipantClockInPlay_GameTimerWrapper")
all_teams = total.find_elements_by_class_name("scb-ParticipantFixtureDetailsHigherBasketball_Team ")
all_handicaps = total.find_elements_by_class_name("sac-ParticipantCenteredStacked50OTB_Handicap")
all_odds = total.find_elements_by_class_name("sac-ParticipantCenteredStacked50OTB_Odds")
all_moneylines = total.find_elements_by_class_name("sac-ParticipantOddsOnly50OTB_Odds")
all_times = total.find_elements_by_class_name("scb-ParticipantFixtureDetailsHigherBasketball_BookCloses ")
islive = []

#filling lists
for team in all_teams:
    teams.append(team.text)

for handicap in all_handicaps:
    handicaps.append(handicap.text)

for odd in all_odds:   
    odds.append(odd.text)

for moneyline in all_moneylines:
    moneylines.append(moneyline.text)

for ltime in all_livetimes:
    times.append(ltime.text)
    islive.append("live")

for ttime in all_times:
    times.append(ttime.text)
    islive.append("upcoming")

# cleaning this data

# need to split handicap, odds data in half
middle_index = len(handicaps)//2

spread_odds = odds[:middle_index]
total_odds = odds[middle_index:]

# need to split data for home and away
home_teams = teams[::2]
away_teams = teams[1::2]
spread_odds_home = spread_odds[::2]
spread_odds_away = spread_odds[1::2]

moneylines_home = moneylines[::2]
moneylines_away = moneylines[1::2]

# creaing a dictionary to store lists
dict_gambling = {'home': home_teams, 'away': away_teams, 'time': times, "status":islive, "money_home":moneylines_home,"money_away":moneylines_away, 'odds_home': spread_odds_home, 'odds_away': spread_odds_away}

#Presenting data in dataframe
df_gambling = pd.DataFrame.from_dict(dict_gambling)
print(df_gambling)

while(True):
    pass
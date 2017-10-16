#! /usr/bin/env python

import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import smtplib
import unittest
import time
import re

class fntsyLu(unittest.TestCase):
	# Sets up the chrome driver
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.get("http://www.espn.com/fantasy/basketball/")
	
	# Method to return the row number of the player 
	def getNumber(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		elements = driver.find_elements_by_class_name("playerEditSlot")
		str = elements[num].get_attribute('id')
		playerNum = re.findall('\d+', str)
		return playerNum[0]
	
	# Returns the list of positions of a player
	def getPosition(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		str = "playername_" + playerList[num]
		playerPositionText = "//*[@id=" + '\'' + str + '\'' + "]"
		playerPositionTextElement = wait.until(lambda driver:driver.find_element_by_xpath(playerPositionText))
		playerHTML = playerPositionTextElement.get_attribute('innerHTML')
		positions = re.findall('PG|SG|SF|PF|\sC\s|C\s|;C', playerHTML)
		return positions

	# Checks if a player has a game scheduled for today
	def hasGame(self, str):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		hasGame = True
		try:
			wait.until(lambda driver:driver.find_element_by_xpath(str))
		except TimeoutException:
			hasGame = False
			return hasGame

		return hasGame

	# Returns the player's name
	def getName(self, str):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		nameElement = wait.until(lambda driver: driver.find_element_by_xpath(str))
		name = nameElement.get_attribute('text')
		return name

	# Returns the owner of the team's name
	def getOwnerName(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		ownerNameElement = wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div/div[3]/div[1]/div[2]/div[1]/ul[2]/li[1]'))
		ownerNameHTML = ownerNameElement.get_attribute('outerHTML')
		ownerName = ownerNameHTML.split('>', 1)[1].split('<', 1)[0].split(' ', 1)[0]
		return ownerName

	# Returns name of the team
	def getTeamName(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		teamNameElement = wait.until(lambda driver: driver.find_element_by_class_name('team-name'))
		teamNameHTML = teamNameElement.get_attribute('innerHTML')
		teamName = teamNameHTML.split('<e', 1)[0]
		teamName.replace(' ', '')
		return teamName

	# Returns league name
	def getLeagueName(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		leagueNameElement = wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div/div[3]/div[1]/div[2]/div[1]/ul[1]/li/a'))
		leagueNameHTML = leagueNameElement.get_attribute('innerHTML')
		leagueName = leagueNameHTML.split('<strong>', 1)[1].split('</strong>', 1)[0]
		return leagueName

	# Checks is row 13 is an Injury-Reserve row. 
	def checkRow13(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		try:
			ir = '//*[@id="pncSlot_13"]'
			irElement = wait.until(lambda driver : driver.find_element_by_xpath(ir))
			irHTML = irElement.get_attribute('outerHTML')
			findIR = re.findall('IR', irHTML)
			if len(findIR) > 0:
				return True
		except TimeoutException:
			return False 
		return False

	# Returns the num of rows. Will most likely return 13, but if there are more than 3 players on the bench the number will
	# always be greater than 13. This method was created to account for the adding/dropping of players because your lineup
	# is affected in the future if you add/drop a player
	def getNumOfRows(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		rows = wait.until(lambda driver: driver.find_elements_by_class_name("playerEditSlot"))
		if(len(rows) - 1 == 14) and self.checkRow13():
			return len(rows) - 2
		else:
			pass
		return len(rows) - 1

	# Sets the player list in the order that the page was loaded.
	def setPlayerList(self):
		driver = self.driver
		elements = driver.find_elements_by_class_name("playertablePlayerName")
		playerHTML = ""
		for i in range(0, len(elements)):
			playerHTML += elements[i].get_attribute('id')

		digits = re.findall('\d+', playerHTML)
		global playerList
		playerList = []
		for d in range(0, len(digits), 1):
			playerList.insert(d, digits[d])  
	
	# Returns a list of players who are on the bench AND have a game scheduled.			
	def getBenchList(self):
		self.setPlayerList()
		benchPlayerList = []
		benchPlayerGameStatuses = []
		count = 0
		for i in range(10, 13, 1):
			str = "pncPlayerRow_" + self.getNumber(i)
			playerGameStatus = "//*[@id=" + "\'" + str + "\'" + "]/td[6]/a"
			benchPlayerGameStatuses.insert(count, self.hasGame(playerGameStatus))
			if self.getNumOfRows() > 13:
				x = self.getNumOfRows() - 13
				num = i - x
			else:
				num = i
			playerName = "//*[@id=" + '\'' + 'playername_' + playerList[num] + '\'' + ']/a[1]'
			newsXPath = "'//*[@id=" '\'' + "playername_" + playerList[num] + '\'' + "]/a[2]/img"
			if benchPlayerGameStatuses[count] == True:
				if not self.hasGame(newsXPath):
					benchPlayerList.insert(count, self.getName(playerName))
				else:
					playerName = "//*[@id=" + '\'' + 'playername_' + playerList[num] + '\'' + ']/a'
					benchPlayerList.insert(count, self.getName(playerName))
			count += 1;
		return benchPlayerList

	# Sends email notifiying user that the script was unable to add players with games scheduled to the starting lineup
	def sendEmail(self, players):
		emailServer = smtplib.SMTP('smtp.gmail.com', 587)
		emailServer.ehlo()
		emailServer.starttls()
		email = ""   		# Insert email you created here
		password = "" 		# Insert password for email here
		recipientEmail = "" # Insert your personal email here
		emailServer.login(email, password)
		emailBody = emailBody = '\nHey ' + self.getOwnerName() + ', there was an issue with setting your lineup for ' + self.getTeamName() + '. Could not get ' + str(len(players)) + ' player into your starting lineup even though he has a game.'
		if len(players) > 1:
			emailBody = '\nHey ' + self.getOwnerName() + ', there was an issue with setting your lineup for ' + self.getTeamName() + '. Could not get ' + str(len(players)) + ' players into your starting lineup even though they have games.'
		emailServer.sendmail(email, recipientEmail,
			'Subject: FANTASY LINEUP ISSUE in ' + self.getLeagueName() + '\n' + emailBody)
		emailServer.quit()

	def sendErrorEmail(self):
		emailServer = smtplib.SMTP('smtp.gmail.com', 587)
		emailServer.ehlo()
		emailServer.starttls()
		email = ""   			      # Insert email you created here
		password = ""				  		  # Insert password for email here
		recipientEmail = "" # Insert your personal email here
		emailServer.login(email, password)
		emailBody = "\nThere was an error in the script. Unable to set your line up."
		emailServer.sendmail(email, recipientEmail, 'Subject: SCRIPT ERROR in ' + self.getLeagueName() + '\n' + emailBody)
		emailServer.quit()

	# Checks if the here button was clicked and a player's move to the starting lineup was finalized. If not, the player's move button
	# is reclicked and stays put.
	def clickHereOnPosition(self, num, num2, count):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		rowGameStatus = "pncPlayerRow_" + self.getNumber(num)
		rowGameStatusStr = "//*[@id=" + "\'" + rowGameStatus + "\'" + "]/td[6]/a"
		if self.hasGame(rowGameStatusStr):
			positionList = self.getPosition(num2)
			if num == 0 or num == 1:
				return self.clickHereOnPosition(5, num2, count)
			elif num == 2 or num == 3:
				return self.clickHereOnPosition(6, num2, count)
			elif num > 3 and count == len(positionList):
				str = "pncButtonMoveSelected_" + playerList[num2]
				moveButton = "//*[@id=" + '\'' + str + '\'' + "]"
				moveButtonElement = wait.until(lambda driver: driver.find_element_by_xpath(moveButton))
				moveButtonElement.click()
				return False
			return False
		else:
			str = "pncButtonHere_" + self.getNumber(num)
			position = "//*[@id=" + '\'' + str + '\'' + "]"
			positionButton = wait.until(lambda driver:driver.find_element_by_xpath(position))
			positionButton.click()
			return True
		return False

	# Checks if a player has been moved to a row corresponding to his position. 
	def toPosition(self, positionList, num):
		count = 0
		for i in range(0, len(positionList), 1):
			count += 1
			if positionList[i] == "PG":
				if self.clickHereOnPosition(0, num, count):
					return True
				else: 
					pass
			elif positionList[i] == "SG":
				if self.clickHereOnPosition(1, num, count):
					return True
				else: 
					pass
			elif positionList[i] == "SF":
				if self.clickHereOnPosition(2, num, count):
					return True
				else:
					pass
			elif positionList[i] == "PF":
				if self.clickHereOnPosition(3, num, count):
					return True
				else:
					pass
			elif positionList[i] == "C" or positionList[i] == ";C":
				if self.clickHereOnPosition(4, num, count):
					return True
				else: 
					pass
		return False

	# If player could not be moved into one of the UTIL rows, a player is moved to the starting lineup. This method initializes
	# a player's position list and checks each row corresponding to his positions.
	def toSL(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		positionList = self.getPosition(num)
		return self.toPosition(positionList, num)

	# Clicks the 'here' buttons and finalizes that the player is moved into the starting lineup.
	def clickHereOnUtil(self, str, str2, num, num2):
		driver = self.driver 
		wait = WebDriverWait(driver, 10)
		if self.hasGame(str):
			if num2 == 9 and len(self.getBenchList()) > 0:
				return self.toSL(num)
		else:
			buttonElement = wait.until(lambda driver: driver.find_element_by_xpath(str2))
			buttonElement.click()
			return True
		return False

	# Initialized strings for selenium to find the options a player could be moved to, the 'here' buttons.
	def initializeHereStrings(self, num):
		stringList = []
		playerRow = "pncPlayerRow_" + self.getNumber(num)
		playerRowGameStatus = "//*[@id=" + '\'' + playerRow + '\'' + "]/td[6]/a"
		here = "pncButtonHere_" + self.getNumber(num)
		playerRowButton = "//*[@id=" + '\'' + here + '\'' + "]"
		stringList = [playerRowGameStatus, playerRowButton]
		return stringList

	# Moves player to the UTIL 
	def toUtil(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		for i in range(7, 10, 1):
			utilHereStrings = self.initializeHereStrings(i)
			if self.clickHereOnUtil(utilHereStrings[0], utilHereStrings[1], num, i):
				return
			else:
				pass
		return

	# Initializes the strings in order for selenium the find the web element for a player's move button. 
	def initializeMoveStrings(self, num, num2):
		stringList = []
		playerRow = "pncPlayerRow_" + self.getNumber(num)
		playerRowGameStatus = "//*[@id=" + '\'' + playerRow + '\'' + "]/td[6]/a"
		move = "pncButtonMove_" + playerList[num2]
		playerRowButton = "//*[@id=" + '\'' + move + '\'' + "]"
		stringList = [playerRowGameStatus, playerRowButton]
		return stringList

	# Clicks the player's move button 
	def movePlayer(self, str, str2, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		if self.hasGame(str):
			buttonElement = wait.until(lambda driver: driver.find_element_by_xpath(str2))
			buttonElement.click()
			if self.getNumOfRows() > 13 and num > self.getNumOfRows() - 13:
				self.toUtil(num)
			elif num > 9:
				self.toUtil(num)
			else:
				self.toSL(num)
		else:
			pass

	# Clicks the submit lineup button. 
	def submitLineUp(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		submit = "//*[@id='pncSaveRoster0']"
		submitElement = wait.until(lambda driver: driver.find_element_by_xpath(submit))
		submitElement.click()
		time.sleep(2)
		self.setPlayerList()

	# Checks the bench and sees if there are players with games scheduled.
	def checkBench(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		for i in range(10, self.getNumOfRows(), 1):
			if self.getNumOfRows() > 13:
				x = self.getNumOfRows() - 13
				num = i - x
			else:
				num = i
			rowStrings = self.initializeMoveStrings(i, num)
			self.movePlayer(rowStrings[0], rowStrings[1], num)

	# Checks the three UTIL rows to see if they could be moved into the starting lineup. 
	def checkUtil(self):
		self.submitLineUp()
		for i in range(7, 10, 1):
			num = i
			utilStrings = self.initializeMoveStrings(i, i)
			self.movePlayer(utilStrings[0], utilStrings[1], num)
		self.checkBench()

	# Clicks login button on ESPN Fantasy homepage and inserts your account info.
	def login(self):
		# initialize variables
		driver = self.driver
		username = "" 							# Insert your username here
		password = ""							# Insert your password here
		wait = WebDriverWait(driver, 10)

		# click Log In button
		loginButtonXpath = "//*[@id='global-header']/div[2]/ul/li[2]/a"
		loginButtonElement1 = wait.until(lambda driver: driver.find_element_by_xpath(loginButtonXpath))
		loginButtonElement1.click()

		# find email and pass ID
		emailFieldID = "//*[@id='did-ui']/div/div/section/section/form/section/div[1]/div/label/span[2]/input"
		passFieldID = "//*[@id='did-ui']/div/div/section/section/form/section/div[2]/div/label/span[2]/input"
		
		# switch to frame so script can type
		driver.switch_to.frame("disneyid-iframe")
		
		# find email input box and type in email
		emailFieldElement = wait.until(lambda driver: driver.find_element_by_xpath(emailFieldID))
		emailFieldElement.click()
		emailFieldElement.clear()
		emailFieldElement.send_keys(username)

		# find pass input box and type in password
		passFieldElement = wait.until(lambda driver: driver.find_element_by_xpath(passFieldID))
		passFieldElement.click()
		passFieldElement.clear()
		passFieldElement.send_keys(password)
		
		# click log in button
		loginButtonXpath2 = "//*[@id='did-ui']/div/div/section/section/form/section/div[3]/button[2]"
		loginButtonElement2 = wait.until(lambda driver: driver.find_element_by_xpath(loginButtonXpath2))
		loginButtonElement2.click()

		leagueID = str(self.LEAGUEID)
		teamID = str(self.TEAMID)
		seasonID = str(self.SEASONID)
		leagueURL = "http://games.espn.com/fba/clubhouse?leagueId=" + leagueID + "&teamId=" + teamID + "&seasonId=" + seasonID
		print leagueURL
		time.sleep(4)
		driver.get(leagueURL)
		time.sleep(4)

	def tearDown(self):
		self.driver.quit()

	def test_main(self):
		self.login()
		time.sleep(2)
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		self.setPlayerList()
		self.checkBench()
		benchList = self.getBenchList()
		if len(benchList) > 0:
			self.setPlayerList()
			self.checkUtil()
			self.submitLineUp()
			newBenchList = self.getBenchList()
		else:
			pass


		if len(benchList) > 0:
			self.sendEmail(newBenchList)
		else:
			pass

		self.submitLineUp()
		time.sleep(2)
		self.tearDown()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		fntsyLu.SEASONID = sys.argv.pop()
		fntsyLu.TEAMID = sys.argv.pop()
		fntsyLu.LEAGUEID = sys.argv.pop()
	unittest.main()
		
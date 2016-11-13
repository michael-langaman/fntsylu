# fntsylu
ESPN Fantasy Basketball Daily Lineup Automator

This is my script to set my ESPN Fantasy Basketball lineup daily. Not fully automative as it does not add players off 
the bench and into the starting lineup if all the spots are taken, and of course, the players in those spots have games.
In that case, the script sends me an email with the names of the players who were unable to be added to the lineup. I could
implement that functionality but my implementation includes comparing the stats of the players. However, I do not trust stats,
as they do not really tell which player is better in my opinion. I'd rather just set the lineup myself. Another missing functionality you might wonder why I did not implement is the option to set your lineup for a certain amount of days. I did not include this functionality because the leagues that I am in are considered 'deep' which means it includes a lot of people (10+). For deep leagues, people constantly add/drop players, so including this functionality would not make sense as adding/dropping players affects your the setup of your lineup for future days as well. I am probably missing other functinonality as this was just a simple project for me to learn Python as its the first actual script I coded in Python. 

# How to use

First, you'll need to install:
 - google-chrome
 - selenium webdriver

Next, clone or download the repository and extract the fntsylu folder. Now, open up the fntsylu.py file in any text editor and edit the following"
'''python
 def login(self):
   driver = self.driver
   username = ""  # Insert your email here
   password = ""  # Insert your password
   wait = WebDriverWait(driver, 10)
   // rest of the code
'''
Before you edit this code, you'll need to create a gmail account that will notify you when there are players still on your bench. After you create the email, go back into the fntsylu.py file and edit the sendEmail function:
'''python
 def sendEmail(self, players):
   // some code ///
   email = ""          # Insert the email you just created
   password = ""       # Insert the password for the email you just created
   recipientEmail = "" # Insert the email you want to be notified (your personal email)
'''

Then go to your command line and change directory to said folder. Then type the following:
 > python fntsylu.py 'Insert league ID' 'Insert team id'
 
Chrome should open up and your lineup should be set.

# fntsylu
ESPN Fantasy Basketball Daily Lineup Automator

This is my script to set my ESPN Fantasy Basketball lineup daily. Not fully automative as it does not add players off 
the bench and into the starting lineup if all the spots are taken, and of course, the players in those spots have games.
In that case, the script sends me an email with the amount of players who were unable to be added to the lineup.

# How to use

First, you'll need to install:
 - google-chrome
 - selenium webdriver

Next, clone or download the repository and extract the fntsylu folder. Now, open up the fntsylu.py file in any text editor and edit the following:
```python
 def login(self):
   // some code //
   username = ""  # Insert your email here
   password = ""  # Insert your password
   // rest of the code //
```
Before you edit this code, you'll need to create a gmail account that will notify you when there are players still on your bench. After you create the email, go back into the fntsylu.py file and edit the sendEmail function:
```python
 def sendEmail(self, players):
   // some code ///
   email = ""          # Insert the email you just created
   password = ""       # Insert the password for the email you just created
   recipientEmail = "" # Insert the email you want to be notified (your personal email)
   // rest of the code //
```
Next, you'll need to know your league ID and team ID in order to enter the command to run the script. 

Here's an example of correct command:
 > python fntsylu.py 7609 18 2018

'7609' is the ID of the league that I want to enter. '18' is the team ID. You can find your league and team ID by reading the url of the homepage of your fantasy league.'2018' is just the current year. Once you find your league and team IDs, go to your command line and change directory to the fntsylu folder, then type the following:
 > python fntsylu.py 'Insert your league ID here' 'Insert your team ID here' 'Insert your season ID here (current year)'

Chrome should open up and the script should be setting your lineup

# Crontab

Next, you can set up cron to run the command for you. In the terminal, type 
 > crontab -e 

And enter the following at the bottom of the crontab file:
 > 0 11 * * * export DISPLAY=:0; /usr/bin/python /path/to/fntsylu.py 'insert league id' 'insert team id' 'insert season id'

For the example line above, cron will run the script every day at 11. 

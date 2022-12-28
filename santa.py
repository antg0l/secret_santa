import re
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variables
sender_address = 'email'
sender_pass = 'password'

names = []
emails = []
recipient = []
budget = 50

count = 0

# asks the for data entry method
print("""Welcome to the secret santa decision-maker! How would you like to enter the information?
   1. give a text (.txt) file with format of: name, email address
   2. manually enter information""")
   
x = 0
while(x == 0):
   try:
      option = int(input("Info entry method (1 or 2): "))
      if(option > 2 or option < 1):
         print("ERROR: You can only input 1 or 2!")
         print("""How would you like to enter the information?
            1. give a text (.txt) file
            2. manually enter information""") 
      else:
         x = 1
   except ValueError:
      print("ERROR: Please input 1 or 2!")
      print("""How would you like to enter the information?
      1. give a text (.txt) file
      2. manually enter information""")

# gets the number of participants
x = 0
while(x == 0):
   try:
      count = int(input("Enter number of participants: "))
      if(count < 2):
         print("ERROR: Number of participants must be 2 or more!")
      else:
         x = 1
   except ValueError:
      print("ERROR: Please input a valid integer number!")

# option 1: read the file (assumes file format is correct)
if(option == 1): 
   x = 0
   while(x == 0):
      filename = str(input("Name of text file (must end in .txt): "))
      if (filename[-4:] == '.txt'):
         x = 1 
      else:
         print("ERROR: Please input a file name which ends with .txt")
   text = open(filename, "r") 
   for i in range(0, count):
      info = text.readline().split(', ')
      names.append(info[0])
      emails.append(info[1])
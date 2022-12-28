import re
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variables
sender_address = 'antg0@yandex.ru'
sender_pass = 'thunder4yan'

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
      #if (info[1][-1] == '\n'):
      #   info[1] = info[1][:-1]
      emails.append(info[1])

possible_santa = names.copy()
print("possible_santa: ", possible_santa)

cont = 0

while(cont == 0):
    
    redo = False
    
    possible_santa = names.copy()
    
    for i in range(0, len(names)):
        recip = random.randint(0, len(possible_santa) - 1)
        x = 0
        while(x == 0):
            if(names[i] == possible_santa[recip]):
                if(len(possible_santa) == 1):
                    redo = True
                    x = 1
                else:
                    recip = random.randint(0, len(possible_santa) - 1)
            else:
                x = 1
        if(redo != True):
            recipient.append(possible_santa[recip])
            possible_santa.pop(recip)
            cont = 1
        else:
            cont = 0      

# this code must run for each name
for i in range(0, count):
    
    # the message which will be sent in the email
    mail_content = f'''Hello {names[i]},
    
You are the secret santa of {recipient[i]}!
    
Remember the budget is ${budget}
    '''
    
    # sets the email address the email will be sent to
    receiver_address = emails[i]
    
    # sets up the MIME
    message = MIMEMultipart()
    message['From'] = sender_address # your email address
    message['To'] = receiver_address # Secret Santa's email address
    message['Subject'] = 'Secret Santa' # subject of the 
    
    # sets the body of the mail
    message.attach(MIMEText(mail_content, 'plain'))
    
    # creates the SMTP session for sending the mail
    session = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    session.connect("smtp.yandex.ru", 465)
    session.ehlo()
    #session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
allocations = open("SantaAllocations.txt", "w+")

for i in range(0, len(names)):
    allocations.write(f'{names[i]} is the secret santa of {recipient[i]}\n')
    
allocations.close()             
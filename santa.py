import re
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class people:
   def __init__(self, name, family):
      self.name = name
      self.family = family

# Variables
sender_address = 'antg0@yandex.ru'
sender_pass = 'thunder4yan'

names = []
emails = []
family_flags = []
recipient = []
names_with_flags = []
possible_santa_i = []
budget = 50
count = 0
option = 1

# gets the number of participants
print("Welcome to the secret santa decision-maker!")
x = 0
while(x == 0):
   try:
      count = int(input("Please enter the number of participants: "))
      if(count < 2):
         print("ERROR: Number of participants must be 2 or more!")
      else:
         x = 1
   except ValueError:
      print("ERROR: Please input a valid integer number!")

# read the file (assumes file format is correct)
if(option == 1): 
   x = 0
   while(x == 0):
      print("Please enter the name of the text file with the information about participants.")
      print("Information must be formatted in the following way (each line): \"name, email, family code, \"")
      print("A family codes can be A, B, or any other. Participants with the same family code will not be secret santas for each other.")
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
      family_flags.append(info[2])
   for i in range(0, count):
      names_with_flags.append(people(names[i],family_flags[i]))      

cont = 0

# Sorting:
while(cont == 0):
    
    redo = False
    
    possible_santa = names_with_flags.copy()
    
    for i in range(0, len(names_with_flags)):
        #choose possible santas from other families:
        for j in range(0, len(possible_santa)):
            if (names_with_flags[i].family != possible_santa[j].family):
                possible_santa_i.append(possible_santa[j])
            
        if (len(possible_santa_i) == 0):
            redo = True
        elif (len(possible_santa_i) == 1):
            recip = 0 
        else:
            recip = random.randint(0, len(possible_santa_i) - 1)            

        if(redo != True):
            recipient.append(possible_santa_i[recip].name)            
            #delete chosen name from possible santa list
            for i in range(0, len(possible_santa)):
                if (possible_santa_i[recip].name == possible_santa[i].name):
                    possible_santa.pop(i)
                    break
            cont = 1
            #reset possible_santa_i list:
            possible_santa_i[:] = []
        else:
            print("Resorting...")
            cont = 0      

# Send a message for each participant:
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
    
#Also write allocations to text file
allocations = open("SantaAllocations.txt", "w+")

for i in range(0, len(names)):
    allocations.write(f'{names[i]} is the secret santa of {recipient[i]}\n')
    
allocations.close()             
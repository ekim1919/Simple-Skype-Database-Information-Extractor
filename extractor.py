#Author: Edward Kim
#Email: edbeta12@gmail.com

import optparse
import os
from subprocess import call
from database import *
from strmanipulation import *

#Extracts information about client 
#Fields: fullname of client, skypename of client, city and country of client. 
def ProfileExtractor(database):

    dbcon = ConnecttoDB(database)
    dbcon.execute("SELECT fullname, skypename, city, country, about  FROM Accounts;")

    textfile = open("Profile","w+")
       
    printtofile = getPrintFunction(textfile.write)

    printHeader("Account Information",printtofile)

    for row in dbcon:

        printtofile("Username: " + divbrack(str(row[0])) )
        printtofile("Skypename: " + divbrack(str(row[1])) )
        printtofile("City & country: " + divbrack(str(row[2])) + " , " + divbrack(str(row[3].upper())) )
        printtofile("About: " + divbrack(str(row[4])) )
     
    dbcon.close() #Close DB connections
    textfile.close()

#Extracts contacts from main.db
#Fields: displayname of contact, skypename of contact, phone number of contact, and timestamp of when last online. 
def ContactExtractor(database):

    dbcon = ConnecttoDB(database)
    dbcon.execute("SELECT displayname, skypename, phone_mobile, datetime(lastonline_timestamp, 'unixepoch'), about FROM contacts;")
    
    textfile = open("Contacts", "w+")

    printtofile = getPrintFunction(textfile.write)

    for row in dbcon:

        printHeader("Contact Found",printtofile)
        printtofile("User: " + divbrack(str(row[0])) )
        printtofile("Skypename: " + divbrack(str(row[1])) )

        if str(row[2]) != "None":
            printtofile("Phone Number: " + divbrack(str(row[2])) )

        printtofile("Last Online: " + str(row[3]) )

        if str(row[4]) != "" and row[4] != "None":
            printtofile("About Contact: " + str(row[4]) )
   
    dbcon.close() #Close DB connection
    textfile.close()

#Extracts all messages stored in main.db. 
#Fields: timestamp of message, whether the chat was received or sent, body_xml of message 
def MessageExtractor(database):

    dbcon = ConnecttoDB(database)
    dbcon.execute("SELECT datetime(timestamp,'unixepoch'), from_dispname, dialog_partner, author, chatname, body_xml FROM Messages;")

    textfile = open("Messages","w+")

    printtofile = getPrintFunction(textfile.write)

    for row in dbcon:

        if (str(row[2]) == str(row[3])) or (row[2] is None):
            chatdirection = " Sender: "+ str(row[1])
        else:
            chatdirection = " Sent to: " + str(row[2]) + " From " + str(row[1])

        printtofile(divbrack(str(row[0])) + chatdirection + " | " + GetChatName(str(row[4]),database)  + " | " + str(row[5]).replace("&apos;","'") )

    textfile.close()  # close file stream
    dbcon.close() #Close DB connection 

# Parses out all Phone Calls.
#Fields: Begin time, duration and members of the call or chat name. 
def PhoneExtractor(database):

    dbcon = ConnecttoDB(database)
    dbcon.execute("SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM Calls, Conversations WHERE calls.conv_dbid = conversations.id") 
   
    textfile = open("PhoneCalls", "w+")
    printtofile = getPrintFunction(textfile.write)
 
    for row in dbcon: 
        
        printHeader("Phone called",printtofile)
        printtofile("Beginning time " + divbrack(str(row[0])) )

        result = str(row[1])

        if result[0] == "#":
            printtofile("Call with: " + GetChatName(result, database))
            printtofile("Participants in Group: " + GetChatParticipants(result,database))

        else:
            printtofile("Call with: "  + result)      
        
    textfile.close()
    dbcon.close()
       
def main():
    #Options parser 
    parser = optparse.OptionParser("usage%prog " + "-p <skype profile path> ")

    parser.add_option('-p', dest='pathName', type='string',help="Type in path please")
    parser.add_option("-P", action="store_true", dest="Profile")
    parser.add_option("-C", action="store_true", dest="Contact")
    parser.add_option("-M", action="store_true", dest="Message")
    parser.add_option("-V", action ="store_true", dest="Phone")

    (options, args) = parser.parse_args()
    try:
        database = os.path.join(options.pathName, "main.db")
   
    except TypeError:
        print("Please type in arguments: Refer to the arguments manual included")

    if options.Profile:
        ProfileExtractor(database)
    if options.Contact:
        ContactExtractor(database)
    if options.Message:
        MessageExtractor(database)
    if options.Phone:
        PhoneExtractor(database)

if __name__ == "__main__":
    main()

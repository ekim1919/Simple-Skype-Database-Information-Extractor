#Author: Edward Kim
#Email: edbeta12@gmail.com

import optparse
import os 
from subprocess import call
from database import *
from strmanipulation import *

#Extracts information about client 
#Fields: fullname of client, skypename of client, city and country of client. 

brackstring = lambda column: divbrack(str(column)) 
opentextfile = lambda textfile: open(textfile,"w+")

def ProfileExtractor(database):

    dbcon = MakeConnection(database,"SELECT fullname, skypename, city, country, about FROM Accounts;")
       
    printtofile, stream = getPrintFunction(textfile("Profile"))

    printHeader("Account Information",printtofile)
    
    for row in dbcon:
        
        #bind to variables for readability 
        username,skypename,city,country,about = (row[i] for i in range(5)) 

        printtofile("Username: " + brackstring(username))
        printtofile("Skypename: " + brackstring(skypename))
        printtofile("City & country: " + brackstring(city) + " , " + brackstring(country.upper()) )
        printtofile("About: " + brackstring(about) )
     
    dbcon.close() #Close DB connections
    stream.close() #close file stream 

#Extracts contacts from main.db
#Fields: displayname of contact, skypename of contact, phone number of contact, and timestamp of when last online. 
def ContactExtractor(database):

    dbcon = MakeConnection(database,"SELECT displayname, skypename, phone_mobile, datetime(lastonline_timestamp, 'unixepoch'), about FROM contacts;")
    stream = opentextfile("Contacts")
    printtofile = getPrintFunction(stream)

    for row in dbcon:
          
        displayname,skypename,phone,lastonline,about = (row[i] for i in range(5)) #tuple generator for simplicity 
        
        printHeader("Contact Found",printtofile)
        printtofile("User: " + brackstring(displayname) )
        printtofile("Skypename: " + brackstring(skypename) )

        if str(row[2]) != "None":
            printtofile("Phone Number: " + brackstring(phone) )

        printtofile("Last Online: " + str(lastonline) )

        if str(about) != "" and about is not None:
            printtofile("About Contact: " + str(about) )
   
    dbcon.close() #Close DB connection
    stream.close() #close file stream

#Extracts all messages stored in main.db. 
#Fields: timestamp of message, whether the chat was received or sent, body_xml of message 
def MessageExtractor(database):

    dbcon = MakeConnection(database,"SELECT datetime(timestamp,'unixepoch'), from_dispname, dialog_partner, author, chatname, body_xml FROM Messages;")
    printfunction = {} #printfunction dictionary stores all print functions based on file streams 
    fileobjects = {} #file object dictioary keeps all of the file streams every unique chat. Key: Chatname Value: objects 
 
    for row in dbcon:
      
        timestamp, displayname, partner, author, chatname, message = (row[i] for i in range(6)) 
        ChatName = GetChatName(chatname,database)
        
        if ChatName not in fileobjects.keys(): #checks if Chatname has a file object associated with it. If not, open new file associtated with the Chatname 
            try:
                FileName = os.path.join(Chatsdirpath,ChatName) #Store files in Chats directory in current working directory (subject to change)
                fileobjects[ChatName] = opentextfile(FileName)
            except FileNotFoundError:
                print("Could not create file for" + ChatName) 
                
            printfunction[ChatName] = getPrintFunction(fileobjects[ChatName]) #make print function based on file object associated with Chatname

        if (str(partner) == str(author)) or (partner is None): # Checks message sender and receiver
            chatdirection = " Sender: "+ str(displayname)
        else:
            chatdirection = " Sent to: " + str(partner) + " From " + str(displayname)

        printtofile = printfunction[ChatName]
        printtofile(brackstring(timestamp) + chatdirection + " | " + str(message).replace("&apos;","'") )

    dbcon.close() #Close DB connection
    for stream in fileobjects: #close file streams 
        fileobjects[stream].close()

# Parses out all Phone Calls.
#Fields: Begin time, duration and members of the call or chat name. 
def PhoneExtractor(database):

    dbcon = MakeConnection(database,"SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM Calls, Conversations WHERE calls.conv_dbid = conversations.id") 
    stream = opentextfile("PhoneCalls")
    printtofile = getPrintFunction(stream)
 
    for row in dbcon: 
        
        begintime, callname = (row[i] for i in range(2))
        
        printHeader("Phone called",printtofile)
        printtofile("Beginning time " + brackstring(begintime) )

        result = str(callname)

        if result[0] == "#": # if first character is a '#', then that indicates a group call. Extract the name of the call with participant
            printtofile("Call with: " + GetChatName(result, database))
            printtofile("Participants in Group: " + GetChatParticipants(result,database))

        else:
            printtofile("Call with: "  + result)
        
    dbcon.close() #close database connection
    stream.close() #close file stream 
       
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
   
        if options.Profile:
            ProfileExtractor(database)
        if options.Contact:
            ContactExtractor(database)
        if options.Message:
            global Chatsdirpath 
            Chatsdirpath = os.path.join(os.getcwd(),"Chats")
            if not os.path.isdir(Chatsdirpath):
                os.mkdir(Chatsdirpath)
            MessageExtractor(database)
        if options.Phone:
            PhoneExtractor(database)
    except:
       
        print("An error has occured ")
        raise #For debugging purposes 

if __name__ == "__main__":
    main()

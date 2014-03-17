import sqlite3
from re import sub 
 
def MakeConnection(dbfile,command): 
    connection = sqlite3.connect(dbfile)
    cursor = connection.cursor()
    return cursor.execute(command) #returns the sqlite3 cursor after the execution of the sqlite command 

ChatCacheDictionary = {} #once friendly chat name is found, it is cached in this dictionary so further database connections are not necessary

def GetChatName(Chatname,dbfile):

    if Chatname not in ChatCacheDictionary.keys():
        
        dbcon = MakeConnection(dbfile, "SELECT friendlyname FROM Chats WHERE name= \"" + Chatname + "\" LIMIT 1")
        row = dbcon.fetchone()

        if row is None: #if no entry is found, the chat does not exist and thus labeled "Nonexistent Chat"
            ChatCacheDictionary[Chatname] = "Nonexistent Chat"
        else:
            ChatCacheDictionary[Chatname] = str(row[0])
            
        dbcon.close()        
    
    FoundName = sub("[/]","",ChatCacheDictionary[Chatname]) #replace any characters which will cause a FileNotFoundError in the built in open function 
    
    try:
        return FoundName[FoundName.rindex("|"):FoundName.rindex(",")+1] #Parses the chat name out
    
    except ValueError:
        return FoundName #if above parsing is illegal, return the value without any modifications 

def GetChatParticipants(Chatname, dbfile):

    dbcon = MakeConnection(dbfile, "SELECT participants FROM Chats WHERE name=\"" + Chatname + "\" LIMIT 1;")
    row = dbcon.fetchone()
    
    dbcon.close()
    return row[0] #returns participants 

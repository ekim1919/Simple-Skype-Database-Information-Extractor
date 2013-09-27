import sqlite3

ChatCacheDictionary = {} #caching chatnames once found for easy access

def ConnecttoDB(dbfile):
    connection = sqlite3.connect(dbfile)
    return connection.cursor()

def GetChatName(Chatname,dbfile):

    if Chatname not in ChatCacheDictionary.keys():
        dbcon = ConnecttoDB(dbfile)
        dbcon.execute("SELECT friendlyname FROM Chats WHERE name=\"" + Chatname + "\" LIMIT 1;")
        
        
        result = dbcon.fetchone()

        if result is None:
            ChatCacheDictionary[Chatname] = "Unknown Chat" 

        else:
            ChatCacheDictionary[Chatname] = result

        dbcon.close()        
    
    FoundName = ChatCacheDictionary[Chatname][0]
    try:
        return FoundName[FoundName.rindex("|"):FoundName.rindex(",")]
    
    except ValueError:
        return FoundName

def GetChatParticipants(Chatname, dbfile):

    dbcon = ConnecttoDB(dbfile)
    dbcon.execute("SELECT participants FROM Chats WHERE name=\"" + Chatname + "\" LIMIT 1;")

    for row in dbcon:
        return row[0]

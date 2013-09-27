#Enunciate the important information   
def divbrack(string):
    return "[ " + string + " ]"

#Print Header 
def printHeader(message, printtofile):
    printtofile("----------------------------" )
    printtofile(message)
    printtofile("----------------------------" )

def getPrintFunction(printstream):
    def printstring(string):
        printstream(string + "\n")
    return printstring

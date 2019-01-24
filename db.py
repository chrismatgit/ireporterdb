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
                self.db_name = 'da3ie1jp2ag7h8'
                self.user ='qczqujabhbhsev'
                self.host='ec2-54-235-68-3.compute-1.amazonaws.com'
                self.password='8cb120b890a130967951018fb17ea866304e3f6a9e980af5b84fe4ebd37377be'
                self.port = 5432

            self.connection = psycopg2.connect(dbname=self.db_name, user=self.user, host=self.host, password=self.password, port =self.port)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            pprint('Connected to the database '+ self.db_name +' successfully')


            create_user_table = "CREATE TABLE IF NOT EXISTS users (user_id SERIAL NOT NULL PRIMARY KEY,\
            firstname TEXT NOT NULL,\
             lastname TEXT NOT NULL, \
             othernames TEXT NOT NULL, \
             email TEXT NOT NULL, \
             phone_number TEXT NOT NULL, \
             username TEXT NOT NULL, \
             password TEXT NOT NULL, \
             registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
             isadmin BOOL DEFAULT FALSE);"
            self.cursor.execute(create_user_table)

            create_incident_table = "CREATE TABLE IF NOT EXISTS incidents (incident_id SERIAL NOT NULL PRIMARY KEY,\
            createdOn TEXT NOT NULL, \
            createdBy INT NOT NULL, \
            incType TEXT NOT NULL, \
            location TEXT NOT NULL, \
            status TEXT NOT NULL, \
            image TEXT NOT NULL, \
            video TEXT NOT NULL, \
            comment TEXT NOT NULL);"
            self.cursor.execute(create_incident_table)

            create_intervention_table = "CREATE TABLE IF NOT EXISTS interventions (intervention_id SERIAL NOT NULL PRIMARY KEY,\
            createdOn TEXT NOT NULL, \
            createdBy INT NOT NULL, \
            incType TEXT NOT NULL, \
            location TEXT NOT NULL, \
            status TEXT NOT NULL, \
            image TEXT NOT NULL, \
            video TEXT NOT NULL, \
            comment TEXT NOT NULL);"
            self.cursor.execute(create_intervention_table)
        except:
            pprint('Failed to connect to the database')


    def user_signup(self, firstname, lastname, othernames, email, phone_number, username, password, isadmin):
        '''Function to insert a user into users table'''
        query = f"INSERT INTO users(firstname, lastname, othernames, email, phone_number, username, password, isadmin)\
         VALUES('{firstname}', '{lastname}', '{othernames}', '{email}', '{phone_number}','{username}', '{password}', 'False') \
         RETURNING user_id,firstname, lastname, othernames, email, phone_number, username, password, isadmin;"
        # pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def admin_signup(self, firstname, lastname, othernames, email, phone_number, username, password, isadmin):
        '''Function to insert a admin into users table'''
        query = f"INSERT INTO users(firstname, lastname, othernames, email, phone_number, username, password, isadmin) \
        VALUES('{firstname}', '{lastname}', '{othernames}', '{email}', '{phone_number}','{username}', '{password}', 'True') \
        RETURNING user_id,firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin;"
        # pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user


    def query_one_user(self, user_id):
        '''Function to search a user into users table'''
        query = f"SELECT * FROM users WHERE user_id = '{user_id}';"
        pprint(query)
        self.cursor.execute(query)
        user= self.cursor.fetchone()
        pprint(user)
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

    def insert_incident(self, createdon, createdby, inctype, location, status, image, video,comment):
        '''Function to insert a red-flag into incidents table'''
        query = f"INSERT INTO incidents(createdon, createdby, inctype, location, status, image, video,comment) VALUES ('{createdon}', '{createdby}', '{inctype}', '{location}', '{status}', '{image}', '{video}', '{comment}') RETURNING incident_id,createdon, createdby, inctype, location, status, image, video,comment;"
        pprint(query)
        self.cursor.execute(query)
        incident = self.cursor.fetchone()
        return incident

    def update(self, table, column, new_value, cell, incident_id):
        '''Function to update a record into incidents table'''
        query = f"UPDATE {table} SET {column}='{new_value}' WHERE {cell}='{incident_id}' RETURNING incident_id;"
        pprint(query)
        self.cursor.execute(query)
        incident = self.cursor.fetchone()
        return incident

    def delete(self, table, cell, incident_id):
        '''Function to delete a record into incidents table'''
        query = f"DELETE FROM {table} WHERE {cell} = '{incident_id}'RETURNING incident_id;"
        pprint(query)
        self.cursor.execute(query)
        incident = self.cursor.fetchone()
        return incident

    def insert_intervention(self, createdon, createdby, inctype, location, status, image, video,comment):
        '''Function to create a intervention record into interventions table'''
        query = f"INSERT INTO interventions(createdon, createdby, inctype, location, status, image, video,comment) VALUES ('{createdon}', '{createdby}', '{inctype}', '{location}', '{status}', '{image}', '{video}', '{comment}') RETURNING intervention_id,createdon, createdby, inctype, location, status, image, video,comment;"
        pprint(query)
        self.cursor.execute(query)
        incident = self.cursor.fetchone()
        return incident

    def query_one_intervention(self, intervention_id):
        '''Function select one intervention in the database'''
        query = f"SELECT * FROM interventions WHERE intervention_id = '{intervention_id}';"
        pprint(query)
        self.cursor.execute(query)
        intervention= self.cursor.fetchone()
        pprint(intervention)
        return intervention

    def update_intervention(self, table, column, new_value, cell, intervention_id):
        '''Function to update one record in interventions table of the database'''
        query = f"UPDATE {table} SET {column}='{new_value}' WHERE {cell}='{intervention_id}' RETURNING intervention_id;"
        pprint(query)
        self.cursor.execute(query)
        intervention = self.cursor.fetchone()
        return intervention

    def delete_intervention(self, table, cell, intervention_id):
        '''Function to delete one record in interventions from the database'''
        query = f"DELETE FROM {table} WHERE {cell} = '{intervention_id}'RETURNING intervention_id;"
        pprint(query)
        self.cursor.execute(query)
        intervention = self.cursor.fetchone()
        return intervention

    
    def drop_table(self, table_name):
        '''Function to delete a table'''
        drop = f"DROP TABLE {table_name};"
        self.cursor.execute(drop)

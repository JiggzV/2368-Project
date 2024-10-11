import mysql.connector
from mysql.connector import Error

import flask
from flask import jsonify
from flask import request


#Setting the Application name
app = flask.Flask(__name__) #Sets up the application
app.config["DEBUG"] = True #Allow to show errors in browser

def create_con(hostname, username, userpw, dbname):
    connection = None
    try: 
        connection = mysql.connector.connect(
            host = hostname,
            user = username, 
            password = userpw,
            database= dbname
        )
        print('connection successful')
    except Error as e:
        print(f'the error {e} occured')
    return connection

conn = create_con('cis2368fall.c5yum806yt73.us-east-2.rds.amazonaws.com', 'admin', 'cis2368fallpass', 'cis2368falldb')
cursor = conn.cursor(dictionary=True)

#Creds.py and info needed to connect to MySQL DB

cursor.execute('''
CREATE TABLE IF NOT EXISTS Investor(
id INT AUTO_INCREMENT,
firstname VARCHAR(60) NOT NULL,
lastname INT(50) NOT NULL,
PRIMARY KEY(id)

);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Stock(
id INT AUTO_INCREMENT,
stockname VARCHAR(60) NOT NULL,
abbreviation VARCHAR(50) NOT NULL,
currentprice DECIMAL(10, 2),
PRIMARY KEY(id)

);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Bond(
id INT AUTO_INCREMENT,
stockname VARCHAR(60) NOT NULL,
abbreviation VARCHAR(50) NOT NULL,
currentprice DECIMAL(10, 2), 
PRIMARY KEY(id)
              
);
''')     

cursor.execute('''
CREATE TABLE IF NOT EXISTS Stocktransaction(
id INT AUTO_INCREMENT,
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
investorid INT,
stockid INT, 
quantity INT,
PRIMARY KEY (id),
FOREIGN KEY (investorid) REFERENCES Investor(id),
FOREIGN KEY (stockid) REFERENCES Stock(id)            
);

 ''')
              
cursor.execute('''
CREATE TABLE IF NOT EXISTS Bondtransaction(
id INT AUTO_INCREMENT,
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
investorid INT,
bondid INT, 
quantity INT,
PRIMARY KEY (id),
FOREIGN KEY (investorid) REFERENCES Investor(id),
FOREIGN KEY (bondid) REFERENCES Bond(id)            
);


''')
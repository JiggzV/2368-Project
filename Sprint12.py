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
lastname VARCHAR(50) NOT NULL,
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

#In this section, We will create all of the CRUD APIs for the Investor Table
@app.route('/api/Investors/<id>', methods = ['GET'])
def get_investor(id):
    cursor = conn.cursor
    cursor.execute("SELECT * FROM Investors WHERE id = %s", (id,))
    data = cursor.fetchone()
    if data:
        return jsonify({'id': data[0], 'firstname': data[1], 'lastname': data[2]})
    else:
        return jsonify({'message': 'Not found'})
    

@app.route('/api/Investors/', methods = ['GET'])
def get_all_investor():
    cursor.execute("SELECT * FROM Investors WHERE id = %s", (id,))
    data = cursor.fetchall()
    if data:
        investors = []
        for row in data:
            investors.append({'id': row[0], 'firstname': row[1], 'lastname': row[2]})
        return jsonify({'investors': investors})
    else:
        return jsonify({'message': 'Not found'})
    


@app.route('/api/Investors/', methods = ['POST'])
def post_investor():
    data = request.get_json()
    if 'firstname' not in data or 'lastname' not in data:
        return jsonify({'message': 'Missing info'}), 400
    
    try:
        cursor.execute("INSERT INTO Investor(firstname, lastname) VALUES (%s, %s)", (data['firstname'], data['lastname']))
        conn.commit()
        return jsonify({'message': 'Investor created successfully'}), 201
    except mysql.connector.Error as e:
        return jsonify({'message': f'Error: {e}'}), 500

@app.route('/api/Investors/<id>', methods = ['PUT'])
def update_investor(id):
    data = request.get_json()
    if 'firstname' not in data or 'lastname' not in data:
        return jsonify({'message': 'Missing Info'}), 400
    
    try: 
        cursor.execute("UPDATE Investor SET firstname = %s, lastname = %s WHERE id = %s", (data['firstname'], data['lastname'], id))
        conn.commit()
        return jsonify({'message': 'Investor Updated'}), 200
    except mysql.connector.Error as e:
        return jsonify({'message': f'An error occurred: {e}'}), 500
     


app.run()
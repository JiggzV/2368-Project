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
     
@app.route('/api/Investors/<id>', methods = ['DELETE'])
def delete_investor(id):
    cursor = conn.cursor()
    query = "DELETE FROM Investor WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return jsonify({'message': 'Investor Deleted'}), 200



''''''''''''''''''''''''''''''''''''
#In this section, we will create all of the endpoints for the "Bond" table.

@app.route('/api/Bonds/', methods = ['POST'])
def create_bond():
    cursor = conn.cursor()
    bondname = request.json['bondname']
    abbreviation = request.json['abbreviation']
    currentprice = request.json['currentprice']
    query = "INSERT INTO Bond (bondname, abbreviation, currentprice) VALUES (%s, %s, %s)"
    cursor.execute(query, (bondname, abbreviation, currentprice))
    conn.commit()
    return jsonify({'message': 'Bond has been created'}), 201

@app.route('/api/Bonds/', methods = ['GET'])
def get_allbond():
    cursor = conn.cursor()
    query = "SELECT * FROM Bond"
    cursor.execute(query)
    bond = cursor.fetchall()
    if bond:
        columns = [desc[0]for desc in cursor.description]
        bond_list = [dict(zip(columns, row)) for row in bond]
        return jsonify(bond_list)
    else:
        return jsonify({'Message': 'Not found'}), 404

@app.route('/api/Bonds/<id>', methods = ['GET'])
def get_abond(id):
    cursor = conn.cursor()
    query = "SELECT * FROM Bond WHERE id = %s"
    cursor.execute(query, (id,))
    bond = cursor.fetchone()
    if bond:
        columns = [desc[0]for desc in cursor.description]
        bond_dict = dict(zip(columns, bond))
        return jsonify(bond_dict)
    else:
        return jsonify({'Message': 'Not found'}), 404


@app.route('/api/Bonds/<id>', methods = ['PUT'])
def update_bond(id):
    cursor = conn.cursor()
    bondname = request.json['bondname']
    abbreviation = request.json['abbreviation']
    currentprice = request.json['currentprice']
    query = "UPDATE Bond SET bondname = %s, abbreviation = %s, currentprice = %s WHERE id = %s"
    cursor.execute(query, (bondname, abbreviation, currentprice, id))
    conn.commit()
    return jsonify({'message': 'Bond has been updated'}), 200


@app.route('/api/Bonds/<id>', methods = ['DELETE'])
def delete_bond(id):
    cursor = conn.cursor()
    query = "DELETE FROM Bond WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return jsonify({'message': 'Bond Deleted'}), 200


''''''''''''''''''''''''''''''''''''''''''''''''
#In this Section, we will implement the endpoints for the Stock table.
#I'm pretty much going to be using the same code used for my Bond Table

@app.route('/api/Stocks/', methods = ['POST'])
def create_stock():
    cursor = conn.cursor()
    stockname = request.json['stockname']
    abbreviation = request.json['abbreviation']
    currentprice = request.json['currentprice']
    query = "INSERT INTO Stock (stockname, abbreviation, currentprice) VALUES (%s, %s, %s)"
    cursor.execute(query, (stockname, abbreviation, currentprice))
    conn.commit()
    return jsonify({'message': 'Bond has been created'}), 201


@app.route('/api/Stocks/', methods = ['GET'])
def get_allstock():
    cursor = conn.cursor()
    query = "SELECT * FROM Stock"
    cursor.execute(query)
    stock = cursor.fetchall()
    if stock:
        columns = [desc[0]for desc in cursor.description]
        stock_list = [dict(zip(columns, row)) for row in stock]
        return jsonify(stock_list)
    else:
        return jsonify({'Message': 'Not found'}), 404


@app.route('/api/Stocks/<id>', methods = ['GET'])
def get_astock(id):
    cursor = conn.cursor()
    query = "SELECT * FROM Stock WHERE id = %s"
    cursor.execute(query, (id,))
    stock = cursor.fetchone()
    if stock:
        columns = [desc[0]for desc in cursor.description]
        stock_dict = dict(zip(columns, stock))
        return jsonify(stock_dict)
    else:
        return jsonify({'Message': 'Not found'}), 404


@app.route('/api/Stocks/<id>', methods = ['PUT'])
def update_stock(id):
    cursor = conn.cursor()
    stockname = request.json['stockname']
    abbreviation = request.json['abbreviation']
    currentprice = request.json['currentprice']
    query = "UPDATE Stock SET stockname = %s, abbreviation = %s, currentprice = %s WHERE id = %s"
    cursor.execute(query, (stockname, abbreviation, currentprice, id))
    conn.commit()
    return jsonify({'message': 'Stock has been updated'}), 200



@app.route('/api/Stocks/<id>', methods = ['DELETE'])
def delete_stock(id):
    cursor = conn.cursor()
    query = "DELETE FROM Stock WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return jsonify({'message': 'Stock Deleted'}), 200


app.run()
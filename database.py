import sqlite3

conn = sqlite3.connect('stocks.db')


def init():
    conn.execute('''create table if not exists Users 
            ( 
                ID INTEGER PRIMARY KEY,  
                first_name varchar(255), 
                last_name varchar(255), 
                user_name varchar(255) NOT NULL, 
                password varchar(255),          
                usd_balance DOUBLE NOT NULL
                ); ''')
    conn.execute('''create table if not exists Stocks  
            ( 
                ID INTEGER PRIMARY KEY, 
                stock_symbol varchar(4) NOT NULL, 
                stock_balance DOUBLE, 
                user_id int,          
                FOREIGN KEY (user_id) REFERENCES Users(ID)             
                ); ''')

    user = conn.execute('''SELECT * FROM Users WHERE ID = 1;''')

    if (user.fetchone() is None):
        conn.execute('''INSERT INTO Users (ID, first_name, last_name, user_name, password, usd_balance)
        VALUES (1, 'John', 'Doe', 'johndoe', 'password', 100);
        ''')

    conn.commit()


def buy_stock(stock_symbol, stock_price, stock_balance, user_id):
    # Check if user has enough money
    user = conn.execute('''SELECT * FROM Users
    WHERE ID = ?;
    ''', (user_id,)).fetchone()

    if (user is None or user[5] < stock_balance * stock_price):
        return False

    # Add stock
    conn.execute('''INSERT INTO Stocks (stock_symbol, stock_balance, user_id)
    VALUES (?, ?, ?);
    ''', (stock_symbol, stock_balance, user_id))
    # Adjust balance
    conn.execute('''UPDATE Users
    SET usd_balance = usd_balance - ?
    WHERE ID = ?;
    ''', (stock_balance * stock_price, user_id))
    conn.commit()


def sell_stock(stock_symbol, stock_price, stock_balance, user_id):

    # Check if user has enough stock
    stock = conn.execute('''SELECT * FROM Stocks
    WHERE stock_symbol = ? AND user_id = ?;
    ''', (stock_symbol, user_id)).fetchone()

    if (stock is None or stock[2] < stock_balance):
        return False

    # Delete stock if balance is 0
    if (stock[2] == stock_balance):
        conn.execute('''DELETE FROM Stocks
        WHERE stock_symbol = ? AND user_id = ?;
        ''', (stock_symbol, user_id))
    else:
        # Update stock balance
        conn.execute('''UPDATE Stocks
        SET stock_balance = stock_balance - ?
        WHERE stock_symbol = ? AND user_id = ?;
        ''', (stock_balance, stock_symbol, user_id))

    # Adjust balance
    conn.execute('''UPDATE Users
    SET usd_balance = usd_balance + ?
    WHERE ID = ?;
    ''', (stock_balance * stock_price, user_id))
    conn.commit()


def list_stocks(user_id):
    return conn.execute('''SELECT * FROM Stocks
    WHERE user_id = ?;
    ''', (user_id,)).fetchall()


def get_balance(user_id):
    return conn.execute('''SELECT usd_balance FROM Users
    WHERE ID = ?;
    ''', (user_id,)).fetchone()[0]

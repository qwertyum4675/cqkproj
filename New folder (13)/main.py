from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os 

app = Flask(__name__)
app.secret_key = "Super Secret"

my_database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="31MySql56",
    database ="cwktest"
)

mycursor = my_database.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")


HOST = os.environ.get('SERVER_HOST', 'localhost')
try:
    PORT = int(os.environ.get('SERVER_PORT', '5555'))
except ValueError: 
    PORT = 5555
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if (password != confirm_password):
            return render_template("signup.html", message= "Passwords don't match")
        
        sql = "SELECT username FROM users WHERE username = %s"
        value = (username,)
        mycursor.execute(sql, value)

        myresult = mycursor.fetchall()

        if len(myresult) > 0: 
            return render_template("signup.html", message = "Username already taken!")
        else: 
            sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
            values = (username, password)
            mycursor.execute(sql, values)
            my_database.commit()

            session['username'] = username  
            return redirect("/")
    else: 
        return render_template("signup.html")

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    else:
        return redirect('/login')    

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
    
            sql = "SELECT username FROM users WHERE username =%s AND password =%s"
            values = [username, password]
            mycursor.execute(sql, values)
    
            myresults = mycursor.fetchall()
    
            if len(myresults) > 0:
                session['username'] = username
                return redirect('/')
            else:
                return render_template('login.html', message = "Invalid username or password")
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)

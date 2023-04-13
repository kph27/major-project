from flask import Flask, render_template, request
import joblib
import numpy as np
import pickle
import sqlite3

app = Flask(__name__)

lr = joblib.load("Models/model.pkl")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("index.html")




@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        T, TM, Tm, SLP, H, VV, V, VM = float(request.form['T']), float(request.form['TM']), float(request.form['Tm']), float(request.form['SLP']), float(request.form['H']), float(request.form['VV']), float(request.form['V']), float(request.form['VM'])
        lr_pm = lr.predict([[T, TM, Tm, SLP, H, VV, V, VM]])

        # print(lr_pm)

    return render_template("result.html", lr_pm = np.round(lr_pm,3))


@app.route('/notebook')
def notebook():
	return render_template('Notebook.html')

@app.route('/about')
def about():
	return render_template('about.html')
   
if __name__ == "__main__":
    app.run(debug = True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  'apiKey': "AIzaSyCC2ny6fQZx7MsL9dLcdDkFLfTX6TMWHaw",
  'authDomain': "lissan-y2-f.firebaseapp.com",
  'projectId': "lissan-y2-f",
  'storageBucket': "lissan-y2-f.appspot.com",
  'messagingSenderId': "565841630605",
  'appId': "1:565841630605:web:c4833274438653ba2e99c4",
  'databaseURL':'https://lissan-y2-f-default-rtdb.europe-west1.firebasedatabase.app'
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()







@app.route('/', methods=['GET','POST'])
def index():
    result=''
    if request.method=='POST':
        num=int(request.form['num'])
        students=int(num/1500)
        books=int(num/2500)
        result1= num
        result2=students
        info =[]
        if num > 1500 and num < 2500:
            info=["By donating this amount of money you are helping this amount of woman ",""]

        elif num >= 2500 :
            info=["This donation will cover the costs of ","students per year","the number of books units in a text book, or enrichment materials"]

        elif num < 1500:
            info = ["you can contrbute to hire more staff members to improve our lessons quality"]
        return render_template('index.html', result1 = result1,result2=result2,info=info)
    return render_template('index.html', result = None)




@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
        user={"name":name,"email":email,"message":message}
        db.child('donations').push(user)
        return redirect (url_for('index'))
    return render_template("donate.html")

@app.route('/info', methods=['GET','POST'])
def info():
    if request.method=='POST':
        donations=db.child('donations').get().val()
        return render_template('info.html',donations=donations)
    else:
        return render_template('admin.html')



@app.route('/admin',methods=['GET','POST'])
def admin():
    error=''
    if request.method=='POST':
        name=request.form['name']
        last_name=request.form['last_name']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']


        # COMMENTED OUT TO ASSURE ONLY ONE USER (ADMIN) IN THE DATABASE-rani 
        try:
        #     login_session['user']=auth.create_user_with_email_and_password(email, password)
        #     user={'email':email, 'password':password}
        #     UID = login_session['user']['localId']
            # db.child('Users').child(UID).set(user)
            login_session['user']=auth.sign_in_user_with_email_and_password(email, password)
            return render_template('info.html')
        except:
            error='Authentication failed'
            return render_template('admin.html')
    else:
        return render_template('admin.html')
                









#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
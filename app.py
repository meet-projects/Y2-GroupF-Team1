from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  'apiKey': "AIzaSyCC2ny6fQZx7MsL9dLcdDkFLfTX6TMWHaw",
  'authDomain': "lissan-y2-f.firebaseapp.com",
  'projectId': "lissan-y2-f",
  'storageBucket': "lissan-y2-f.appspot.com",
  'messagingSenderId': "565841630605",
  'appId': "1:565841630605:web:c4833274438653ba2e99c4",'databaseURL':'https://lissan-y2-f-default-rtdb.europe-west1.firebasedatabase.app'
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        full_name=request.form['full_name']
        username=request.form['username']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user={'email':email, 'password':password, 'full_name':full_name, 'username':username}
            print("meow2")
            db.child('Users').child(UID).set(user)
            return redirect (url_for('home'))
        except:
            error='Authentication failed'
            return render_template('signup.html')
    else:
        return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            return redirect (url_for('home'))
        except:
            error='Authentication failed'
            return render_template('signin.html')
    else:
        return render_template('signin.html')

questions = [
    {
        'question': 'How do you say car?',
        'options': ['London', 'Berlin', 'Paris', 'Madrid'],
        'answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the "Red Planet"?',
        'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    }
    # Add more questions as needed
]

@app.route('/quiz')
def quiz():
    return render_template('gameshiraz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for question in questions:
        user_answer = request.form.get(question['question'])
        if user_answer == question['answer']:
            score += 1
    return render_template('result.html', score=score, total=len(questions))






@app.route('/', methods=['GET', 'POST'])
def game():
	return render_template("our_staff.html")
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
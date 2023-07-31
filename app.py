from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os
from flask import Flask, render_template, request, jsonify
import openai

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


openai.api_key = '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'

@app.route('/start', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        try:
            data = request.json
            if data and 'message' in data:
                user_message = data['message']
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo",  # Use gpt-3.5-turbo engine or the correct Babbage engine name if available
                    prompt=user_message,
                    max_tokens=150,
                    temperature=0.7
                )
                chatbot_response = response.choices[0].text.strip()
                return jsonify({'message': chatbot_response})
            else:
                return jsonify({'message': 'Invalid data format. Expected JSON with "message" field.'}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500  # Return error message and status code 500 for server errors
    else:
        return render_template('start.html')







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







@app.route('/game', methods=['GET', 'POST'])
def game():
	return render_template("game.html")
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
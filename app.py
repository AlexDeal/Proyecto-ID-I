from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import processor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore

cred = credentials.Certificate('static/prueba-bd942-firebase-adminsdk-xwv7e-50a290b79b.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

'''
email='alejandro@gmail.com'
doc_ref = db.collection('Usuarios').document(email)
try:

    doc_ref.set({
        'nombre':'Alejandro',
        'apellido': 'Serrano',
        'edad':23
    })
except:
    print('error')
'''

'''
email='alejandro@gmail.com'
password='123456'
try:
    user=auth.create_user(email=email, password=password)
except:
  print("An exception occurred")
'''

app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'

#VISTAS
@app.route('/')
def index():
    return render_template('index.html', **locals())

@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("chatbot.html", **locals())
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    if person["is_logged_in"] == True:
        return render_template("chatbot.html", email=person["email"], name=person["name"])
    else:
        return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')


#CONTROLADORES
@app.route('/controladorLogin', methods = ["POST", "GET"])
def controladorLogin():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["user"]
        password = result["password"]
        try:
            #Try signing in the user with the given information
            user = auth.get_user_by_email(email)
            #user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True

            #Get the name of the user

            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            #return print('welcome')
            return redirect(url_for('index'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            print('hola')
            #return redirect(url_for('index'))

@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']

        response = processor.chatbot_response(the_question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)

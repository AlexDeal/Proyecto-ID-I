from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import processor
import pyrebase

#Agregamos las credenciales
config = {
  "apiKey": "AIzaSyCa-18sM8mj-I_XOI4WlNk6M-BUNhTfsLs",
  "authDomain": "prueba-bd942.firebaseapp.com",
  "databaseURL": "https://prueba-bd942-default-rtdb.firebaseio.com/",
  "storageBucket": "prueba-bd942.appspot.com"
}

#Inicializamos firebase

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


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
           
            user = auth.sign_in_with_email_and_password(email, password)
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

@app.route("/controladorRegistro", methods = ["POST", "GET"])
def controladorRegistro():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        nombre = result["nombre"]
        apellidoP = result["AP"]
        apellidoM = result["AM"]
        email = result["direccion"]
        usuario = result["user"]
        password = result["password"]
        
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #person["name"] = user["name"]
            #Append data to the firebase realtime database
            data = {"nombre": nombre,
            'apellidoP':apellidoP,
            'apellidoM':apellidoM, 
            'email': email,
            'user':usuario,
            'contrasenia':password}

            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('index'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('index'))

@app.route('/salir')
def salir():
    person["is_logged_in"] = False
    return redirect(url_for('index'))

@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']

        response = processor.chatbot_response(the_question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)

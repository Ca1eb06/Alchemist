from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy()
db.init_app(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar_url = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    message = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        message_name = request.form['name']
        message_email = request.form['email']
        message_message = request.form['message']
        new_message = Message(name=message_name, email=message_email, message=message_message)

        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/users')
        except:
            return 'There was an issue adding your task'
    else: 
        return render_template('contact.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_item = User(
            name=name,
            email=email,
            password=password
        )
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/users')
        except:
            return 'There was an issue adding your task'
    else: 
        return render_template('signup.html')
    
@app.route('/users')
def users():
    users = User.query.order_by(User.date_created).all()
    print(len(users))
    return render_template('users.html', users=users)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/service.html', methods=['POST', 'GET'])
def service():
    return render_template('service.html')

@app.route("/test2")
def test2():
    return render_template("test2.html")

if (__name__ == "__main__"):
    app.run(debug=True)
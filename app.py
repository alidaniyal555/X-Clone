from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/userprofile')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/userprofile')
def userprofile():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('userprofile.html',user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/notification')
def notification():
    return render_template('notification.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/grock')
def grock():
    return render_template('grock.html')


@app.route('/lists')
def lists():
    return render_template('lists.html')


@app.route('/communities')
def communities():
    return render_template('communities.html')

@app.route('/Premium')
def Premium():
    return render_template('Premium.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/Create Account')
def CreateAccount():
    return render_template('CreateAccount.html')

@app.route('/Next')
def next_page():
    return render_template('next_page.html')

@app.route('/next_page1')
def next_page1():
    return render_template('next_page1.html')

if __name__ == '__main__':
    app.run(debug=True)
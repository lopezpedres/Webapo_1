#import all the necessary packages
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_email


#create the app and app's name
app = Flask(__name__)

#if dev, it's development mode. Which means that we are going to store our data in postgres
ENV = 'development'
if ENV == 'development':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123Aapostgres@localhost/lexus'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mkcnzewcfnabvp:9a3c01b63813a9cea66d0446133d142e0c33c9fccfb376392730962fc98b5930@ec2-18-233-83-165.compute-1.amazonaws.com:5432/dbvftaq99n20rr'

#We dont want to keep track of this if we dont need it, requires extra memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#creates our db, which works with models
db = SQLAlchemy(app)

class feedBack(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique = True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,customer,dealer,rating,comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments



#the "/" means that is ony for the home page
@app.route("/")
def index():
    return render_template("index.html")

"""le damos la ruta a la que queremos llegar, dentro de index.html hay un tag que se llama
form, dentro hay una accion y un metodo los cuales vamos a usar """

@app.route('/submit', methods=['POST'])
def submit():
    if request.method =='POST':
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        #print(customer,dealer, rating, comments)
        
        if customer == '' or dealer == '':
            return render_template('index.html', message= 'Please enter required fields')
        if db.session.query(feedBack).filter(feedBack.customer==customer).count()==0:
            data=feedBack(customer,dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
            send_email(customer,dealer,rating,comments)
            return render_template("success.html")
        else: 
             return render_template('index.html', message= 'You have al ready submitted feedback')
#Esto es para que el programa unicamente corra cuando llamemos a programa.       
if __name__=='__main__':
    app.run()
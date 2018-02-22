# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
#from sqlalchemy.types import DateTime
import config
import os
import datetime
#from datetime import datetime


# create the application object
app = Flask(__name__)


# search for app environment setting to automatically find out production vs development environment
app.config.from_object(os.environ['APP_SETTINGS'])

# get config >> remove this comment part in production and save it in a personal log file
# create database object after app
config.BaseConfig.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# add this local settings to the environment to create environment variables
# in the terminal: 
# export APP_SETTINGS="config.DevelopmentConfig"
# Flask will look for APP_SETTINGS in OS-environment variables to figure out DevelopmentMode or Production Mode

# Set env variable for local database
# in the terminal: 
# export DATABASE_URL="sqlite:////orders.db"

#print(os.environ['APP_SETTINGS']) # prints app setting in any environment. This is for checking!
#print(os.environ['DATABASE_URL'])

#app.secret_key = config.SECRET_KEY


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    return render_template('index.html')  # render a template
    # return "Hello, World!"  # return a string


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('[Logged In]')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are Logged Out.')
    return redirect(url_for('welcome'))



# ---------------------------------------------------------------------------
"""
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(30))
    email = db.Column(db.Unicode(30))
    telephone = db.Column(db.Unicode(8))
    many_orders = db.relationship('Orders', backref='owner', lazy='dynamic')

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Unicode(30))
    description = db.Column(db.Unicode(200))
    quantity = db.Column(db.Integer)
    received_time = db.Column(db.DateTime)
    payed_time = db.Column(db.DateTime)
    payed = db.Column(db.Unicode(5))
    amount_total = db.Column(db.Integer)
    tag = db.Column(db.Unicode(10))
    Customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
"""

# TODO
# revisit the queries, maybe by keeping server running on a a single run time to keep database in consistent state
# deploy to Heroku


def create_tables():
    db.create_all()
    db.session.commit()

#create_tables()
#  >>>> relationel insert work correct on single session / runtime !!!

# TODO: Make a full order List e.g.: 
# order_spec=
# [['jack', 'ja@gmail.com', '12345678'], 
# ['sandwich', 'bread, apple, orange', '6', ],
# ['sandwich', 'bread, apple, orange', '10', ],
# ['sandwich', 'no bread, rice, almond', '4', ]]
# this method must get an order List with customer info and order details as input
# the method must then read and parse the List elements for insert into database tables.
# this method returns 2 time of the same cutomer and order in the database ?!
# the same method returns only one in the mode_test.py. Debug why ?!
# try to remove method call and run this part as script ... 
def insert_order(customer_name, customer_email, customer_tel):
    c_obj = Customer(name=customer_name, email=customer_email, telephone=customer_tel)

    o1 = Orders(item_name='sw', description='salaterne osv', quantity='2',
    received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
    payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='yes', 
    amount_total='24', tag='eGt4H2b', owner=c_obj)


    db.session.add(c_obj)
    db.session.commit()
    

#insert_order('Joe', 'jojo@jo.io', '22113344')


def insertToCustomer(customer_name, customer_email, customer_tel):
    if is_recorded(customer_email, customer_tel) is False:
        new_customer = Customer(name=customer_name, email=customer_email, telephone=customer_tel)
        db.session.add(new_customer)
        db.session.commit()
        return
    print('--- Customer already exists! ---')




# create Customers
#c1 = Customer(name='anthon', email='sdfsdf@ur.fk', telephone='11223344')
#c2 = Customer(name='jack', email='vdfvdfv@dl.qw', telephone='22334455')

# create Orders and relate it to their parents 'owner'
#o3 = Orders(item_name='sw', description='salaterne osv', quantity='10',
#received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
#payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='no', amount_total='190', tag='ufe4oi3', owner=c1)

#o4 = Orders(item_name='sw', description='agurk, pasta, killer cili', quantity='7',
#received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
#payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='yes', amount_total='311', tag='ksj4yRq', owner=c1)

##o2 = Orders(email='teter@tet.dk', owner=c1)
##o3 = Orders(email='45ter@3et.dt', owner=c1)
##o4 = Orders(email='11ter@4et.dr', owner=c2)


#db.session.add(c1)
#db.session.add(c2)
#db.session.commit()

##alternative 
##p1.many_orders.append(a1)





# -------------------------  Database queries for Customer Table  ------------------------------



def get_customer_list():
    result = Customer.query.all()
    for res in result:
        print(res.name, res.email, res.telephone)


def is_recorded(customer_tel, customer_email):
    result_for_tel = Customer.query.filter(or_(Customer.telephone==customer_tel, Customer.email==customer_email)).first()
    if result_for_tel is None:
        return False
    return True


def update_customer_name(customer_tel, customer_email, new_name):
    if is_recorded(customer_tel, customer_email) is True:
        result_for_update = Customer.query.filter_by(telephone=customer_tel).first()
        result_for_update.name = new_name
        db.session.commit()
        print('--- updated! ---')
        return
    print('--- no records to update ---')


def is_recorded(customer_tel, customer_email):
    result_for_tel = Customer.query.filter(or_(Customer.telephone==customer_tel, Customer.email==customer_email)).first()
    if result_for_tel is None:
        return False
    return True


def get_customer_by_name(customer_name):
    customer_by_name = Customer.query.filter_by(name=customer_name).first()
    print('..............', customer_by_name.name, customer_by_name.telephone, customer_by_name.email )


def get_customer_by_tel_email(customer_tel, customer_email):
        customer_tel_email = Customer.query.filter_by(telephone=customer_tel, email=customer_email).first()
        if customer_tel_email is None:
            #customer_tel_email = 'no records exists in database'
            print('----------- no records in database ---------------')
        else:
            print('..............', customer_tel_email.name, customer_tel_email.telephone, customer_tel_email.email )



#get_customer_list()
#insertToCustomer('TREX-Killer', '90439433', 'alf@ravity.org')
#get_customer_by_tel_email('90439425' ,'alf@gravity.or')
#update_customer_name('83710200', 'ib@iblo.dk', 'T---rex')



# -------------------------  Database queries for Orders Table  ------------------------------



def get_orders_list():
    result_ordr = Orders.query.all()
    for res in result_ordr:
        print(
            res.id, res.item_name, res.description, res.quantity,
            res.id, res.fk_customer, res.received_time, res.payed_time,
            res.payed_yes, res.payed_no, res.amount_total, res.tag
             )

#get_orders_list()


# check if customer exist, return customer ID. If not exist insert new customer and return new customer ID
def is_recorded_get_customer_ID(customer_name, customer_tel, customer_email):
    result_for_tel_email = Customer.query.filter(or_(Customer.telephone==customer_tel, Customer.email==customer_email)).first()
    if result_for_tel_email is None:
        insertToCustomer(customer_name, customer_tel, customer_email)
        new_customer_id = Customer.query.filter_by(telephone=customer_tel).first()
        #print('&&&&&----&&&>>  ', new_customer_id.id) #test
        return new_customer_id.id
    else:
        #print(result_for_tel_email.id) # test
        return result_for_tel_email.id


#is_recorded_get_customer_ID('john', "87657777", "mailme@gmail.dr")

# TODO: Forign key insert into Orders using is_recoreced_get_customer_ID(), 
def insertToOrders():
    order_received_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # make order_list [..., ..., order_received_time, ...]
    # identify customer by tel and email using is_recorded_get_customer
    # insert into Orders TAble
    print (order_received_time)
    


# TODO: maybe foreign key create table for production?, sqlalchemy relation
# TODO: UPDATE/UPSERT if payed / if Not Payed

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()

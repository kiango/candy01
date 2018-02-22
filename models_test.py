from app import db
import datetime


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


# TODO
# revisit the queries, maybe by keeping server running on a a single run time to keep database in consistent state
# deploy to Heroku

def create_tables():
    db.create_all()
    db.session.commit()

create_tables()
#  >>>> relationel insert work correct on single session / runtime !!!

# try to put this in a method and call to se if the methodcreates duplicates in tables !!?
# create Customers
c1 = Customer(name='anthon', email='sdfsdf@ur.fk', telephone='11223344')
c2 = Customer(name='jack', email='vdfvdfv@dl.qw', telephone='22334455')

# create Orders and relate it to their parents 'owner'
o1 = Orders(item_name='sw', description='salaterne osv', quantity='2',
received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='yes', amount_total='24', tag='eGt4H2b', owner=c1)

o1 = Orders(item_name='sw', description='salaterne osv', quantity='1',
received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='yes', amount_total='14', tag='lkr4H2b', owner=c1)

o1 = Orders(item_name='sw', description='salaterne osv', quantity='10',
received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='no', amount_total='190', tag='ufe4oi3', owner=c1)

o1 = Orders(item_name='sw', description='agurk, pasta, killer cili', quantity='7',
received_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
payed_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), payed='yes', amount_total='311', tag='ksj4yRq', owner=c1)

#o2 = Orders(email='teter@tet.dk', owner=c1)
#o3 = Orders(email='45ter@3et.dt', owner=c1)
#o4 = Orders(email='11ter@4et.dr', owner=c2)

# select customer > if exist > add(c1); else insert customer and add(c1)
db.session.add(c1)
db.session.add(c2)
db.session.commit()

#alternative 
#p1.many_orders.append(a1)

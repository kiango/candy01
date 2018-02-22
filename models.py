from app import db

# class named as the table name in the database 'candy'
class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode(30))
    telephone = db.Column('telephone', db.Unicode(8))
    email = db.Column('email', db.Unicode(30))

    # constructor
    def __init__(self, name, telephone, email):
        self.name = name
        self.telephone = telephone
        self.email = email

    def __repr__(self):
        return '<Customer %r>' % self.name


#db.create_all()


# --------------------  independent query methods -----------------------------------
def insertToCustomer():
    new_entry = Customer('Alfred', '90439424', 'alf@gravity.org')
    db.session.add(new_entry)
    db.session.commit()

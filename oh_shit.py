from app import app, db
from app.mod_sms.models import *

ug1 = UserGroup(name='Canyon Time', phone='+17868378095', active=True)
ug2 = UserGroup(name='test', phone='+18503783607', active=True)

ryan  = User(fname='Ryan', lname='Kuhl', phone='+13058985985', active=True)
simon = User(fname='Simon', lname='', phone='+13109264989', active=True)
dan = User(fname='Dan' , lname='Malik', phone='+14152718694', active=True)
tom = User(fname='Tom' , lname='Scorer', phone='+13109022760', active=True)
steve = User(fname='Steve', lname='Makuch', phone='+16164609893', active=True)
chris = User(fname='Chris', lname='', phone='+16269882527', active=True)
ben = User(fname='Ben' , lname='Eisenbise', phone='+13234017625', active=True)
alex = User(fname='Alex', lname='Thorpe', phone='+14243869550', active=True)

ug1.groups_to_users.append(ryan)
ug1.groups_to_users.append(simon)
ug1.groups_to_users.append(dan)
ug1.groups_to_users.append(tom)
ug1.groups_to_users.append(steve)
ug1.groups_to_users.append(chris)
ug1.groups_to_users.append(ben)
ug1.groups_to_users.append(alex)

ug2.groups_to_users.append(ryan)

db.session.add(ug1)
db.session.add(ug2)
db.session.add(ryan)
db.session.add(simon)
db.session.add(dan)
db.session.add(tom)
db.session.add(steve)
db.session.add(chris)
db.session.add(ben)
db.session.add(alex)

db.session.commit()

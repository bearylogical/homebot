from homebot import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    MACaddresses = db.relationship('MACaddress', backref='user', lazy='dynamic')

    # def __init__(self, name, email):
    # 	self.name = name
    # 	self.email = email

    def __repr__(self):
        return '<ID %r>' % (self.id) + '<User %r>' % (self.name) + '<email %r>' % (self.email) + '<MACaddresses %r>' % (
            self.MACaddresses)


class MACaddress(db.Model):
    __tablename__ = 'mac_address'
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(20), index=True, unique=True)
    device_name = db.Column(db.String(20), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# def __init__(self, macAddress, device_name,):
# 	self.macAddress = macAddress
# 	self.device_name = device_name

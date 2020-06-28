#  (c) Giovambattista Vieri 2020
#  All Rights Reserved
#  License GPL 
#  No guarantee/warranty on this alpha code. 
# 
#

from flask import Flask 
from flask import render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from datetime import datetime, timedelta
import requests
import csv
from flask import send_file


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./localvalues.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
totemname = 'totem n. 1'


db = SQLAlchemy(app)
class locmeasures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False) 
    value = db.Column(db.Float, default=0)
    uploaded = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name

    def __init__(self,name, value):
        self.name=name
        self.value=value

engine=db.create_all()

try: 
    dummy=locmeasures(name='test',value=36.6);
    print(dummy)
    db.session.add(dummy)
    db.session.commit()
except:
    print('eccezione inizializzazione db')

@app.route('/upload')
def upload():
# here we have to make a select than upload every record
    # lock the table!!!!
    f = open('upload.csv', 'w')
    out = csv.writer(f)
    toupload = locmeasures.query.filter(locmeasures.uploaded == False).all()
    for item in toupload:
        out.writerow([totemname, item.name , item.timestamp , item.value] )
        # don't forget to change uploaded status 
        item.uploaded=True
    
    f.close()  
    db.session.commit()
     
    return send_file('upload.csv',
                     mimetype='text/csv',
                     attachment_filename='upload.csv',
                     as_attachment=True)

@app.route('/show')
def show():
#### hereby the business logic 
    dummy=locmeasures.query.all()
    val=render_template("listall.html", query=dummy, title='prova')
    since = datetime.now() - timedelta(hours=8)
#    old = locmeasures.query.filter(locmeasures.timestamp > text('(NOW() - INTERVAL 8 HOURS)')).all()
    old = locmeasures.query.filter(locmeasures.timestamp < since).all()
#    for r in old:
#        print(r) 
    return val

@app.route('/insertform')
def insertform():
### it will increment quantity by one. 
    return render_template('insertvalue.html')

@app.route('/insertvalue', methods=['POST'])
def insertvalue():
    msg=" problem on insertion" 
    if request.method == 'POST':
        try:
            msg="everything ok"
            print ('getting parameters')
            name = request.form['name']
            valuestr=str(request.form['value']  )
#            print("---"+valuestr+"||||")  

            value = float(valuestr)  
            pin = request.form['pin'] 
#            print (' {} {} {} '.format(name, value, pin))
            dummy=locmeasures(name=name,value=value)
            db.session.add(dummy)
            db.session.commit()
        except Exception as e: 
            print ('type is:', e.__class__.__name__)
            print (e) 
            db.session.rollback()
            msg="problem in db add" 
        finally:
            return render_template('resultinsert.html', msg=msg)

    return render_template('resultinsert.html', msg=msg)

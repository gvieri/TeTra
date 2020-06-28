#   
# traffic light: it get input from three endpoint:
# show - it show the data as color red green yellow
# increment - it is the increment 
# decrement - it is the decrement 
#

from flask import Flask 
from flask import render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from datetime import datetime, timedelta
from io import TextIOWrapper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://centraldb:centraldb@localhost/centraldb'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class measures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    totemid = db.Column(db.String(36), nullable=False) # uuid related to totem location
    name = db.Column(db.String(80), nullable=False)
    totemtimestamp = db.Column(db.DateTime(timezone=True),nullable=False) # timestamp related to token
    timestamp = db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False) 
    value = db.Column(db.Float, default=0)
    uploaded = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<name %r>' % self.name

    def __init__(self,name, value):
        self.name=name
        self.value=value

db.create_all()

try: 
    dummy=locmeasures(name='test',value=36.6);
    print(dummy)
    db.session.add(dummy)
    db.session.commit()
except:
    print('eccezione inizializzazione db')

@app.route('/upload',methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            record = User(totemid=row[0], name=row[1], totemtimestamp=row[2],value=row[3] )
            db.session.add(record)
            db.session.commit()
        return redirect(url_for('upload'))
    return """
            <form method='post' action='/' enctype='multipart/form-data'>
              Upload a totem csv file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
           """

@app.route('/show')
def show():
#### hereby the business logic 
    dummy=locmeasures.query.all()
    val=render_template("listall.html", query=dummy, title='prova')
    since = datetime.now() - timedelta(hours=8)
#    old = locmeasures.query.filter(locmeasures.timestamp > text('(NOW() - INTERVAL 8 HOURS)')).all()
    old = locmeasures.query.filter(locmeasures.timestamp < since).all()
    for r in old:
        print(r) 
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
            totemid = request.form['totemid']
            name = request.form['name']
            totemtimestamp = request.form['totemtimestamp']
            valuestr=str(request.form['value']  )
            value = float(valuestr)  
            pin = request.form['pin'] 
            print (' {} {} {} '.format(name, value, pin))
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

#################################################

if __name__ == '__main__':
    app.run(host="localhost", port=5555, debug=False)



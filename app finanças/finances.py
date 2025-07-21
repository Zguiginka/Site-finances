from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'banco1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Gastos(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.Date)
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)
    cat1 = db.Column(db.String(50))
    cat2 = db.Column(db.String(50))

@app.context_processor
def inject_globals():
    g2 = 2700
    g1 = 700
    g3 = g2 - g1
    g1car = 250
    b1car = 200
    tcar = b1car - g1car
    return dict(g1=g1, g2=g2, g3=g3, g1car=g1car, b1car=b1car, tcar=tcar)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/gastos', methods=['GET', 'POST'])
def gastos():
    
    if request.method == 'POST':
            data=request.form['data']
            dataobj = datetime.strptime(data,'%Y-%m-%d').date()
            newgasto = Gastos(data=dataobj)
            db.session.add(newgasto)
            db.session.commit()
            return redirect('/gastos')
    return render_template('gastos.html')
    

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print('criad com sucesso')
        except Exception as e:
            print(f'{e}')
    app.run(debug=True)



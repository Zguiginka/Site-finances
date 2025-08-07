import os
from flask import Flask, render_template,request,redirect
from models import db,Gastos
from routes.home import home_bp
from routes.gastos import gastos_bp
from routes.budget import budget_bp
from routes.ganhos import ganhos_bp

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'banco1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(gastos_bp)
app.register_blueprint(budget_bp)




   
if __name__ == '__main__':
    
    with app.app_context():
        try:
            db.create_all()
            print('criad com sucesso')
        except Exception as e:
            print(f'{e}')
    app.run(debug=True)



from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract

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
    idparc = db.Column(db.Integer)
    numparcela = db.Column(db.Integer)
    

@app.context_processor
def inject_globals():
    g2 = 2700
    g1 = 700
    g3 = g2 - g1
    g1car = 200
    b1car = 250
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

    meses_disp = sorted(set(
        gasto.data.strftime('%Y-%m') for gasto in Gastos.query.all() if gasto.data)
    )
    
    if request.method == 'POST':
            data=request.form['data']
            dataobj = datetime.strptime(data,'%Y-%m-%d').date()
            prod = request.form['produto']
            preco = request.form['valor']
            catego1 = request.form['cat1']
            catego2 = request.form['cat2']
            numparc = request.form['qtd_parcelas']




            

            if numparc == "":
                newgasto = Gastos(
                    data=dataobj,
                    descricao=prod,
                    valor=preco,
                    cat1= catego1,
                    cat2= catego2
                    )
                db.session.add(newgasto)
                db.session.commit()
                return redirect('/gastos')
            else:
                numparc = int(numparc)           
                parcfield = request.form['tipo_entrada']

                if parcfield == "total":
                    
                    valfim = float(preco)/numparc
                    
                    
                    for i in range(numparc):
                        count = i + 1
                        idparcelasdb = db.session.query(db.func.max(Gastos.idparc)).scalar()
                        if idparcelasdb == None:
                            idparcelas = 0
                        else:
                            idparcelas = int(idparcelasdb+1)
                        print(idparcelas)
                        nameparc = fr"{str(count)}/{str(numparc)}"
                        datasparc = dataobj + relativedelta(months = i)

                        newgasto = Gastos(
                            data=datasparc,
                            descricao=prod,
                            valor=valfim,
                            numparcela = nameparc,
                            idparc = idparcelas,
                            cat1= catego1,
                            cat2= catego2
                            )
                        
                        db.session.add(newgasto)
                        db.session.commit()
                else:
                        for i in range(numparc):
                            valfim = float(preco)
                            count = i + 1
                            idparcelasdb = db.session.query(db.func.max(Gastos.idparc)).scalar()
                            if idparcelasdb == None:
                                idparcelas = 0
                            else:
                                idparcelas = int(idparcelasdb+1)
                            print(idparcelas)
                            nameparc = fr"{str(count)}/{str(numparc)}"
                            datasparc = dataobj + relativedelta(months = i)

                            newgasto = Gastos(
                                data=datasparc,
                                descricao=prod,
                                valor=valfim,
                                numparcela = nameparc,
                                idparc = idparcelas,
                                cat1= catego1,
                                cat2= catego2
                                )
                            
                            db.session.add(newgasto)
                            db.session.commit()

                print("Todos adicionados com sucesso")
                return redirect('/gastos')
    if request.method == "GET":
        mes = request.args.get('filtro_messel')
        
        print(mes)
        if mes:
            ano, mesnum = mes.split('-')
            gastos = Gastos.query.filter(
                extract('year',Gastos.data) == int(ano),
                extract('month',Gastos.data) == int(mesnum)
            ).all()
        else:
            gastos = Gastos.query.all()


        resumo = {}

        for gasto in gastos:
            cat = gasto.cat1
            if cat not in resumo:
                resumo[cat] = {'total': 0, 'gastos': []}

            resumo[cat]['total'] += gasto.valor
            resumo[cat]['gastos'].append({
                'descricao': gasto.descricao,
                'data': datetime.strftime(gasto.data,'%d-%m'),
                'valor': gasto.valor
            })

        
        
                    

    return render_template('gastos.html', resumo=resumo,gastos=gastos,meses_disp=meses_disp)
    

if __name__ == '__main__':
    
    with app.app_context():
        try:
            db.create_all()
            print('criad com sucesso')
        except Exception as e:
            print(f'{e}')
    app.run(debug=True)



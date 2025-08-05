from flask import Flask, render_template,request,redirect,Blueprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
from models import db,Gastos
from utils import bdbuy,get_meses_disp,inject_globals


gastos_bp = Blueprint('gastos',__name__)

@gastos_bp.route('/gastos',methods=['GET', 'POST'])
def gastos():

    meses_disp = get_meses_disp()

    if request.method == 'POST':
            data=request.form['data']
            dataobj = datetime.strptime(data,'%Y-%m-%d').date()
            prod = request.form['produto']
            preco = request.form['valor']
            catego1 = request.form['cat1']
            catego2 = request.form['cat2']
            numparc = request.form['qtd_parcelas']
            metod = request.form['metodo']

            if numparc == "":
                newgasto = Gastos(
                    data=dataobj,
                    descricao=prod,
                    valor=preco,
                    cat1= catego1,
                    cat2= catego2,
                    metodo = metod
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
                            cat2= catego2,
                            metodo = metod
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
                                cat2= catego2,
                                metodo = metod
                                )
                            
                            db.session.add(newgasto)
                            db.session.commit()

                print("Todos adicionados com sucesso")
                return redirect('/gastos')
            
    if request.method == "GET":
        mes = request.args.get('filtro_messel')
        
        
        if mes:
            ano, mesnum = mes.split('-')
            gastos = Gastos.query.filter(
                extract('year',Gastos.data) == int(ano),
                extract('month',Gastos.data) == int(mesnum)
            ).all()
        else:
            gastos = Gastos.query.all()


        resumo,totalgasto = bdbuy(gastos)
            
        
        
                    

    return render_template('gastos.html',totalgasto=totalgasto,filtromes=mes, resumo=resumo,gastos=gastos,meses_disp=meses_disp)
    
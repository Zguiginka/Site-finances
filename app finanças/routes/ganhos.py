from flask import Flask, render_template,request,redirect,Blueprint,flash
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
from models import db,Ganhos
from utils import bdbuy,get_meses_disp,inject_globals,get_meses_disp_gan,bdwon


ganhos_bp = Blueprint('ganhos',__name__)

@ganhos_bp.route('/ganhos',methods=['GET', 'POST'])
def ganhos_view():

    meses_disp = get_meses_disp_gan()

    if request.method == 'POST':
            data=request.form['data']
            dataobj = datetime.strptime(data,'%Y-%m-%d').date()
            prod = request.form['produto']
            preco = request.form['valor']
            catego1 = request.form['cat1']

            
            newgasto = Ganhos(
                    data=dataobj,
                    descricao=prod,
                    valor=preco,
                    categoria= catego1,
                    )
            db.session.add(newgasto)
            db.session.commit()
            return redirect('/ganhos')
                        
            db.session.add(newgasto)
            db.session.commit()
    if request.method == "GET":
        mes = request.args.get('filtro_messel')
        
        
        if mes:
            ano, mesnum = mes.split('-')
            ganhos = Ganhos.query.filter(
                extract('year',Ganhos.data) == int(ano),
                extract('month',Ganhos.data) == int(mesnum)
            ).all()
        else:
            ganhos = Ganhos.query.all()


        resumo,totalgasto = bdwon(ganhos)
    return render_template("ganhos.html",resumo=resumo,totalgasto=totalgasto,ganhos=ganhos)
from flask import Flask, render_template,request,redirect,Blueprint
from sqlalchemy import extract
from models import Gastos
from utils import get_meses_disp, bdbuy, inject_globals

home_bp = Blueprint('home',__name__)

@home_bp.route('/')

def home():
           
    mes = request.args.get('filtro_messel')
            
    if mes:
        ano, mesnum = mes.split('-')
        gastos = Gastos.query.filter(
        extract('year',Gastos.data) == int(ano),
        extract('month',Gastos.data) == int(mesnum)
        ).all()
        meses_disp = get_meses_disp()
        _,totalgasto = bdbuy(gastos)


    else:
        gastos = Gastos.query.all()
        meses_disp = get_meses_disp()
        _,totalgasto = bdbuy(gastos)

    return render_template('index.html',totalgasto=totalgasto,meses_disp = meses_disp,filtromes = mes)
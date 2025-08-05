from flask import Flask, render_template,request,redirect,Blueprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
from models import db,Gastos
from utils import bdbuy,get_meses_disp,inject_globals

budget_bp = Blueprint('budget',__name__)

@budget_bp.route('/budget')
def budget():
    return render_template('budget.html')
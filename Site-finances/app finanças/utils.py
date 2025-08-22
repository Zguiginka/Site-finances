from models import Gastos, Ganhos


def inject_globals():
    g2 = 2700
    g1 = 700
    g3 = g2 - g1
    g1car = 200
    b1car = 250
    tcar = b1car - g1car
    return dict(g1=g1, g2=g2, g3=g3, g1car=g1car, b1car=b1car, tcar=tcar)

def get_meses_disp():
     return sorted(set((
        gasto.data.strftime('%Y-%m'),gasto.data.strftime('%b-%Y')) for gasto in Gastos.query.all() if gasto.data))

def get_meses_disp_gan():
     return sorted(set((
        ganho.data.strftime('%Y-%m'),ganho.data.strftime('%b-%Y')) for ganho in Ganhos.query.all() if ganho.data))
    
    
def bdbuy(gastos):
    resumo = {}
    for gasto in gastos:
            cat1 = gasto.cat1
            cat2 = gasto.cat2 if gasto.cat2 else cat1

            # Se categoria 1 ainda não existe, cria
            if cat1 not in resumo:
                resumo[cat1] = {
                    'total': 0,
                    'subcategorias': {}
                }

            # Se categoria 2 ainda não existe dentro da cat1, cria
            if cat2 not in resumo[cat1]['subcategorias']:
                resumo[cat1]['subcategorias'][cat2] = {      
                    'total': 0,
                    'gastos': []
                }

            # Soma os totais
            resumo[cat1]['total'] += gasto.valor
            resumo[cat1]['subcategorias'][cat2]['total'] += gasto.valor

            # Adiciona o gasto individual à subcategoria
            resumo[cat1]['subcategorias'][cat2]['gastos'].append({
                'descricao': gasto.descricao,
                'data': gasto.data.strftime('%d-%m'),
                'valor': gasto.valor,
                'id':gasto.id
            })
    totalgasto = sum(cat['total'] for cat in resumo.values())
    print(resumo)
    return(resumo,totalgasto)

def bdwon(ganhos):
    resumo = {}
    for ganho in ganhos:
            cat1 = ganho.categoria
            

            # Se categoria 1 ainda não existe, cria
            if cat1 not in resumo:
                resumo[cat1] = {
                    'total': 0,
                    'categorias': []
                }


            # Soma os totais
            resumo[cat1]['total'] += ganho.valor
            

            # Adiciona o gasto individual à subcategoria
            resumo[cat1]['categorias'].append({
                'descricao': ganho.descricao,
                'data': ganho.data.strftime('%d-%m'),
                'valor': ganho.valor,
                'id':ganho.id
            })
    totalgasto = sum(cat['total'] for cat in resumo.values())
    return(resumo,totalgasto)
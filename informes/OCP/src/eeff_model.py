import json, openpyxl, glob
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

P=json.load(open('/tmp/claude-0/ocp_prod.json'))
# concentration-stage national copper for share
nat={}
X='/tmp/claude-0/dl/x/'
for f,y in [('Producción metálica Ene - Dic 2023.xlsx','2023'),('Producción Metálica Ene - Dic 2024.xlsx','2024'),('Producci#U00f3n Minera Ene - Dic 2025.xlsx','2025'),('Producci#U00f3n met#U00e1lica Ene - Ago 2026.xlsx','2026')]:
    ws=openpyxl.load_workbook(X+f,read_only=True,data_only=True).worksheets[0]
    s=0
    for r in ws.iter_rows(values_only=True):
        if r and r[0]=='COBRE' and r[2] in ('CONCENTRACIÓN','BENEFICIO','LIXIVIACIÓN') and isinstance(r[22],(int,float)) and str(r[3]).upper()!='REFINACIÓN':
            s+=r[22]
    nat[y]=s
print('nat conc', nat)

KG_OZ=1/0.0311034768
LB_T=2204.62262
Y=['2023','2024','2025','2026P','2027P','2028P']
cu={'2023':P['2023']['COBRE'][-1],'2024':P['2024']['COBRE'][-1],'2025':P['2025']['COBRE'][-1]}
ag={'2023':P['2023']['PLATA'][-1],'2024':P['2024']['PLATA'][-1],'2025':P['2025']['PLATA'][-1]}
cu26_8=P['2026']['COBRE'][-1]; ag26_8=P['2026']['PLATA'][-1]
cu['2026P']=cu26_8/8*12; ag['2026P']=ag26_8/8*12
# 2027-28: planta 9,1 ktpd sin ampliación aprobada; supuesto +5%/año por ramp-up a 6 ktpd
cu['2027P']=cu['2026P']*1.05; ag['2027P']=ag['2026P']*1.05
cu['2028P']=cu['2027P']*1.05; ag['2028P']=ag['2027P']*1.05

A={ # supuestos por año
 'pcu':  {'2023':3.84775,'2024':4.14623,'2025':4.50894,'2026P':6.13756,'2027P':5.700610,'2028P':5.60}, # US$/lb BCRPData / MMM
 'pag':  {'2023':23.404,'2024':28.240,'2025':40.095,'2026P':71.630,'2027P':55.0,'2028P':50.0},
 'tc':   {'2023':3.7438,'2024':3.7539,'2025':3.5681,'2026P':3.4029,'2027P':3.45,'2028P':3.50},
 'TC':   {'2023':88,'2024':80,'2025':21.25,'2026P':0,'2027P':10,'2028P':20},      # US$/dms benchmark
 'RC':   {'2023':0.088,'2024':0.080,'2025':0.02125,'2026P':0,'2027P':0.010,'2028P':0.020}, # US$/lb
 'ley':  {'2023':1.00,'2024':1.00,'2025':1.00,'2026P':1.00,'2027P':1.00,'2028P':1.00}, # % Cu cabeza
 'rec':  {'2023':0.88,'2024':0.92,'2025':0.92,'2026P':0.92,'2027P':0.92,'2028P':0.92},
 'cuxt': {'2023':60.0,'2024':50.0,'2025':52.0,'2026P':56.0,'2027P':57.0,'2028P':58.0}, # US$/t tratada
 'capex':{'2023':25.0,'2024':50.0,'2025':40.0,'2026P':35.0,'2027P':30.0,'2028P':25.0},
 'ga':   {'2023':5.0,'2024':6.0,'2025':6.0,'2026P':6.5,'2027P':6.5,'2028P':7.0},
}
GRADE_CONC=0.24; PAY_CU=0.965; PAY_AG=0.90; RC_AG=0.50; FLETE=70.0; HUM=0.08
COMPRA=22.0; VU_COMPRA=10; VU_CAPEX=8; TASA_INT=0.08; IR=0.295; PART=0.08; APORTE=0.0035
CAP_INI=30.0; RED_CAP_PEN=22.6

def tramos(m, base, paso, inc, maxr, top=None):
    # devuelve tasa efectiva marginal sobre la utilidad operativa (por tramos de margen de 5 pp desde 10%)
    edges=[0,0.10]+[0.10+0.05*i for i in range(1,15)]+[9]
    rates=[base+inc*i for i in range(len(edges)-1)]
    rates=[min(r,maxr) for r in rates]
    if top: rates[-1]=top
    tot=0
    for i in range(len(edges)-1):
        a,b=edges[i],edges[i+1]
        if m>a: tot+=(min(m,b)-a)*rates[i]
    return tot/m if m>0 else base

R={k:{} for k in ['cu','ag','agoz','mineral','tpd','conc','cupay_lb','ingCu','ingAg','ingBruto','tcrc','flete','ventas','opex','ga','ebitda','dep','ebit_pre','regalia','iem','aporte','ebit','int','ebt','part','ir','neta','capex','cxc','inv','cxp','ppe_b','ppe_n','deuda','caja','capital','res','c1','pagable_ag','ventas_pen','nat_share']}
dep_capex_hist=[]
CAJA_MIN=5.0
deuda=0.0; caja=CAP_INI-COMPRA; capital=CAP_INI; resacum=0; perdida=0
ppe_b=COMPRA; acc_dep=0
prev={'cxc':0,'inv':0,'cxp':0}
for i,y in enumerate(Y):
    c=cu[y]; a=ag[y]; oz=a*KG_OZ
    mineral=c/(A['ley'][y]/100*A['rec'][y])/1e6
    conc=c/GRADE_CONC
    lbpay=c*PAY_CU*LB_T
    ingCu=lbpay*A['pcu'][y]/1e6
    ingAg=oz*PAY_AG*A['pag'][y]/1e6
    tcrc=(conc*A['TC'][y] + lbpay*A['RC'][y] + oz*PAY_AG*RC_AG)/1e6
    flete=conc/(1-HUM)*FLETE/1e6
    ventas=ingCu+ingAg-tcrc-flete
    opex=mineral*A['cuxt'][y]
    ga=A['ga'][y]
    dep=COMPRA/VU_COMPRA + sum(dep_capex_hist)/VU_CAPEX
    aporte=ventas*APORTE
    op=ventas-opex-ga-dep
    m=op/ventas
    reg=max(op*tramos(m,0.01,0.0075,0.0075,0.12),0.01*ventas) if op>0 else 0.01*ventas
    iem=op*tramos(m,0.02,0.004,0.004,0.084,top=0.084) if op>0 else 0
    ebit=op-reg-iem-aporte
    interes=deuda*TASA_INT
    ebt=ebit-interes
    part=max(ebt,0)*PART
    base_ir=ebt-part
    if base_ir<0: perdida+=-base_ir; imp=0
    else:
        uso=min(perdida,base_ir); perdida-=uso; imp=(base_ir-uso)*IR
    neta=ebt-part-imp
    cxc=ventas*30/365; inv=(opex+ga)*30/365; cxp=(opex+ga)*45/365
    dwc=(cxc-prev['cxc'])+(inv-prev['inv'])-(cxp-prev['cxp'])
    capex=A['capex'][y]
    red=RED_CAP_PEN/A['tc'][y] if y=='2024' else 0
    fco=neta+dep-dwc
    fcf=fco-capex
    # fondeo: la caja por encima del mínimo y el FCF amortizan deuda; el déficit se cubre con deuda (vinculadas/prepagos)
    caja_disp=caja+fcf-red
    if caja_disp<CAJA_MIN:
        nueva=CAJA_MIN-caja_disp; deuda+=nueva; caja=CAJA_MIN
    else:
        amort=min(deuda,caja_disp-CAJA_MIN); deuda-=amort; caja=caja_disp-amort
    capital-=red; resacum+=neta
    ppe_b+=capex; acc_dep+=dep; dep_capex_hist.append(capex)
    vals=dict(cu=c,ag=a,agoz=oz/1e3,mineral=mineral,tpd=mineral*1e6/350,conc=conc,cupay_lb=lbpay/1e6,ingCu=ingCu,ingAg=ingAg,
              ingBruto=ingCu+ingAg,tcrc=tcrc,flete=flete,ventas=ventas,opex=opex,ga=ga,ebitda=ventas-opex-ga-reg-iem-aporte,dep=dep,
              ebit_pre=op,regalia=reg,iem=iem,aporte=aporte,ebit=ebit,int=interes,ebt=ebt,part=part,ir=imp,neta=neta,capex=capex,
              fco=fco,fcf=fcf,red=red,
              cxc=cxc,inv=inv,cxp=cxp,ppe_b=ppe_b,ppe_n=ppe_b-acc_dep,deuda=deuda,caja=caja,capital=capital,res=resacum,
              c1=(opex+ga+tcrc+flete-ingAg)/(lbpay/1e6),ventas_pen=ventas*A['tc'][y],
              nat_share=(c/nat[y[:4]]*100 if y[:4] in ('2023','2024','2025') else (cu26_8/nat['2026']*100 if y=='2026P' else None)))
    for k,v in vals.items(): R.setdefault(k,{})[y]=v
    prev={'cxc':cxc,'inv':inv,'cxp':cxp}
    act=caja+cxc+inv+ppe_b-acc_dep; pp=cxp+deuda+capital+resacum
    assert abs(act-pp)<1e-6, (y,act,pp)
json.dump({'R':R,'A':A,'Y':Y,'cu26_8':cu26_8,'ag26_8':ag26_8,'nat':nat},open('/tmp/claude-0/ocp_model.json','w'),indent=1)
for k in ['cu','agoz','fco','fcf','caja','mineral','tpd','ventas','ingCu','ingAg','tcrc','flete','opex','dep','regalia','iem','ebit','int','neta','c1','ppe_n','deuda','capital','res','nat_share']:
    print(f"{k:10s}",' '.join(f"{(R[k][y] if R[k][y] is not None else float('nan')):10.2f}" for y in Y))

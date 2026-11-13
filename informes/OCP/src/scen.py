import json
M=json.load(open('/tmp/claude-0/ocp_model.json')); R=M['R']; A=M['A']
LB_T=2204.62262; KG_OZ=1/0.0311034768
def tramos(m, base, inc, maxr, top=None):
    edges=[0,0.10]+[0.10+0.05*i for i in range(1,15)]+[9]
    rates=[min(base+inc*i,maxr) for i in range(len(edges)-1)]
    if top: rates[-1]=top
    tot=sum((min(m,b)-a)*r for a,b,r in zip(edges[:-1],edges[1:],rates) if m>a)
    return tot/m if m>0 else base
def pl(y,pcu,pag,cuxt=None,tc_mult=1.0,soles_share=0.55,interes=0.0):
    c=R['cu'][y]; oz=R['agoz'][y]*1e3; conc=R['conc'][y]; lbpay=R['cupay_lb'][y]*1e6
    ingCu=lbpay*pcu/1e6; ingAg=oz*0.9*pag/1e6
    tcrc=(conc*A['TC'][y]+lbpay*A['RC'][y]+oz*0.9*0.5)/1e6; fl=R['flete'][y]
    ventas=ingCu+ingAg-tcrc-fl
    ct=(cuxt or A['cuxt'][y]); opex=R['mineral'][y]*ct*(soles_share/tc_mult+(1-soles_share))
    ga=A['ga'][y]; dep=R['dep'][y]
    op=ventas-opex-ga-dep; m=op/ventas
    reg=max(op*tramos(m,0.01,0.0075,0.12),0.01*ventas) if op>0 else 0.01*ventas
    iem=op*tramos(m,0.02,0.004,0.084,0.084) if op>0 else 0
    ap=ventas*0.0035; ebit=op-reg-iem-ap; ebitda=ebit+dep
    ebt=ebit-interes; neta=ebt*(1-0.08)*(1-0.295) if ebt>0 else ebt
    return dict(ventas=ventas,opex=opex,ebitda=ebitda,ebit=ebit,neta=neta,reg=reg+iem,margen=ebitda/ventas)
S={'Alto':{'2026P':(6.14,71.6),'2027P':(7.00,65.0),'2028P':(6.80,60.0)},
   'Base':{'2026P':(6.14,71.6),'2027P':(5.70,55.0),'2028P':(5.60,50.0)},
   'Bajo':{'2026P':(6.14,71.6),'2027P':(4.50,35.0),'2028P':(4.30,30.0)}}
out={}
for k,v in S.items():
    out[k]={y:pl(y,*v[y]) for y in v}
    print(k,{y:{a:round(b,1) for a,b in d.items() if a in('ventas','ebitda','neta')} for y,d in out[k].items()})
# precio de equilibrio (EBIT=0) 2027 y C1+D&A
for y in ['2025','2027P']:
    lo,hi=1.0,6.0
    for _ in range(60):
        mid=(lo+hi)/2
        if pl(y,mid,A['pag'][y])['ebit']>0: hi=mid
        else: lo=mid
    print('breakeven',y,round(hi,2))
# elasticidad del EBITDA y de las ventas al precio del cobre (2027 base, ±10%)
b=pl('2027P',5.70,55); u=pl('2027P',5.70*1.1,55)
print('eps ventas',round((u['ventas']/b['ventas']-1)/0.1,2),'eps ebitda',round((u['ebitda']/b['ebitda']-1)/0.1,2),'eps neta',round((u['neta']/b['neta']-1)/0.1,2))
# TC: depreciación 10% (3,45->3,80) en 2027 base
d=pl('2027P',5.70,55,tc_mult=1.10); print('TC +10%: ebitda',round(b['ebitda'],1),'->',round(d['ebitda'],1))
# inflación costos +5,25% vs 2,0% sobre opex 2027
print('opex 2027 base',round(b['opex'],1),'+1pp inflación =',round(b['opex']*0.01,2))
json.dump({'S':S,'out':out},open('/tmp/claude-0/ocp_scen.json','w'),indent=1)

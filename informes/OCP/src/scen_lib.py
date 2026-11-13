import json
M=json.load(open("/tmp/claude-0/ocp_model.json")); R=M["R"]; A=M["A"]
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

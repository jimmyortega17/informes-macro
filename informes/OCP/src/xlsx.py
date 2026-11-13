import re, os, sys, ast, json, shutil
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
S=os.path.dirname(os.path.abspath(__file__)); OUT=sys.argv[1]
src=open(os.path.join(S,"build.py"),encoding="utf-8").read()
cuts={k:src.index(f'MARK("{k}")') for k in ("s1int","s1peru","s2desc","s2imp")}
pat=re.compile(r'CADENA\("([^"]+)",\s*\n\s*(\[.*?\]),\s*\n\s*"([^"]*)"',re.S)
chains=[]
for m in pat.finditer(src):
    pos=m.start(); sec="s1int" if pos<cuts["s1peru"] else "s1peru" if pos<cuts["s2desc"] else "s2imp"
    t=re.sub(r"^Cadena \d*\.?\s*","",m.group(1)); chains.append((sec,f"Cadena {len(chains)+1}. "+t,ast.literal_eval(m.group(2)),m.group(3)))
wb=Workbook(); ws=wb.active; ws.title="Cadenas de Razonamiento"
for i,col in enumerate("ABCDEFGHIJK"): ws.column_dimensions[col].width=22 if i%2==0 else 3
ws["A1"]="OPERADORES CONCENTRADOS PERUANOS S.A.C. (MINA COBRIZA) — CADENAS DE RAZONAMIENTO MACROECONÓMICO 2026-2028"; ws["A1"].font=Font(name="Calibri",bold=True,size=13)
ws["A2"]="Fuente: BCRP RI setiembre 2026 / BCRPData (consulta 13-nov-2026) / MINEM / MEF MMM 2027-2030 / Veritrade-SUNAT / EEFF estimados por el grupo"; ws["A2"].font=Font(name="Calibri",size=8)
titles={"s1int":"■  SECCIÓN 1 — INTERNACIONAL","s1peru":"■  SECCIÓN 1 — PERÚ","s2imp":"■  SECCIÓN 2 — IMPACTO SOBRE OCP (9 CANALES)"}
F_FIRST,F_MID,F_LAST="FFDDEEFF","FFE2EFDA","FFF2F2F2"
r=4; cur=None
for sec,title,elems,nota in chains:
    if sec!=cur:
        r+=1; ws.cell(r,1,titles[sec]).font=Font(name="Calibri",bold=True,size=11); r+=2; cur=sec
    ws.cell(r,1,title).font=Font(name="Calibri",bold=True,size=10); r+=1
    n=len(elems)
    for k,(no,ci) in enumerate(elems):
        col=1+2*k; fill=PatternFill("solid",fgColor=F_FIRST if k==0 else F_LAST if k==n-1 else F_MID)
        sym=no[0] if no[0] in "↑↓" else "→"
        c=ws.cell(r,col,sym); c.font=Font(name="Calibri",bold=True,size=13); c.fill=fill; c.alignment=Alignment(horizontal="center")
        txt=(no[1:] if no[0] in "↑↓" else no).strip()+"\n"+ci
        c=ws.cell(r+1,col,txt); c.font=Font(name="Calibri",size=9); c.fill=fill; c.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
        if k<n-1:
            a=ws.cell(r,col+1,"→"); a.font=Font(name="Calibri",bold=True,size=14); a.alignment=Alignment(horizontal="center")
    ws.row_dimensions[r+1].height=72
    c=ws.cell(r+2,1,nota); c.font=Font(name="Calibri",size=9,italic=True); c.alignment=Alignment(wrap_text=True,vertical="top")
    ws.merge_cells(start_row=r+2,start_column=1,end_row=r+2,end_column=11); ws.row_dimensions[r+2].height=30
    r+=5
wb.save(os.path.join(OUT,"OCP_Cadenas_Razonamiento.xlsx")); print("cadenas",len(chains))

# ---------- OCP_EEFF.xlsx: formato minera corona + hojas de soporte ----------
M=json.load(open('/tmp/claude-0/ocp_model.json')); R=M['R']; Y=["2026P","2025","2024","2023"]
SC=json.load(open('/tmp/claude-0/ocp_scen.json'))
base=os.path.join(OUT,"OCP_EEFF_estimados.xlsx"); dst=os.path.join(OUT,"OCP_EEFF.xlsx")
wb=openpyxl.load_workbook(base)
HDR=PatternFill("solid",fgColor="FFBEBEBE"); SUBT=PatternFill("solid",fgColor="FFD3D3D3"); WH=PatternFill("solid",fgColor="FFFFFFFF")
def sheet(ws,title,rows):
    ws["A1"]="ESTIMADO POR EL GRUPO — OCP no publica EEFF (US$ millones)"; ws["A1"].font=Font(name="Calibri",bold=True,color="C00000")
    for j,h in enumerate([title]+Y):
        c=ws.cell(2,1+j,h); c.font=Font(name="Calibri",bold=True,size=9); c.fill=HDR
    for i,(label,key) in enumerate(rows,3):
        bold=label.isupper() or label.startswith(("Total","Utilidad","Flujo","EBITDA","Ventas netas"))
        ws.cell(i,1,label).font=Font(name="Calibri",bold=bold,size=9); ws.cell(i,1).fill=SUBT if bold else WH
        for j,y in enumerate(Y):
            v=None if key is None else (key(y) if callable(key) else R[key][y])
            c=ws.cell(i,2+j,v); c.font=Font(name="Calibri",bold=bold,size=9); c.fill=SUBT if bold else WH
            if isinstance(v,float): c.number_format="#,##0.0" if abs(v)>=3 or key not in('c1',) else "0.00"
    ws.column_dimensions["A"].width=52
    for col in "BCDE": ws.column_dimensions[col].width=12
ws=wb.create_sheet("Hoja1",0)
sheet(ws,"ESTADO DE SITUACIÓN FINANCIERA",[("ACTIVOS",None),("Efectivo y equivalentes","caja"),("Cuentas por cobrar comerciales (traders)","cxc"),("Inventarios (concentrado y suministros)","inv"),
 ("Total Activos Corrientes",lambda y:R['caja'][y]+R['cxc'][y]+R['inv'][y]),("Propiedad, planta y equipo, bruto","ppe_b"),("Propiedad, planta y equipo, neto","ppe_n"),
 ("Total Activos",lambda y:R['caja'][y]+R['cxc'][y]+R['inv'][y]+R['ppe_n'][y]),("PASIVOS",None),("Cuentas por pagar comerciales","cxp"),("Deuda con vinculadas / prepagos (cierre)","deuda"),
 ("Total Pasivos",lambda y:R['cxp'][y]+R['deuda'][y]),("PATRIMONIO",None),("Capital social (neto de reducción S/22,6 MM en 2024)","capital"),("Resultados acumulados","res"),
 ("Total Patrimonio",lambda y:R['capital'][y]+R['res'][y]),("Total Pasivo y Patrimonio",lambda y:R['cxp'][y]+R['deuda'][y]+R['capital'][y]+R['res'][y])])
ws=wb.create_sheet("Hoja2",1)
sheet(ws,"ESTADO DE RESULTADOS",[("Ingreso bruto cobre","ingCu"),("Ingreso bruto plata","ingAg"),("(−) TC/RC","tcrc"),("(−) Flete y depósito Callao","flete"),("Ventas netas","ventas"),
 ("(−) Costo de operación","opex"),("(−) G&A y ventas","ga"),("EBITDA","ebitda"),("(−) Depreciación","dep"),("(−) Regalía minera","regalia"),("(−) IEM","iem"),("(−) Aportes OEFA/Osinergmin","aporte"),
 ("Utilidad operativa (EBIT)","ebit"),("(−) Gastos financieros","int"),("Utilidad antes de participaciones e IR","ebt"),("(−) Participación de trabajadores","part"),("(−) Impuesto a la renta","ir"),("Utilidad neta","neta")])
ws=wb.create_sheet("Hoja3",2)
sheet(ws,"ESTADO DE FLUJOS DE EFECTIVO",[("Utilidad neta","neta"),("(+) Depreciación","dep"),("Flujo de operación (neto de Δ capital de trabajo)","fco"),("(−) Capex","capex"),
 ("Flujo libre (operación − capex)","fcf"),("Reducción de capital pagada","red"),("Deuda (saldo de cierre)","deuda"),("Saldo de caja","caja")])
ws=wb.create_sheet("Ratios",3)
sheet(ws,"RATIOS OCP",[("Margen EBITDA (%)",lambda y:R['ebitda'][y]/R['ventas'][y]*100),("Margen neto (%)",lambda y:R['neta'][y]/R['ventas'][y]*100),("C1 neto (US$/lb Cu)","c1"),
 ("Deuda / EBITDA (veces)",lambda y:R['deuda'][y]/R['ebitda'][y]),("ROE (%)",lambda y:R['neta'][y]/(R['capital'][y]+R['res'][y])*100),
 ("Liquidez corriente (veces)",lambda y:(R['caja'][y]+R['cxc'][y]+R['inv'][y])/R['cxp'][y]),("Capex / ventas (%)",lambda y:R['capex'][y]/R['ventas'][y]*100),
 ("Días de cobro / días de pago",lambda y:"30 / 45")])
ws=wb.create_sheet("Escenarios",4)
ws["A1"]="Escenarios de precio del cobre 2027P-2028P (US$ MM) — estimado por el grupo"; ws["A1"].font=Font(bold=True,size=12)
hdr=["Escenario","Prob.","Cu 2027","Ag 2027","Ventas 2027","EBITDA 2027","Utilidad 2027","Cu 2028","Ag 2028","Ventas 2028","EBITDA 2028","Utilidad 2028"]
for j,h in enumerate(hdr): c=ws.cell(3,1+j,h); c.font=Font(bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor="1F3864")
for i,(k,p) in enumerate([("Alto",0.25),("Base",0.5),("Bajo",0.25)],4):
    o=SC['out'][k]; s=SC['S'][k]
    vals=[k,p,s['2027P'][0],s['2027P'][1],o['2027P']['ventas'],o['2027P']['ebitda'],o['2027P']['neta'],s['2028P'][0],s['2028P'][1],o['2028P']['ventas'],o['2028P']['ebitda'],o['2028P']['neta']]
    for j,v in enumerate(vals): c=ws.cell(i,1+j,v); c.number_format="0.0" if j>1 else "0%"
ws.cell(8,1,"Elasticidades (2027P, cobre base ±10%): ventas 0,86; EBITDA 1,55; utilidad neta 1,89. Precio de equilibrio (EBIT = 0): US$2,83/lb. TC +10% → EBITDA +US$4,5 MM.")
ws.column_dimensions["A"].width=14
wb.save(dst); print("eeff ok", wb.sheetnames)
wb=openpyxl.load_workbook(dst)
ws=wb.create_sheet("Plan_vs_Real",5)
ws["A1"]="Plan de minado (SINIA/MINAM, SMPCM UM Cobriza, info dic-2021) vs producción real (MINEM)"; ws["A1"].font=Font(bold=True,size=12)
hdr=["Año","Mineral plan (t)","Concentrado plan (t secas)","Cu plan (t)","Ley cabeza implícita plan (%)","Ley conc. plan (%)","Cu real MINEM (TMF)","Cumplimiento (%)","Mineral estimado grupo (Mt)"]
for j,h in enumerate(hdr): c=ws.cell(3,1+j,h); c.font=Font(bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor="1F3864")
plan=[("2022",548000,19461,4281,0),("2023",1649000,60025,13806,8351),("2024",1644000,64755,15217,14791),("2025",1826000,74820,17583,16545)]
for i,(y,mi,co,cu,re_) in enumerate(plan,4):
    vals=[y,mi,co,cu,cu/mi*100,cu/co*100,re_,re_/cu*100,R['mineral'].get(y)]
    for j,v in enumerate(vals):
        c=ws.cell(i,1+j,v)
        if isinstance(v,float): c.number_format="0.00"
ws.cell(9,1,"Calibración: el supuesto del grupo (ley 1,0% × recuperación 92% = 0,92% efectivo) frente a 0,93% (2024) y 0,96% (2025) del plan; mineral estimado a <2% del plan. Concentrado 23,5% vs 24% supuesto: +US$0,1-0,2 MM de TC/RC y flete al año (no material).")
ws.cell(10,1,"Conceptos: (a) producción MINEM = dato real; (b) ventas locales a traders = estimación; (c) exportaciones SUNAT por RUC = 0 para OCP; (d) ingresos tributarios = reservados.")
wb.save(dst); print("plan ok")

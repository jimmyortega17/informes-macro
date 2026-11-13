import json, openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
M=json.load(open('/tmp/claude-0/ocp_model.json')); R=M['R']; A=M['A']; Y=M['Y']
P=json.load(open('/tmp/claude-0/ocp_prod.json'))
wb=openpyxl.Workbook()
B=Font(bold=True,name='Calibri',size=11); N=Font(name='Calibri',size=11); I=Font(italic=True,name='Calibri',size=9,color='555555')
H=PatternFill('solid',fgColor='1F3864'); HF=Font(bold=True,color='FFFFFF',name='Calibri',size=11)
E=PatternFill('solid',fgColor='FFF2CC'); thin=Side(style='thin',color='999999')
TAG='ESTIMADO POR EL GRUPO (no son EEFF auditados ni publicados por OCP)'
def sheet(name,title,widths=None):
    ws=wb.create_sheet(name); ws['A1']=title; ws['A1'].font=Font(bold=True,size=13,name='Calibri'); ws['A2']=TAG; ws['A2'].font=Font(bold=True,color='C00000',name='Calibri')
    if widths:
        for i,w in enumerate(widths): ws.column_dimensions[chr(65+i)].width=w
    return ws
def header(ws,row,vals):
    for j,v in enumerate(vals):
        c=ws.cell(row,1+j,v); c.fill=H; c.font=HF; c.alignment=Alignment(horizontal='center',wrap_text=True)
def rows(ws,start,items,fmt='#,##0.0'):
    r=start
    for it in items:
        lab,key=it[0],it[1]; f=it[2] if len(it)>2 else fmt; bold=it[3] if len(it)>3 else False
        ws.cell(r,1,lab).font=B if bold else N
        for j,y in enumerate(Y):
            v=R[key][y] if isinstance(key,str) else key(y)
            c=ws.cell(r,2+j,v); c.number_format=f; c.font=B if bold else N
            if y.endswith('P'): c.fill=E
        r+=1
    return r
wb.remove(wb.active)
# Resumen
ws=sheet('Resumen','OCP – Cobriza: EEFF estimados 2023-2025 y proyección 2026P-2028P (US$ millones)',[52]+[13]*6)
header(ws,4,['Concepto']+Y)
r=rows(ws,5,[('Cobre fino producido (TMF) – MINEM, real','cu','#,##0'),('Plata producida (miles oz) – MINEM, real','agoz','#,##0'),
 ('Precio cobre (US$/lb) – BCRPData / MMM',lambda y:A['pcu'][y],'0.00'),('Precio plata (US$/oz) – BCRPData / supuesto',lambda y:A['pag'][y],'0.00'),
 ('Ventas netas (NSR)','ventas','#,##0.0',True),('Costo de operación (mina+planta)','opex'),('Gastos de administración y ventas','ga'),
 ('Depreciación y amortización','dep'),('Regalía minera + IEM + aportes',lambda y:R['regalia'][y]+R['iem'][y]+R['aporte'][y]),
 ('Utilidad operativa (EBIT)','ebit','#,##0.0',True),('Gastos financieros','int'),('Participación de trabajadores (8%)','part'),('Impuesto a la renta (29,5%)','ir'),
 ('Utilidad neta','neta','#,##0.0',True),('Margen EBIT (%)',lambda y:R['ebit'][y]/R['ventas'][y],'0.0%'),('Margen neto (%)',lambda y:R['neta'][y]/R['ventas'][y],'0.0%'),
 ('Cash cost C1 neto de subproducto (US$/lb Cu pagable)','c1','0.00'),('Capex','capex'),('Activo fijo neto','ppe_n'),('Deuda (vinculadas / prepagos de traders)','deuda'),
 ('Patrimonio','capital'),('Ventas netas (S/ millones, al TC promedio)','ventas_pen','#,##0.0'),('Participación en el cobre nacional, etapa concentración (%)','nat_share','0.00')])
ws.cell(r+1,1,'Las columnas amarillas son proyecciones. 2026P = enero-agosto real (MINEM) anualizado; los precios de 2026 son el promedio de enero a octubre de BCRPData; 2027P-2028P usan el cobre y el zinc del MMM 2027-2030.').font=I
ws.cell(r+2,1,'"Patrimonio" = capital social neto de la reducción; los resultados acumulados van en la hoja Balance.').font=I
# Produccion
ws=sheet('Produccion_MINEM','Producción mensual de OCP – U.M. Expansión Cobriza (MINEM, producción minera por titular)',[10]+[10]*13)
r=4
for y in ['2023','2024','2025','2026']:
    for mn,u in [('COBRE','TMF'),('PLATA','kg finos')]:
        header(ws,r,[f'{mn} {y} ({u})','Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic','Acum.']); r+=1
        ws.cell(r,1,mn)
        for j,v in enumerate(P[y][mn]):
            c=ws.cell(r,2+j,v); c.number_format='#,##0.0'
        r+=2
ws.cell(r,1,'Fuente: MINEM, «Producción Minera» por titular y unidad (archivos 2023, 2024, 2025 y enero-agosto 2026), https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera. Etapa: concentración/flotación; titular: Operadores Concentrados Peruanos S.A.C.; unidad: EXPANSION COBRIZA (San Pedro de Coris, Churcampa, Huancavelica). El MINEM no registra zinc, plomo ni oro para OCP.').font=I
# Supuestos
ws=sheet('Supuestos','Supuestos de la estimación',[58]+[11]*6+[60])
header(ws,4,['Supuesto']+Y+['Fuente / justificación'])
sup=[('Precio cobre LME (US$/lb)','pcu','BCRPData PN01652XM (promedio anual; 2026 = ene-oct). 2027P-2028P: MMM 2027-2030 (C-01): 570 y 560 ¢/lb'),
('Precio plata (US$/oz)','pag','BCRPData PN01655XM (2026 = ene-oct). 2027P-2028P: supuesto del grupo (reversión parcial)'),
('Tipo de cambio (S/ por US$)','tc','BCRPData PN01234PM (promedio anual; 2026 = ene-oct). 2027P-2028P: supuesto'),
('TC concentrado (US$/dms)','TC','Benchmark anual China-Antofagasta: 88 (2023), 80 (2024), 21,25 (2025), 0 (2026). 2027P-28P: supuesto'),
('RC cobre (US$/lb)','RC','Benchmark anual (igual que el TC/10)'),
('Ley de cabeza Cu (%)','ley','Supuesto del grupo (histórico de Cobriza ~1% Cu); no publicado por OCP'),
('Recuperación metalúrgica Cu','rec','Supuesto del grupo (88% durante el arranque de 2023; 92% en régimen)'),
('Costo de operación (US$/t tratada)','cuxt','Volcan, costo unitario consolidado: 49,2 US$/t (2024), 51,7-58,6 (trimestres de 2025), 60,6-70 (2026); Nexa Cerro Lindo: 39,9 US$/t (2025). Cobriza (~5 ktpd) se ubica en el rango de Volcan'),
('Capex (US$ MM)','capex','Supuesto del grupo, acotado por el capex ≥US$50 MM anunciado para 2024 (S. Dyer, Energiminas, dic-2023), la MEIA-d (US$93,3 MM) y los ITS (US$66,7 MM y US$8,25 MM)'),
('G&A y ventas (US$ MM)','ga','Supuesto del grupo (oficina en Lima, comercialización y seguros)')]
r=5
for lab,k,src in sup:
    ws.cell(r,1,lab)
    for j,y in enumerate(Y): c=ws.cell(r,2+j,A[k][y]); c.number_format='0.000' if A[k][y]<10 else '#,##0.0'
    ws.cell(r,8,src).alignment=Alignment(wrap_text=True); r+=1
fix=[('Ley del concentrado de cobre','24% Cu','Supuesto del grupo (típico en concentrados peruanos: 22-28%)'),
('Cobre pagable','96,5%','Término estándar de los contratos de concentrado (deducción de ~1 unidad)'),
('Plata pagable / RC de la plata','90% / US$0,50 por oz','Término estándar para el Ag contenido en un concentrado de Cu'),
('Flete mina–Callao + almacén y embarque','US$70 por tm húmeda; humedad 8%','Supuesto del grupo (unos 480 km por carretera más el depósito en el Callao, p. ej. Perubar)'),
('Compra de activos (2022)','US$22,0 MM; vida útil de 10 años','US$19,7 MM sin IGV (Andina) y US$22 MM con IGV/costos (Energiminas, Consultores A1)'),
('Depreciación del capex','8 años, desde el año siguiente','Supuesto del grupo'),
('Regalía minera (Ley 28258, mod. Ley 29788)','1%-12% de la utilidad operativa por tramos de margen; mínimo 1% de las ventas','Ley 29788'),
('Impuesto Especial a la Minería (Ley 29789)','2%-8,4% de la utilidad operativa por tramos de margen','Ley 29789'),
('Aportes OEFA + Osinergmin','0,35% de las ventas','D.S. de aportes por regulación (supuesto simplificado)'),
('Participación de trabajadores','8% de la utilidad antes de impuestos','D. Leg. 892 (minería)'),
('Impuesto a la renta','29,5%; pérdidas arrastrables','LIR'),
('Capital inicial','US$30 MM (2022)','Supuesto del grupo (cubre la compra de US$22 MM más caja de arranque)'),
('Reducción de capital','S/22,6 MM en 2024 (US$6,0 MM)','Dato del usuario (junta del 24/09/2024); no se verificó en una fuente pública'),
('Capital de trabajo','CxC 30 días de ventas; inventarios 30 días y CxP 45 días de costos','Supuesto del grupo (pagos provisionales del trader al embarque)'),
('Deuda','Variable de cierre: cubre el déficit de caja (caja mínima US$5 MM); tasa de 8%','Supuesto: préstamos del Grupo DC y/o prepagos de traders. No se halló deuda pública')]
r+=1; header(ws,r,['Supuesto fijo','Valor','','','','','','Fuente']); r+=1
for a,b,cc in fix:
    ws.cell(r,1,a); ws.cell(r,2,b); ws.cell(r,8,cc).alignment=Alignment(wrap_text=True); r+=1
# Ventas
ws=sheet('Ventas','Construcción de las ventas (NSR) – US$ millones salvo indicación',[58]+[13]*6)
header(ws,4,['Concepto']+Y)
rows(ws,5,[('Cobre fino (TMF)','cu','#,##0'),('Mineral tratado estimado (Mt) = Cu / (ley × recuperación)','mineral','0.00'),('Ritmo equivalente (t/día, 350 días)','tpd','#,##0'),
('Concentrado de Cu (dms) = Cu / 24%','conc','#,##0'),('Cu pagable (millones de lb)','cupay_lb','0.0'),('Plata (miles de oz)','agoz','#,##0'),
('Ingreso bruto Cu','ingCu'),('Ingreso bruto Ag (crédito de subproducto)','ingAg'),('Ingreso bruto total','ingBruto','#,##0.0',True),
('(−) TC/RC de concentrados y RC de Ag','tcrc'),('(−) Flete mina–Callao y depósito','flete'),('Ventas netas (NSR)','ventas','#,##0.0',True)])
# EERR
ws=sheet('EERR','Estado de resultados estimado – US$ millones',[52]+[13]*6)
header(ws,4,['Partida']+Y)
rows(ws,5,[('Ventas netas','ventas','#,##0.0',True),('(−) Costo de operación (mina+planta+energía+personal)','opex'),('(−) G&A y ventas','ga'),
('(−) Depreciación y amortización','dep'),('Utilidad operativa antes de regalía/IEM','ebit_pre','#,##0.0',True),('(−) Regalía minera','regalia'),('(−) IEM','iem'),('(−) Aportes OEFA/Osinergmin','aporte'),
('EBIT','ebit','#,##0.0',True),('EBITDA','ebitda','#,##0.0'),('(−) Gastos financieros','int'),('Utilidad antes de participaciones e IR','ebt'),('(−) Participación de trabajadores 8%','part'),('(−) Impuesto a la renta 29,5%','ir'),
('Utilidad neta','neta','#,##0.0',True),('Margen EBITDA',lambda y:R['ebitda'][y]/R['ventas'][y],'0.0%'),('Margen neto',lambda y:R['neta'][y]/R['ventas'][y],'0.0%'),
('C1 neto (US$/lb Cu pagable)','c1','0.00')])
# Balance y flujo
ws=sheet('Balance','Balance aproximado y flujo de caja – US$ millones (cierre de año)',[52]+[13]*6)
header(ws,4,['Partida']+Y)
r=rows(ws,5,[('Caja','caja'),('Cuentas por cobrar (30 días)','cxc'),('Inventarios (30 días de costo)','inv'),('Activo fijo bruto (compra + capex acumulado)','ppe_b'),('Activo fijo neto','ppe_n'),
('TOTAL ACTIVO',lambda y:R['caja'][y]+R['cxc'][y]+R['inv'][y]+R['ppe_n'][y],'#,##0.0',True),
('Cuentas por pagar (45 días)','cxp'),('Deuda (vinculadas / prepagos; variable de cierre)','deuda'),('Capital social (neto de la reducción)','capital'),('Resultados acumulados','res'),
('TOTAL PASIVO + PATRIMONIO',lambda y:R['cxp'][y]+R['deuda'][y]+R['capital'][y]+R['res'][y],'#,##0.0',True),
('Deuda / EBITDA',lambda y:R['deuda'][y]/R['ebitda'][y],'0.00'),('Deuda / Patrimonio',lambda y:R['deuda'][y]/(R['capital'][y]+R['res'][y]),'0.00')])
header(ws,r+1,['Flujo de caja']+Y)
rows(ws,r+2,[('Flujo operativo (utilidad neta + D&A − Δ capital de trabajo)','fco'),('(−) Capex','capex'),('Flujo de caja libre','fcf','#,##0.0',True),('Reducción de capital pagada','red')])
# Sensibilidad 2025
ws=sheet('Sensibilidad','Sensibilidad del EBIT 2025 (US$ MM) a la ley de cabeza y al costo por tonelada',[34,12,12,12,12])
import itertools
base_v=R['ventas']['2025']; cu25=R['cu']['2025']
header(ws,4,['Ley Cu \\ Costo US$/t',45,52,60,70])
for i,ley in enumerate([0.8,0.9,1.0,1.2]):
    ws.cell(5+i,1,f'{ley:.1f}% Cu')
    for j,ct in enumerate([45,52,60,70]):
        mineral=cu25/(ley/100*0.92)/1e6
        op=base_v-mineral*ct-R['ga']['2025']-R['dep']['2025']
        ebit=op-(R['regalia']['2025']+R['iem']['2025']+R['aporte']['2025'])*(op/R['ebit_pre']['2025'])
        c=ws.cell(5+i,2+j,ebit); c.number_format='#,##0.0'
ws.cell(10,1,'Escenario base: ley 1,0% y costo de US$52/t. Regalía e IEM escalados en proporción a la utilidad operativa (aproximación).').font=I
header(ws,12,['Precio Cu 2026P (US$/lb)',5.0,5.5,6.14,6.5])
for j,p in enumerate([5.0,5.5,6.13756,6.5]):
    v=R['ventas']['2026P']+R['ingCu']['2026P']*(p/6.13756-1); c=ws.cell(13,2+j,v); c.number_format='#,##0.0'
ws.cell(13,1,'Ventas netas 2026P (US$ MM)')
# Clientes
ws=sheet('Clientes','Clientes y canal comercial',[30,60,70])
header(ws,4,['Contraparte','Relación con OCP','Evidencia pública'])
cl=[('Perubar S.A. (Glencore, 99,99%)','Indicado por el usuario: depósito y comprador/trader en el Callao','No se encontró una nota pública que vincule a OCP con Perubar. Perubar almacena, mezcla y embarca concentrados de terceros (glencoreperu.pe)'),
('Glencore Perú S.A.C.','Probable comprador local (exportador de registro) si la venta se hace en el Callao','Glencore Perú es uno de los principales exportadores de la partida 2603 (Tendata/SUNAT). Sin evidencia específica de OCP'),
('Mercuria Energy Group','Indicado por el usuario: comprador/offtaker','No se encontró un offtake ni un prepago público con OCP. Mercuria colocó ~US$2.000 MM en acuerdos de concentrado en 2025 (p. ej., Geotechmin, prepago de US$250 MM)'),
('Trafigura / IXM','Posibles compradores alternativos','IXM tiene depósito en el Callao. Sin evidencia de contratos con OCP'),
('China (fundiciones)','Destino final probable del concentrado','China compra la mayor parte del concentrado de Cu peruano; benchmark TC/RC de US$0 en 2026')]
for i,(a,b,c) in enumerate(cl):
    for j,v in enumerate((a,b,c)): ws.cell(5+i,1+j,v).alignment=Alignment(wrap_text=True,vertical='top')
ws.cell(11,1,'Implicancia: si OCP vende en el Callao a Perubar/Glencore Perú o a la filial local de un trader, el exportador ante SUNAT es el trader y no OCP. Por eso la consulta de exportaciones por el RUC de OCP podría salir baja o vacía, y el FOB de aduanas no serviría para contrastar las ventas.').font=I
# Fuentes
ws=sheet('Fuentes','Datos reales encontrados y fuentes',[45,70,80])
header(ws,4,['Dato','Valor','Fuente / URL'])
F=[('Producción Cu OCP (TMF)','2023: 8.351 | 2024: 14.791 | 2025: 16.545 | ene-ago 2026: 10.528','MINEM, Producción Minera por titular: https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera'),
('Producción Ag OCP (kg finos)','2023: 10.757 | 2024: 20.190 | 2025: 22.130 | ene-ago 2026: 15.534','Ídem'),
('Zinc, plomo y oro','No reportados para OCP','Ídem'),
('Precios Cu/Ag/Zn y TC','Promedios anuales BCRPData','https://estadisticas.bcrp.gob.pe (PN01652XM, PN01655XM, PN01657XM, PN01234PM)'),
('Precios 2027-2028','Cu 570/560 ¢/lb; Zn 140 ¢/lb; petróleo 75/70','MEF, MMM 2027-2030, cuadro C-01 (archivo del repo)'),
('Compra de Cobriza','US$19,7 MM sin IGV (único postor); US$22 MM total; toma de posesión 19/10/2022','Andina: https://andina.pe/agencia/noticia-grupo-dyer-adquiere-mina-cobriza-un-valor-197-millones-903195.aspx ; Energiminas'),
('Trabajadores','604 recontratados','Proactivo / Dipromin (2022)'),
('Capacidad','Planta de 9.100 tms/d; ritmo de 4.000 t/d con ramp-up a 8.000 t/d; MEIA-d con optimización a 12.000 tmd','Rumbo Minero (OCP Cobriza, plan de exploraciones); Energiminas, 27/12/2023'),
('MEIA-d','US$93,3 MM; presentada el 21/12/2023 ante el Senace','https://energiminas.com/2023/12/27/mina-cobriza-grupo-dyer-coriat-planea-destinarus-93-3-millones-para-plan-de-minado-y-optimizacion'),
('ITS','Octavo ITS aprobado por US$8,25 MM (Senace); ITS de US$66,7 MM (dato del usuario)','Proactivo: senace-aprueba-octavo-its-de-cobriza-con-inversion-de-us-8-25-millones'),
('Capex 2024','≥US$50 MM anunciados por Samuel Dyer','Energiminas (dic-2023)'),
('OEFA','RD 01807-2025-OEFA/DFAI: multa de 34,212 UIT. RD 0155-2025: 10,327 UIT. En ambas OCP no entregó sus ingresos, así que no hubo análisis de no confiscatoriedad','https://cdn.www.gob.pe/uploads/document/file/9465822/7750663-resolucion-n-1807-2025-oefa-dfai.pdf ; .../8226264/6871962-resolucion-n-0155-2025-oefa-dfai.pdf'),
('SUNAT – PRICO','OCP figura como Principal Contribuyente Nacional (Intendencia de Principales Contribuyentes Nacionales)','https://www.sunat.gob.pe/legislacion/superin/2024/anexo1-000009-2024.pdf'),
('BCRP Sucursal Huancayo','En jul-2025, la mayor producción de cobre de Huancavelica vino de OCP','https://www.bcrp.gob.pe/docs/Sucursales/Huancayo/2025/presentacion-huancavelica-07-2025.pdf'),
('Disputa tributaria municipal','Alcabala y predial pendientes ante el Tribunal Fiscal e Indecopi','Energiminas, 28/04/2025'),
('Osinergmin','Resolución 1957-2026 (sanción, 12/06/2026)','gob.pe/institucion/osinergmin/normas-legales/8516923-1957-2026'),
('Costos de referencia','Volcan: 49,2 US$/t (2024), 51,7-58,6 (2025), 60,6-70 (2026); Nexa Cerro Lindo: 39,9 US$/t (2025)','Volcan, Análisis y Discusión de la Gerencia (latibex.com); Nexa, comunicado de guidance 2026-2028'),
('TC/RC benchmark','88/8,8 (2023), 80/8,0 (2024), 21,25/2,125 (2025), 0/0 (2026)','Skillings, Crux Investor, SMM (cita a la IEA)'),
('SUNAT exportaciones/importaciones por RUC','NO OBTENIDO: la consulta por exportador de Aduanet pide código captcha y datosabiertos.gob.pe bloqueó el acceso automático (HTTP 418)','www.aduanet.gob.pe – consulta manual pendiente')]
for i,(a,b,c) in enumerate(F):
    for j,v in enumerate((a,b,c)): ws.cell(5+i,1+j,v).alignment=Alignment(wrap_text=True,vertical='top')
wb.save('/home/user/informes-macro/informes/OCP/OCP_EEFF_estimados.xlsx'); print('ok')

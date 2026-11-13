import openpyxl,json,collections
from openpyxl.styles import Font,PatternFill,Alignment
src=openpyxl.load_workbook('informes/OCP/insumos/Veritrade_OCP_importaciones_2019-2026.xlsx',read_only=True,data_only=True).worksheets[0]
rows=[r for r in src.iter_rows(min_row=7,values_only=True) if r[0] and r[4]]
for r in rows:
    if str(r[0])[:4]=='8413': print('8413:',r[4].date(),r[29],round(r[20]),str(r[38])[:110])
D=json.load(open('/tmp/claude-0/imp.json')); M=json.load(open('/tmp/claude-0/ocp_model.json'))
f='informes/OCP/OCP_EEFF_estimados.xlsx'; wb=openpyxl.load_workbook(f)
if 'Importaciones' in wb.sheetnames: del wb['Importaciones']
ws=wb.create_sheet('Importaciones',2)
H=PatternFill('solid',fgColor='1F3864'); HF=Font(bold=True,color='FFFFFF'); I=Font(italic=True,size=9,color='555555')
ws['A1']='Importaciones de OCP por partida y año (Veritrade / SUNAT, DUA/DAM; US$ CIF)'; ws['A1'].font=Font(bold=True,size=13)
ws['A2']='DATO REAL: 168 DUA del importador RUC 20608321731, ene-2019 a nov-2026 (no hay registros antes de 2023)'; ws['A2'].font=Font(bold=True,color='C00000')
for c,w in zip('ABCDEFGH',[10,58,12,12,14,14,14,40]): ws.column_dimensions[c].width=w
yrs=['2023','2024','2025','2026']
def hdr(r,v):
    for j,x in enumerate(v): c=ws.cell(r,1+j,x); c.fill=H; c.font=HF; c.alignment=Alignment(horizontal='center',wrap_text=True)
hdr(4,['Partida (4 díg.)','Descripción']+[y if y!='2026' else '2026 (ene-nov)' for y in yrs]+['Total','Bien principal'])
bien={'8421':'Filtros prensa MATEC (Italia), agua y relaves; sep-2025 y ene-feb 2026','8413':'Bomba ABEL HMQ (Alemania), abr-2026','8474':'Partes de chancado y molienda; zarandas','8429':'Topador de ruedas RHINO RWD235','9027':'Estación de calidad de aire','9015':'Equipos de topografía'}
r=5
for k,v in sorted(D['p4'].items(),key=lambda x:-sum(x[1].values())):
    ws.cell(r,1,k); ws.cell(r,2,D['desc'][k][:70])
    for j,y in enumerate(yrs): c=ws.cell(r,3+j,v.get(y,0)/1e6); c.number_format='0.000'
    c=ws.cell(r,7,sum(v.values())/1e6); c.number_format='0.000'; ws.cell(r,8,bien.get(k,'')); r+=1
ws.cell(r,2,'TOTAL (US$ MM)').font=Font(bold=True)
for j,y in enumerate(yrs): c=ws.cell(r,3+j,D['yr'][y]/1e6); c.number_format='0.000'; c.font=Font(bold=True)
c=ws.cell(r,7,sum(D['yr'].values())/1e6); c.number_format='0.000'; c.font=Font(bold=True); r+=1
ws.cell(r,2,'Capex estimado por el grupo (US$ MM)')
for j,y in enumerate(['2023','2024','2025','2026P']): ws.cell(r,3+j,M['R']['capex'][y])
r+=1; ws.cell(r,2,'Importaciones directas / capex estimado')
for j,(y,yc) in enumerate(zip(yrs,['2023','2024','2025','2026P'])): c=ws.cell(r,3+j,D['yr'][y]/1e6/M['R']['capex'][yc]); c.number_format='0.0%'
r+=2; hdr(r,['País de origen','','US$ MM']); r+=1
for p,v in sorted(D['pais'].items(),key=lambda x:-x[1])[:8]:
    ws.cell(r,1,p); c=ws.cell(r,3,v/1e6); c.number_format='0.00'; r+=1
notas=['Lectura: las importaciones directas son capex ambiental y de planta (agua/relaves, bombeo, chancado), coherente con el ITS de relaves y agua y con el escalamiento de la planta. Equivalen a ~6% del capex estimado en 2025 y ~13% en 2026: el resto del capex es obra civil, desarrollo de mina y compras locales a distribuidores (p. ej. equipos nacionalizados por terceros).',
'Los insumos operativos (explosivos, reactivos, combustible, bolas de molienda) NO aparecen como importación directa: se compran en el mercado local (en soles o en dólares), así que su costo depende de la inflación local y del tipo de cambio por intermedio de los proveedores.',
'Exportaciones: Veritrade no registra exportaciones con el RUC de OCP. Es coherente con la venta local del concentrado a traders (Perubar/Glencore Perú, Mercuria), que son los exportadores de registro.',
'Fuente: Veritrade (base SUNAT de DUA/DAM), archivo informes/OCP/insumos/Veritrade_OCP_importaciones_2019-2026.xlsx, provisto por el usuario.']
for n in notas:
    r+=1; ws.cell(r,1,n).font=I; ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=8); ws.cell(r,1).alignment=Alignment(wrap_text=True); ws.row_dimensions[r].height=45
# update Fuentes row
fs=wb['Fuentes']
for row in fs.iter_rows(min_row=5):
    if row[0].value and str(row[0].value).startswith('SUNAT exportaciones'):
        row[0].value='SUNAT exportaciones/importaciones por RUC'
        row[1].value='IMPORTACIONES: US$7,27 MM CIF (2023: 0,006 · 2024: 0,14 · 2025: 2,53 · ene-nov 2026: 4,59), con detalle en la hoja Importaciones. EXPORTACIONES: no hay registros con el RUC de OCP (venta local a traders).'
        row[2].value='Veritrade (base SUNAT), archivo provisto por el usuario. La consulta directa en Aduanet pide captcha'
wb.save(f); print('ok')

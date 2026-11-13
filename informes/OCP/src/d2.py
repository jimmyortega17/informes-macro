import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.family']='Carlito'
G='#008000'; R='#C00000'; B='#1F3864'
fig,ax=plt.subplots(figsize=(17,7.8),dpi=200); ax.set_xlim(0,162); ax.set_ylim(0,78); ax.axis('off')
W=13;H=10
def box(x,y,lab,arr,num,w=W,h=H,fc='white'):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.3',fc=fc,ec='black',lw=1.4))
    c={'↑':G,'↓':R,'':B}[arr]
    ax.text(x-0.4,y+2.2,lab,ha='right',va='center',fontsize=15,fontweight='bold',color=B)
    if arr: ax.text(x+0.4,y+2.2,arr,ha='left',va='center',fontsize=22,fontweight='bold',color=c)
    ax.text(x,y-2.4,num,ha='center',va='center',fontsize=9,linespacing=1.15)
def arrow(x1,y1,x2,y2,dash=False):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=B,lw=1.8,ls='--' if dash else '-',mutation_scale=16,shrinkA=0,shrinkB=0))
Y0=46; xs=[9,25,41,57,73,89,105,121,137,153]
ax.add_patch(FancyBboxPatch((1,64),26,11,boxstyle='round,pad=0.3',fc='#F2F2F2',ec='black',lw=1.4))
ax.text(14,72,'Y  vs  Yn     Si: Y > Yn',ha='center',fontsize=13,fontweight='bold',color=B)
ax.text(14,67.3,'PBI 2026: 3,2% ≥ potencial ≈3,0%\n(BCRP, RI set-2026)',ha='center',va='center',fontsize=8.8)
data=[('P','↑','Inflación Lima\n5,25% (oct-26)'),('BC','','BCRP sube i\n12-nov-26'),('H','↓','Menor emisión\nprimaria'),('M','↓','Liquidez soles\n+16,7%, se modera'),('i','↑','Tasa ref. 4,25%→4,50%\nr real ex ante 1,45%'),('I','↓','Inv. privada\n+14,0% → +6,5%'),('Z','↓','Demanda interna\n6,2% → 3,7%'),('Y','↓','PBI 3,2% → 3,0%\n(2027)'),('P','↓','Inflación 5,25%\n→ 2,5% (2027)'),('Pᵉ','↓','Expectativas\n3,05% → ≈2,5%')]
for x,(l,a,n) in zip(xs,data): box(x,Y0,l,a,n,w=15.5 if l=='i' else W)
box(9,16,'Pᵉ','','Expectativas\n3,05% (> meta 3%)')
box(89,70,'E','↓','TC S/3,41:\nsol se aprecia')
box(105,70,'X','↓','Export. en soles ↓\nOCP: −S/25 MM*')
box(89,16,'E','↓','Importaciones\nmás baratas')
ax.add_patch(FancyBboxPatch((113,4),16,25,boxstyle='round,pad=0.3',fc='white',ec='black',lw=1.4))
for yy,l,a,n in [(25,'C','↓','Consumo 3,6%→3,4%'),(17,'I','↓','Inversión 14%→6,5%'),(9,'IM','↑','Import. +10,8% (2026)')]:
    ax.text(119.5,yy+0.6,l,ha='right',fontsize=14,fontweight='bold',color=B,va='center'); ax.text(120.3,yy+0.6,a,fontsize=19,fontweight='bold',color=G if a=='↑' else R,va='center')
    ax.text(121,yy-2.6,n,ha='center',fontsize=8.3)
arrow(9,63.7,9,51.3); arrow(9,21.3,9,40.7)
for a,b in zip(xs[:-1],xs[1:]):
    wa=7.6 if a==73 else 6.8; wb=7.6 if b==73 else 6.8
    arrow(a+wa,Y0,b-wb,Y0)
arrow(78,51.3,84,64.7); arrow(95.8,70,98.2,70); arrow(105,64.7,105,51.3)
arrow(78,40.7,84,21.3); arrow(95.8,14,112.7,10)
arrow(121,40.7,121,29.3); arrow(115,29.3,108,40.7)
# bracket under P, Pe and dashed feedback
ax.plot([131,131,159,159],[40,38,38,40],color=B,lw=1.4); ax.plot([145,145],[38,36.5],color=B,lw=1.4)
ax.plot([145,145,148],[36.5,2,2],ls='',)
ax.plot([145,145,73],[36.5,1.5,1.5],ls='--',color=B,lw=1.6); arrow(73,1.5,73,40.7,dash=True)
ax.text(93,2.9,'Cuando P y Pᵉ bajan, el BCRP vuelve a reducir i (retroalimentación)',ha='center',fontsize=9.5,style='italic',color=B)
fig.text(0.01,0.005,'* Cada 10 céntimos de apreciación del sol reducen en ≈S/25 MM las ventas anuales estimadas de OCP expresadas en soles (ventas 2026P: US$249 MM, estimadas por el grupo).',fontsize=8.3)
plt.savefig('esquema_transmision_ocp.png',bbox_inches='tight',facecolor='white')

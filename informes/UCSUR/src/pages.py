import subprocess, sys, json, re, os
pdf=sys.argv[1]; n=int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
txt=[subprocess.run(['pdftotext','-f',str(i),'-l',str(i),pdf,'-'],capture_output=True,text=True).stdout for i in range(1,n+1)]
start=next(i for i,t in enumerate(txt) if 'SECCIÓN 1' in t)  # 0-based pdf index of section page 1
def find(key):
    return next(i for i,t in enumerate(txt) if f'⟦{key}⟧' in t)-start+1
P={}
for k,(a,b) in {'int':('int_ini','int_fin'),'peru':('peru_ini','peru_fin'),'cruces':('cruces_ini','cruces_fin'),'cxc':('cruces_ini','cxc_fin')}.items():
    P[k]=[find(a),find(b)]
for k in ('razint','razperu'): P[k]=[find(k)]*2
print(json.dumps(P)); json.dump(P,open(sys.argv[2],'w'))

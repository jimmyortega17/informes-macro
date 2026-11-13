import subprocess, sys, json, re
pdf=sys.argv[1]; n=int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
txt=[subprocess.run(['pdftotext','-f',str(i),'-l',str(i),pdf,'-'],capture_output=True,text=True).stdout for i in range(1,n+1)]
start=next(i for i,t in enumerate(txt) if '⟦s1int⟧' in t)
P={k:[next(i for i,t in enumerate(txt) if f'⟦{k}⟧' in t)-start+1] for k in ('s1int','s1peru','s2desc','s2imp','s3')}
print(n, json.dumps(P)); json.dump(P,open(sys.argv[2],'w'))

#!/usr/bin/env python3
"""measure_css.py - Deriva contraste de pares de colores presentes en los heroes D2.
No rendering; solo estima. Util cuando no hay browser disponible."""
import re, json, os, glob

def norm(tok):
    tok=tok.strip()
    m=re.match(r'^#([0-9a-f]{3,6})$', tok, re.I)
    if m:
        h=m.group(1)
        if len(h)==3: h=''.join(c*2 for c in h)
        return tuple(int(h[i:i+2],16) for i in (0,2,4))
    return None

def lum(rgb):
    def f(c):
        c/=255.0
        return c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(rgb[0])+.7152*f(rgb[1])+.0722*f(rgb[2])

def contrast(a,b):
    la,lb=lum(a),lum(b)
    bigger,smaller=(la,lb) if la>lb else (lb,la)
    return round((bigger+.05)/(smaller+.05),2)

out=[]
for f in sorted(glob.glob('studies/design/recreaciones/hero-*.html')):
    src=open(f).read()
    # CSS vars: --name:#hex; background: var(--x)
    pairs=set()
    # vars
    vars={}
    for k,v in re.findall(r'--(\w+)\s*:\s*(#[0-9a-f]{3,6})', src, re.I):
        vars[k]=norm(v)
    # paint combos: color/background-color
    combos=[]
    # try var usage pairs
    if 'fg' in vars and 'bg' in vars: combos.append(('fg','bg'))
    if 'fg' in vars and 'bg-2' in vars: combos.append(('fg','bg-2'))
    if 'muted' in vars and 'bg' in vars: combos.append(('muted','bg'))
    if 'accent' in vars and 'bg' in vars: combos.append(('accent','bg'))
    row={'file':os.path.basename(f),'vars':vars}
    ratios={}
    for a,b in combos:
        if vars.get(a) and vars.get(b):
            ratios[f'{a}_on_{b}']=contrast(vars[a],vars[b])
    row['measured']=ratios
    out.append(row)
print(json.dumps(out,indent=1,ensure_ascii=False))

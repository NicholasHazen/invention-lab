#!/usr/bin/env python3
"""Rebuild three original vector teaching figures; standard library only."""
from pathlib import Path
import math
from actuator_sizing import Rotary, triangular

OUT = Path(__file__).resolve().parent.parent / 'assets'
OUT.mkdir(exist_ok=True)


def start(title, subtitle, height=720):
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {height}" role="img" aria-label="{title}">
<rect width="1120" height="{height}" fill="#f5f3ed"/>
<style>text{{font-family:Arial,sans-serif;fill:#1c3339;font-size:21px}}.title{{font-size:32px;font-weight:700}}.small{{font-size:18px}}.axis{{stroke:#647578;stroke-width:2}}.grid{{stroke:#d7dedb;stroke-width:1}}</style>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#32525a"/></marker></defs>
<text x="44" y="52" class="title">{title}</text><text x="44" y="86">{subtitle}</text>''']


def text(x,y,s,cls=''):
    return f'<text x="{x}" y="{y}" class="{cls}">{s}</text>'


def line(x1,y1,x2,y2,color='#32525a',width=2,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" {extra}/>'


def path(points,color,width=3,extra=''):
    return '<polyline fill="none" stroke="'+color+'" stroke-width="'+str(width)+'" points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" '+extra+'/>'


def save(name, parts):
    (OUT/name).write_text('\n'.join(parts+['</svg>']))


p=Rotary(1e-5)
s=start('Torque changes during the move','Horizontal → vertical in 1 s • output shaft • moving-friction model, no stiction')
x=lambda t: 110+930*t
y=lambda tau: 390-640*tau
for val in (0,.1,.2,.3):
    s += [line(110,y(val),1040,y(val),'#d7dedb',1), text(43,y(val)+7,f'{val:.1f}')]
s += [text(43,139,'N·m'),line(110,159,110,410),line(110,390,1040,390)]
for val in (0,.25,.5,.75,1):
    s += [line(x(val),390,x(val),398), text(x(val)-13,430,f'{val:g}')]
s += [text(955,465,'Time (s)')]
points=[(i/300,triangular(i/300,1,math.pi/2)) for i in range(301)]
s += [path([(x(t),y(p.gravity_max*math.cos(theta))) for t,(theta,_,_) in points],'#258071',4)]
for lo,hi,a in ((0,.5,p.acceleration),(.5,1,-p.acceleration)):
    pts=[(lo+(hi-lo)*i/150) for i in range(151)]
    s += [path([(x(t),y(p.gravity_max*math.cos(triangular(t,1,p.angle)[0])+p.load_inertia*a+p.friction)) for t in pts],'#b95631',4),
          line(x(lo),y(p.load_inertia*a),x(hi),y(p.load_inertia*a),'#5775a4',3)]
s += [line(x(.5),y(.201164808+p.load_inertia*p.acceleration+.01),x(.5),y(.201164808-p.load_inertia*p.acceleration+.01),'#b95631',4),
      line(x(.5),159,x(.5),410,'#879397',1,'stroke-dasharray="5 5"'),
      text(600,157,'Acceleration reverses at 45°','small')]
for xx,col,label in ((80,'#b95631','Total required'),(385,'#258071','Gravity'),(630,'#5775a4','Acceleration term')):
    s += [line(xx,492,xx+40,492,col,4), text(xx+50,499,label)]
s += [text(80,548,'Total includes +0.010 N·m assumed moving friction.'),
      text(80,582,'Envelope: 0.311873 N·m. The initial upward limit reaches it in this model.'),
      text(80,616,'Negative torque near the end opposes positive motion: braking can return energy.'),
      text(80,672,'Original calculated diagram • not measured hardware behavior','small')]
save('sizing-torque-trace.svg',s)

s=start('Where does the feedback come from?','Choose the measured object before choosing gains • conceptual signal map, not wiring',800)
def box(x,y,w,h,label,color='#e1e9e2'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" stroke="#728b89"/>'+text(x+18,y+h/2+8,label)
s += [box(60,150,230,80,'Motor + shaft'),box(405,150,310,80,'Belt / gears / coupling'),box(825,150,230,80,'Output + arm'),
      line(292,190,400,190,extra='marker-end="url(#arrow)"'),line(717,190,819,190,extra='marker-end="url(#arrow)"'),
      text(425,265,'Clearance + compliance','small'),
      line(175,232,175,295),line(940,232,940,295),
      box(60,295,300,65,'Motor encoder','#e1e8f2'),box(755,295,300,65,'Load encoder','#f3e0d4'),
      text(62,393,'Sees rotor motion','small'),text(757,393,'Sees output motion','small'),
      text(60,442,'Motor angle ÷ ratio estimates output angle. Transmission errors break that estimate.'),
      line(44,467,1076,467,'#b9c9c7',1),
      text(60,509,'A typical cascaded command path'),
      box(60,540,255,85,'Position loop'),box(425,540,255,85,'Velocity loop'),box(790,540,265,85,'Current loop'),
      line(318,582,420,582,extra='marker-end="url(#arrow)"'),line(684,582,785,582,extra='marker-end="url(#arrow)"'),
      text(329,557,'speed','small'),text(695,557,'torque','small'),
      text(75,665,'Measured position','small'),text(440,665,'Measured velocity','small'),text(805,665,'Measured current','small'),
      line(185,651,185,630,extra='marker-end="url(#arrow)"'),line(550,651,550,630,extra='marker-end="url(#arrow)"'),line(925,651,925,630,extra='marker-end="url(#arrow)"'),
      text(60,722,'Each stage has limits. The actual drive determines sensor assignment and tuning.'),
      text(60,760,'Motor current can estimate motor torque; it does not directly measure fingertip force.','small')]
save('sizing-feedback-path.svg',s)

s=start('A loose gap and a flexible structure differ','Synthetic data only • input fixed • tangential force and tip deflection at 100 mm radius',780)
xx=lambda f: 535+1460*f
yy=lambda d: 368-132*d
for val in (-1,-.5,0,.5,1):
    s += [line(170,yy(val),900,yy(val),'#d7dedb',1),text(112,yy(val)+7,f'{val:g}')]
for val in (-.2,-.1,0,.1,.2):
    s += [line(xx(val),180,xx(val),550,'#d7dedb',1),text(xx(val)-20,580,f'{val:g}')]
s += [line(170,yy(0),920,yy(0),extra='marker-end="url(#arrow)"'),line(xx(0),550,xx(0),170,extra='marker-end="url(#arrow)"'),
      text(54,144,'Tip deflection (mm)'),text(750,614,'Applied force (N)')]
for sign,color in ((1,'#b95631'),(-1,'#258071')):
    s += [path([(xx(sign*.1),yy(sign*.6)),(xx(sign*.2),yy(sign*1))],color,4),
          path([(xx(0),yy(sign*.2)),(xx(sign*.1),yy(sign*.6))],color,3,'stroke-dasharray="6 5"')]
    for f,d in ((sign*.1,sign*.6),(sign*.2,sign*1)):
        s += [f'<circle cx="{xx(f)}" cy="{yy(d)}" r="7" fill="{color}"/>']
s += [line(565,yy(.2),565,yy(-.2),extra='marker-start="url(#arrow)" marker-end="url(#arrow)"'),
      text(590,347,'0.40 mm gap','small'),text(685,198,'Slope = 4 mm/N','small'),
      text(60,660,'Branch slopes → elastic stiffness: 2.5 N·m/rad.'),
      text(60,700,'Zero-force intercept separation → apparent lost motion: 0.229°.'),
      text(60,744,'Extrapolation also includes friction / hysteresis / fixture error; it is not pure backlash proof.','small')]
save('sizing-compliance.svg',s)
print('Wrote three sizing figures to',OUT)

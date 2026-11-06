"""Regenerate the guide's original layout references. Python 3, standard library only.

These are dimensioned design studies, not fabrication drawings or rated assemblies.
Run from any directory: python3 generate_layouts.py
"""
from pathlib import Path
import csv, html, json, math

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / 'assets'
ASSETS.mkdir(exist_ok=True)

def belt_length(c, big, small):
    d = big-small
    return 2*math.sqrt(c*c-d*d)+math.pi*(big+small)+2*d*math.asin(d/c)

R, r = 60*2/(2*math.pi), 20*2/(2*math.pi)
lo, hi = R-r+.001, 200
for _ in range(80):
    mid=(lo+hi)/2
    if belt_length(mid,R,r)<200: lo=mid
    else: hi=mid
C=(lo+hi)/2

studies = {
 'belt-joint': {
  'title':'Belt-driven rotary joint', 'units':'mm',
  'scope':'Concept component envelopes and pitch geometry; no tooth profiles, selected motor, fasteners, fits, or fabrication release.',
  'parameters': [('pitch','mm',2),('motor_teeth','',20),('output_teeth','',60),('belt_pitch_length','mm',200),('center_distance','mm',C),('shaft_diameter','mm',8),('bearing_od','mm',22),('bearing_width','mm',7),('bearing_spacing','mm',30),('belt_plane','mm',15),('pulley_envelope_width','mm',10),('installation_travel','mm',4),('arm_length','mm',100)],
  'notes':['200 mm belt is a candidate pitch length, not a selected SKU. Installation travel must be checked against selected manufacturer guidance.','Bearing centres z=0,30; output pulley z=10..20; 6.5 mm space per side before hub/retainer allowances.','Motor envelope 42 x 42 x 40; its mounting pattern, shaft and pulley hub remain unresolved.'],
 },
 'screw-stage': {
  'title':'Horizontal lead-screw stage', 'units':'mm',
  'scope':'Screw, nut, guide and support envelopes; no thread form, bearing selection, fastening or rated speed/load.',
  'parameters':[('travel','mm',50),('lead','mm',2),('screw_diameter','mm',8),('screw_overall','mm',140),('nut_length','mm',20),('carriage_length','mm',30),('travel_start_x','mm',40),('travel_end_x','mm',90),('thread_start_x','mm',25),('thread_end_x','mm',105),('guide_offset','mm',25),('guide_start_x','mm',20),('guide_end_x','mm',110),('screw_axis_height','mm',20),('mechanical_stop_low_x','mm',20),('mechanical_stop_high_x','mm',110)],
  'notes':['Useful carriage centre x=40..90; guide block extends +/-15; nut extends +/-10.','Fixed support x=0..15, float support x=115..130. Thread region x=25..105; both nut-end margins 5 mm.','Screw x=-10..130 includes 10 mm coupling engagement; motor shaft ends x=-11 leaving 1 mm between shaft ends. Coupling bores/engagement require selection.','Stop contact planes x=20,110 give block-centre stops x=35,95: 5 mm beyond each commanded endpoint. Sensor trigger and stopping margin still require selected hardware.'],
 },
 'tendon-gripper': {
  'title':'One-finger tendon study', 'units':'mm',
  'scope':'Constant-radius sector and spool envelopes, not groove/anchor/spring or fabrication-ready finger geometry.',
  'parameters':[('tip_moment_arm','mm',30),('tendon_radius','mm',10),('spool_radius','mm',8),('finger_rotation','deg',60),('tendon_travel','mm',10*math.pi/3),('spool_rotation','deg',75),('hinge_diameter','mm',4),('finger_thickness','mm',8),('clevis_gap','mm',8.6),('cheek_thickness','mm',4),('tendon_plane_z','mm',4),('spool_center_x','mm',-45),('spool_center_y','mm',18)],
  'notes':['Tip force is perpendicular to the 30 mm arm; other contact directions change the moment.','Tendon remains tangent to the 10 mm circular sector at y=10; anchored wrap must cover the whole 60 degree excursion.','Clevis cheeks z=-4.3..-0.3 and 8.3..12.3, finger z=0..8; nominal side clearance 0.3 mm each, calibrated before fabrication.'],
 }
}

def write_params(name,s):
    with (HERE/f'{name}-parameters.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['name','unit','value','status'])
        for n,u,v in s['parameters']:w.writerow([n,u,round(v,9),'study input; not manufacturer specification'])
    (HERE/f'{name}-layout.json').write_text(json.dumps(s,indent=2)+'\n')

class DXF:
    def __init__(self): self.entities=[]
    def add(self,*pairs):
        self.entities.extend(str(v) for p in pairs for v in p)
    def line(self,x1,y1,x2,y2,layer='REFERENCE'):
        self.add((0,'LINE'),(8,layer),(10,x1),(20,y1),(30,0),(11,x2),(21,y2),(31,0))
    def circle(self,x,y,r,layer='REFERENCE'):
        self.add((0,'CIRCLE'),(8,layer),(10,x),(20,y),(30,0),(40,r))
    def rect(self,x,y,w,h,layer):
        for a,b in [((x,y),(x+w,y)),((x+w,y),(x+w,y+h)),((x+w,y+h),(x,y+h)),((x,y+h),(x,y))]:self.line(*a,*b,layer)
    def save(self,name):
        # AC1015 and INSUNITS=4 explicitly encode millimetres; pure line/circle geometry.
        header=['0','SECTION','2','HEADER','9','$ACADVER','1','AC1015','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
        (HERE/name).write_text('\n'.join(header+self.entities+['0','ENDSEC','0','EOF'])+'\n')

d=DXF();d.circle(0,0,R,'OUTPUT_PITCH');d.circle(C,0,r,'MOTOR_PITCH');d.circle(0,0,4,'SHAFT');d.circle(0,0,11,'BEARING');d.rect(C-21,-21,42,42,'MOTOR_ENVELOPE');d.line(0,0,C,0,'CENTRES')
a=math.asin((R-r)/C)
for sign in [-1,1]:d.line(R*math.sin(a),sign*R*math.cos(a),C+r*math.sin(a),sign*r*math.cos(a),'BELT_TANGENT')
d.save('belt-joint-front.dxf')
d=DXF();d.rect(-15,-4,60,8,'SHAFT')
for z in [-3.5,26.5]:d.rect(z,-11,7,22,'BEARING')
d.rect(10,-R,10,2*R,'PULLEY_ENVELOPE');d.line(0,-25,0,25,'STATION');d.line(30,-25,30,25,'STATION');d.save('belt-joint-axial.dxf')
d=DXF();d.rect(-10,-4,140,8,'SCREW_ENVELOPE');d.rect(0,-14,15,28,'FIXED_SUPPORT');d.rect(115,-14,15,28,'FLOAT_SUPPORT');d.rect(20,21,90,8,'GUIDE');d.rect(50,12,30,26,'BLOCK_MID_TRAVEL');d.rect(55,-8,20,16,'NUT_MID_TRAVEL');d.line(40,-20,90,-20,'USEFUL_TRAVEL');d.rect(15,12,5,26,'STOP');d.rect(110,12,5,26,'STOP');d.save('screw-stage-plan.dxf')
d=DXF();d.circle(0,20,4,'SCREW');d.rect(-8,12,16,16,'NUT');d.rect(21,8,8,6,'GUIDE');d.rect(12,12,26,12,'BLOCK');d.rect(-8,28,46,4,'CARRIAGE');d.rect(-18,0,62,6,'BASE');d.save('screw-stage-end.dxf')
d=DXF();d.circle(0,0,10,'SECTOR_PITCH');d.circle(0,0,2,'HINGE');d.circle(-45,18,8,'SPOOL_PITCH');d.line(-45,10,0,10,'TENDON');d.line(0,0,30,0,'FINGER_START');d.line(0,0,15,30*math.sin(math.pi/3),'FINGER_END');d.rect(24,-9,8,5,'OPEN_STOP');d.rect(8,30*math.sin(math.pi/3)+2,6,5,'CLOSED_STOP');d.save('tendon-gripper-front.dxf')
d=DXF();d.rect(0,-10,8,20,'FINGER');d.rect(-4.3,-12,4,24,'CHEEK');d.rect(8.3,-12,4,24,'CHEEK');d.rect(-7,-2,22,4,'PIN');d.line(4,-15,4,15,'TENDON_PLANE');d.save('tendon-gripper-axial.dxf')

class SVG:
    def __init__(self,title,sub,height=680):
        self.p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(sub)}</desc><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto-start-reverse"><path d="M0,0 L6,3 L0,6" fill="none" stroke="#536577"/></marker></defs><style>text{{font-family:system-ui,sans-serif;fill:#203347;font-size:19px}}.small{{font-size:16px}}.label{{font-size:17px;font-weight:600}}.muted{{fill:#536577}}.dimension{{stroke:#536577;stroke-width:1.5;marker-start:url(#arr);marker-end:url(#arr)}}.axis{{stroke:#8e9ba5;stroke-width:1.3;stroke-dasharray:8 5}}.part{{stroke:#236b86;stroke-width:2;fill:#d9eef4}}.metal{{stroke:#657683;stroke-width:2;fill:#e5e9ed}}.drive{{stroke:#b46a23;stroke-width:2;fill:#f8e4cc}}.path{{stroke:#bc6332;stroke-width:4;fill:none}}.ghost{{fill:none;stroke:#8675aa;stroke-width:2;stroke-dasharray:7 5}}</style><rect width="1200" height="{height}" fill="#fcfcf9"/>']
        self.text(38,42,title,26);self.text(38,72,sub,17,'muted')
    def text(self,x,y,t,size=19,cl=''):
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cl}" style="font-size:{size}px">{html.escape(t)}</text>')
    def line(self,x1,y1,x2,y2,cl='axis'):
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cl}"/>')
    def rect(self,x,y,w,h,cl='part'):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" class="{cl}"/>')
    def circle(self,x,y,r,cl='part'):
        self.p.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{cl}"/>')
    def dim(self,x1,y1,x2,y2,t,tx=None,ty=None):
        self.line(x1,y1,x2,y2,'dimension');self.text(tx if tx is not None else (x1+x2)/2-28,ty if ty is not None else (y1+y2)/2-10,t,16)
    def save(self,name):(ASSETS/name).write_text(''.join(self.p)+'</svg>\n')

s=SVG('Belt joint: one view locates axes; the other separates parts','Design study · millimetres · pitch circles are not manufactured pulley profiles',720)
s.text(45,122,'A  LOOK ALONG THE OUTPUT SHAFT',18,'label');s.text(650,122,'B  LOOK ACROSS THE OUTPUT SHAFT',18,'label')
x,y,k=150,280,4
s.circle(x,y,R*k,'drive');s.circle(x+C*k,y,r*k,'drive');s.circle(x,y,11*k,'metal');s.circle(x,y,4*k,'metal');s.rect(x+C*k-84,y-84,168,168,'ghost')
for sign in [-1,1]:s.line(x+R*math.sin(a)*k,y+sign*R*math.cos(a)*k,x+(C+r*math.sin(a))*k,y+sign*r*math.cos(a)*k,'path')
s.line(x-90,y,x+C*k+90,y);s.dim(x,y+128,x+C*k,y+128,f'C = {C:.3f} mm',x+45,y+118)
s.text(52,458,'60 teeth · pitch Ø38.197',17);s.text(320,458,'20 teeth · pitch Ø12.732',17);s.text(80,492,'Motor footprint is a generic 42 mm square.',16,'muted');s.text(80,518,'Move motor along the centre line to install/tension.',16,'muted')
x,y,k=730,280,7
s.rect(x-15*k,y-4*k,60*k,8*k,'metal')
for z in [-3.5,26.5]:
 s.rect(x+z*k,y-11*k,7*k,7*k,'part');s.rect(x+z*k,y+4*k,7*k,7*k,'part')
s.rect(x+10*k,y-R*k,10*k,(R-4)*k,'drive');s.rect(x+10*k,y+4*k,10*k,(R-4)*k,'drive')
s.line(x,y-155,x,y+115);s.line(x+30*k,y-155,x+30*k,y+115);s.dim(x,y+132,x+30*k,y+132,'30 mm station spacing',x+21,y+157)
s.text(657,466,'A: z = 0',17);s.text(940,466,'B: z = 30',17);s.text(772,178,'Pulley: z = 10…20',16);s.text(754,492,'Bearing width: 7 · shaft Ø8',16);s.text(754,518,'6.5 mm per side before hubs / retainers',16)
s.dim(680,564,790,564,'',680,560);s.text(805,570,'Insert shaft from this end; reserve 60 mm access.',16)
s.rect(40,605,1120,78,'ghost');s.text(58,634,'Load path: arm → metal shaft → two bearings → housing → base.',18,'label');s.text(58,661,'Belt tension also loads both shafts. Torque alone does not determine bearing load.',17)
s.save('design-belt-layout.svg')

s=SVG('Belt joint: build the dependencies before the details','Four modeling checkpoints · each frame is an instructional sketch, not a Fusion screenshot',580)
for i,(title,lines) in enumerate([
 ('1  Locate axes',['Origin = output axis','Constrain the second centre','with center_distance.']),
 ('2  Reserve the stack',['Offset planes at z = 0 / 15 / 30','Bearings flank the belt plane','Inspect the 6.5 mm gaps.']),
 ('3  Give loads a route',['Separate shaft / bearings / base','Add two accessible cartridges','Keep belt and tools unobstructed.']),
 ('4  Finish for printing',['Fit coupon before full bracket','Bed-edge chamfer; root fillets','Check slicer paths and access.'])]):
 xx=30+i*295;s.rect(xx,105,280,420,'ghost');s.text(xx+14,138,title,18,'label')
 for j,t in enumerate(lines):s.text(xx+14,410+j*29,t,15)
 if i==0:
  s.circle(xx+72,260,49,'drive');s.circle(xx+209,260,18,'drive');s.dim(xx+72,343,xx+209,343,'C',xx+134,330)
 elif i==1:
  s.rect(xx+45,248,190,18,'metal');s.rect(xx+75,213,21,86);s.rect(xx+183,213,21,86);s.rect(xx+126,185,28,140,'drive');s.line(xx+140,172,xx+140,350)
 elif i==2:
  s.rect(xx+30,320,220,20);s.rect(xx+75,220,24,100);s.rect(xx+180,220,24,100);s.line(xx+45,250,xx+240,250,'path')
 else:
  s.p.append(f'<path d="M{xx+55},320 L{xx+55},220 L{xx+100},220 L{xx+100},282 Q{xx+100},300 {xx+118},300 L{xx+225},300 L{xx+225},320 Z" class="part"/>');s.text(xx+44,360,'Root radius ≠ fit edge',16)
s.save('design-belt-steps.svg')

s=SVG('Screw stage: travel belongs to the carriage centre','Design study · useful travel is smaller than the screw envelope · not a screw/guide selection',710)
s.text(45,120,'A  PLAN VIEW: X RUNS ALONG THE SCREW',18,'label');x,y,k=190,290,4
s.rect(x-10*k,y-4*k,140*k,8*k,'metal');s.rect(x,y-14*k,15*k,28*k,'part');s.rect(x+115*k,y-14*k,15*k,28*k,'part');s.rect(x+20*k,y-29*k,90*k,8*k,'metal');s.rect(x+50*k,y-38*k,30*k,26*k,'part');s.rect(x+55*k,y-8*k,20*k,16*k,'drive')
for q in [25,75]:s.rect(x+q*k,y-38*k,30*k,26*k,'ghost')
for q in [15,110]:s.rect(x+q*k,y-38*k,5*k,26*k,'drive')
s.line(x+65*k,y-8*k,x+65*k,y-12*k,'path');s.dim(x+40*k,y+125,x+90*k,y+125,'50 mm useful centre travel',x+42*k,y+155)
s.text(46,445,'Fixed axial support',16);s.text(824,445,'Floating radial support',16);s.text(915,170,'Guide carries',16);s.text(915,196,'side loads /',16);s.text(915,222,'moments.',16)
s.text(188,475,'Thread region x = 25…105; nut length 20; 5 mm end margin at each useful endpoint.',16)
s.text(48,529,'B  END VIEW',18,'label');x,y,k=215,655,3.2
s.rect(x-18*k,y-6*k,62*k,6*k);s.circle(x,y-20*k,4*k,'metal');s.rect(x-8*k,y-28*k,16*k,16*k,'drive');s.rect(x+21*k,y-14*k,8*k,6*k,'metal');s.rect(x+12*k,y-24*k,26*k,12*k);s.rect(x-8*k,y-32*k,46*k,4*k)
s.text(430,566,'Nut pushes carriage; it does not replace the guide.',18,'label');s.text(430,595,'Stops contact the block at x = 20 and 110.',17);s.text(430,622,'Centre stop positions = 35 and 95: 5 mm beyond each useful endpoint.',16);s.text(430,649,'Slide block onto rail before fitting the removable end stop.',16);s.text(430,676,'Reserve ≥30 mm clear insertion beyond an open rail end.',16)
s.save('design-screw-layout.svg')

s=SVG('Screw stage: dimension the moving envelope first','Four modeling checkpoints · the screw transmits thrust; the guide establishes the path',580)
for i,(title,lines) in enumerate([
 ('1  Define the travel',['Centres at x = 40 and 90','Block length = 30 mm','Nut length = 20 mm']),
 ('2  Add the guide',['Rail x = 20…110; y = 25','Rigidly connect nut + block','Do not constrain screw to slide.']),
 ('3  Close the thrust path',['Fixed support → base','Float support permits growth','Coupling is not a thrust bearing.']),
 ('4  Plan real assembly',['Nut slides on screw first','Block slides onto open rail','End stop is fitted last.'])]):
 xx=30+i*295;s.rect(xx,105,280,420,'ghost');s.text(xx+14,138,title,18,'label')
 for j,t in enumerate(lines):s.text(xx+14,410+j*29,t,15)
 if i==0:
  s.rect(xx+30,242,78,48,'ghost');s.rect(xx+172,242,78,48,'ghost');s.dim(xx+69,337,xx+211,337,'50 mm',xx+110,327)
 elif i==1:
  s.rect(xx+28,238,224,16,'metal');s.rect(xx+100,222,80,49);s.line(xx+28,320,xx+252,320,'path');s.rect(xx+112,298,56,42,'drive');s.line(xx+140,271,xx+140,298,'path')
 elif i==2:
  s.line(xx+25,267,xx+255,267,'path');s.rect(xx+52,225,32,84);s.rect(xx+207,236,27,62,'metal');s.text(xx+38,350,'fixed',16);s.text(xx+205,350,'float',16)
 else:
  s.rect(xx+35,260,210,20,'metal');s.rect(xx+50,243,60,54);s.dim(xx+130,225,xx+230,225,'insert',xx+145,210);s.rect(xx+245,247,15,46,'drive')
s.save('design-screw-steps.svg')

s=SVG('Tendon finger: a radius makes the force calculation meaningful','Design study · constant-radius wrap, one tendon layer, and a perpendicular fingertip force',730)
s.text(45,120,'A  LOOK ALONG THE HINGE PIN',18,'label');x,y,k=440,320,5.5
s.circle(x-45*k,y-18*k,8*k,'drive');s.circle(x,y,10*k,'drive');s.circle(x,y,2*k,'metal');s.rect(x,y-15,30*k,30,'part');s.line(x,y,x+15*k,y-30*math.sin(math.pi/3)*k,'ghost');s.line(x-45*k,y-10*k,x,y-10*k,'path');s.p.append(f'<line x1="{x+30*k}" y1="{y+5}" x2="{x+30*k}" y2="{y+88}" stroke="#536577" stroke-width="2" marker-end="url(#arr)"/>')
s.p.append(f'<path d="M{x},{y-10*k} A{10*k},{10*k} 0 0 1 {x+5*k},{y+10*math.sqrt(3)/2*k}" class="path"/>');s.circle(x+5*k,y+10*math.sqrt(3)/2*k,4,'metal')
s.text(400,432,'5 N perpendicular tip force',17);s.dim(x,y+75,x+30*k,y+75,'30 mm',x+55,y+64);s.text(80,164,'Spool radius 8',17);s.text(69,360,'Tendon tension 15 N ideal',17);s.text(75,389,'Straight tangent at y = 10',16);s.text(365,178,'60° finger travel',17);s.text(377,473,'Sector radius 10 mm',17)
s.text(737,155,'The wrapped arc matters.',19,'label');s.text(737,189,'A straight cord tied to a hole',17);s.text(737,215,'has a changing moment arm.',17);s.text(737,260,'Here: tendon travel = r × angle',17);s.text(737,291,'10 × π/3 = 10.47 mm',19,'label');s.text(737,334,'Spool motion = 10.47 / 8',17);s.text(737,365,'= 1.309 rad = 75°',19,'label');s.text(737,409,'Ideal spool torque = 15 × 0.008',17);s.text(737,440,'= 0.12 N·m before return spring',18,'label')
s.text(45,529,'B  AXIAL SECTION: HINGE SUPPORT',18,'label');x,y,k=185,620,6
s.rect(x-7*k,y-2*k,22*k,4*k,'metal');s.rect(x-4.3*k,y-12*k,4*k,24*k);s.rect(x+8.3*k,y-12*k,4*k,24*k);s.rect(x,y-10*k,8*k,20*k,'drive')
s.text(385,558,'Finger z = 0…8; cheeks −4.3…−0.3 and 8.3…12.3.',16);s.text(385,588,'0.3 mm per side is a fit-trial starting value, not a universal tolerance.',16);s.text(385,618,'Hinge carries contact load into the base. Spool needs its own support.',17);s.text(385,648,'Insert the pin axially; reserve ≥22 mm tool/withdrawal access.',16);s.text(385,678,'Add open/close stops and route the return spring clear of the tendon.',16)
s.save('design-tendon-layout.svg')

s=SVG('Tendon finger: model the contact geometry before the shell','Four modeling checkpoints · tendon routing, bearing support and service access are design inputs',580)
for i,(title,lines) in enumerate([
 ('1  Constrain the radii',['Hinge radius = 10 mm','Spool radius = 8 mm','Tendon tangent at y = 10']),
 ('2  Give the finger a hinge',['Extrude finger 8 mm','Clevis gap starts at 8.6 mm','Keep pin and bushings separate.']),
 ('3  Trace the excursion',['Revolute joint: 0…60°','Provide ≥10.47 mm wrap travel','Add open and closed stops.']),
 ('4  Add service details',['Accessible tendon anchor','Rounded smooth cord route','Pin insertion and spring access'])]):
 xx=30+i*295;s.rect(xx,105,280,420,'ghost');s.text(xx+14,138,title,18,'label')
 for j,t in enumerate(lines):s.text(xx+14,410+j*29,t,15)
 if i==0:
  s.circle(xx+74,238,28,'drive');s.circle(xx+205,306,40,'drive');s.line(xx+74,266,xx+205,266,'path')
 elif i==1:
  s.rect(xx+63,208,28,126);s.rect(xx+189,208,28,126);s.rect(xx+98,221,84,100,'drive');s.line(xx+30,272,xx+250,272,'path')
 elif i==2:
  s.circle(xx+83,310,28,'drive');s.line(xx+83,310,xx+230,310,'path');s.line(xx+83,310,xx+157,183,'ghost');s.circle(xx+223,331,8,'metal');s.circle(xx+176,188,8,'metal')
 else:
  s.circle(xx+140,270,60,'drive');s.line(xx+140,210,xx+52,210,'path');s.circle(xx+182,227,9,'metal');s.dim(xx+182,183,xx+182,214,'',xx+185,185);s.text(xx+57,360,'Anchor stays reachable',16)
s.save('design-tendon-steps.svg')

for name,study in studies.items():write_params(name,study)
(HERE/'layout-checks.json').write_text(json.dumps({
 'units':'mm','belt_center_distance':C,'belt_pitch_length_reconstructed':belt_length(C,R,r),
 'belt_axial_gap_each_side':10-3.5,'screw_nut_margin_each_end':40-10-25,
 'screw_block_margin_each_end':40-15-20,'tendon_travel':10*math.pi/3,
 'tendon_spool_angle_degrees':(10*math.pi/3)/8*180/math.pi,
 'limitations':'Numerical consistency only; no load, print, fit, manufacturing or hardware validation.'},indent=2)+'\n')
print(f'Generated six diagrams, six DXFs, three parameter tables and three JSON studies. Belt centre: {C:.9f} mm.')

#!/usr/bin/env python3
"""Create original silent teaching animations, posters, and captions.

Requires Python 3.10+, Pillow, and ffmpeg/ffprobe on PATH. This script does not
operate hardware or read CAD. Coordinates are schematic; kinematic ratios are
calculated from the guide's nominal values. Outputs overwrite files beside it.
"""
from pathlib import Path
import argparse, json, math, re, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H, FPS, SECONDS = 1280, 720, 24, 12
PAPER = '#fbfaf7'
INK = '#243e38'
MUTED = '#5e6e66'
TEAL = '#23695b'
TEAL_LIGHT = '#dfece6'
RUST = '#a9542c'
RUST_LIGHT = '#f4e5d3'
GRAY = '#abb5ad'
LINE = '#d8ded5'
WHITE = '#fffefa'

def load_font(size, bold=False):
    names = [
        f'/System/Library/Fonts/Supplemental/Arial{" Bold" if bold else ""}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf',
        f'C:/Windows/Fonts/arial{"bd" if bold else ""}.ttf',
    ]
    for filename in names:
        if Path(filename).is_file(): return ImageFont.truetype(filename, size)
    raise RuntimeError('Install Arial or DejaVu Sans, or add its location to load_font().')

FONTS = {(size, bold):load_font(size, bold) for size in [18,20,21,22,24,28,34,36] for bold in [False,True]}
def font(size=22, bold=False):return FONTS[size,bold]

def txt(d,xy,text,size=22,color=INK,bold=False,anchor=None):
    d.text(xy,text,font=font(size,bold),fill=color,anchor=anchor)

def wrapped(d,xy,text,width,size=22,color=INK,bold=False,leading=None):
    x,y=xy;lines=[];line=''
    for word in text.split():
        trial=(line+' '+word).strip()
        if line and d.textlength(trial,font=font(size,bold))>width:
            lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    for line in lines:
        txt(d,(x,y),line,size,color,bold);y+=leading or size+6
    return y

def line(d,points,color=INK,width=3):d.line(points,fill=color,width=width,joint='curve')
def arrow(d,a,b,color=TEAL,width=4,head=12,both=False):
    line(d,[a,b],color,width)
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    if not length:return
    ux,uy=dx/length,dy/length
    def tip(t,sign):
        u,v=ux*sign,uy*sign
        d.polygon([t,(t[0]-head*u+head*.45*v,t[1]-head*v-head*.45*u),(t[0]-head*u-head*.45*v,t[1]-head*v+head*.45*u)],fill=color)
    tip(b,1)
    if both:tip(a,-1)

def circle(d,c,r,fill=WHITE,outline=INK,width=3):
    d.ellipse((c[0]-r,c[1]-r,c[0]+r,c[1]+r),fill=fill,outline=outline,width=width)

def dashed(d,a,b,color=GRAY,width=2,dash=10):
    length=math.dist(a,b)
    if not length:return
    for distance in range(0,int(length),dash*2):
        q=min(length,distance+dash)
        line(d,[(a[0]+(b[0]-a[0])*distance/length,a[1]+(b[1]-a[1])*distance/length),(a[0]+(b[0]-a[0])*q/length,a[1]+(b[1]-a[1])*q/length)],color,width)

def base(number,title,subtitle):
    image=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(image)
    txt(d,(40,25),f'{number:02} / MECHANISM IN MOTION',18,TEAL,True)
    txt(d,(40,58),title,36,INK,True)
    txt(d,(40,112),subtitle,22,MUTED)
    d.rounded_rectangle((40,166,814,567),radius=14,fill=WHITE,outline=LINE,width=2)
    d.rounded_rectangle((842,166,1240,567),radius=14,fill=TEAL_LIGHT,outline=LINE,width=2)
    txt(d,(40,696),'Original schematic • illustrative timing • no physical test or hardware simulation',18,MUTED)
    return image,d

def metrics(d,rows,note):
    for i,(label,value) in enumerate(rows):
        y=190+i*84
        txt(d,(867,y),label,20,MUTED)
        txt(d,(867,y+29),value,34,TEAL,True)
        line(d,[(867,y+75),(1213,y+75)],'#c2d4ca',1)
    wrapped(d,(867,459),note,345,22,INK,False,27)

def footer(d,benefit,cost,check):
    for x,label,text in [(40,'BENEFIT',benefit),(448,'COST',cost),(856,'CHECK',check)]:
        txt(d,(x,588),label,18,TEAL,True)
        wrapped(d,(x,614),text,373,20,INK,False,25)

def progress(time):return max(0.0,min(1.0,(time-1)/9))

def belt(time):
    p=progress(time);input_turns=3*p;output_turns=p
    image,d=base(1,'Three input turns. One output turn.','A 20-tooth input pulley drives a 60-tooth output pulley.')
    scale=5
    # Pitch radius = tooth_count * pitch / (2*pi), where pitch is 2 mm.
    small=20*2/(2*math.pi)*scale;large=60*2/(2*math.pi)*scale
    distance=58.61153060046303*scale
    c1=(220,348);c2=(220+distance,348)
    alpha=math.asin((large-small)/distance)
    nt=(-math.sin(alpha),-math.cos(alpha));nb=(-math.sin(alpha),math.cos(alpha))
    a=(c1[0]+small*nt[0],c1[1]+small*nt[1]);b=(c2[0]+large*nt[0],c2[1]+large*nt[1])
    c=(c2[0]+large*nb[0],c2[1]+large*nb[1]);e=(c1[0]+small*nb[0],c1[1]+small*nb[1])
    d.rounded_rectangle((169,292,271,404),radius=7,fill='#edf0eb',outline=GRAY,width=2)
    for center,radius,count,turns in [(c1,small,20,input_turns),(c2,large,60,output_turns)]:
        circle(d,center,radius,RUST_LIGHT,RUST,3)
        for n in range(count):
            angle=2*math.pi*(n/count+turns)-math.pi/2
            line(d,[(center[0]+(radius-7)*math.cos(angle),center[1]+(radius-7)*math.sin(angle)),(center[0]+radius*math.cos(angle),center[1]+radius*math.sin(angle))],RUST,2)
        phase=2*math.pi*turns-math.pi/2
        q=(center[0]+radius*.72*math.cos(phase),center[1]+radius*.72*math.sin(phase))
        line(d,[center,q],TEAL,5);circle(d,q,5,TEAL,TEAL,1)
        circle(d,center,11,WHITE,MUTED,3)
    line(d,[a,b],RUST,5);line(d,[e,c],RUST,5)
    angle=math.degrees(alpha)
    d.arc((c1[0]-small,c1[1]-small,c1[0]+small,c1[1]+small),90+angle,270-angle,fill=RUST,width=5)
    d.arc((c2[0]-large,c2[1]-large,c2[0]+large,c2[1]+large),-90-angle,90+angle,fill=RUST,width=5)
    txt(d,(96,219),'INPUT · 20 teeth',22,INK,True)
    txt(d,(519,207),'OUTPUT · 60 teeth',22,INK,True)
    txt(d,(258,248),'Toothed belt',21,RUST)
    line(d,[(353,276),(374,284)],RUST,2)
    txt(d,(112,432),'Motor shaft',21,MUTED)
    txt(d,(489,459),'Output shaft',21,MUTED)
    arrow(d,(220,501),(c2[0],501),MUTED,2,8,True)
    txt(d,(225,520),'58.612 mm axis spacing',20,MUTED)
    metrics(d,[('Input rotation',f'{input_turns:.2f} turns'),('Output rotation',f'{output_turns:.2f} turns'),('Speed reduction','3 : 1')],'Ideal: 3× output torque. Real torque gain is lower because of losses.')
    footer(d,'Place the motor away from the joint axis.','Belt stretch and tension load the shaft supports.','Matching tooth system, tension, bearing loads.')
    return image

def screw(time):
    p=progress(time);travel=50*p;turns=travel/2
    image,d=base(2,'One screw turn advances the nut 2 mm.','The guide carries side loads; the screw supplies axial drive force.')
    sx=lambda mm:150+4.2*mm
    center=sx(40+travel)
    d.rectangle((60,478,708,497),fill='#e3e8e1',outline=MUTED,width=2)
    d.rectangle((61,350,78,478),fill='#e3e8e1',outline=MUTED,width=2)
    d.rounded_rectangle((60,298,118,354),radius=5,fill='#e8e4d9',outline=MUTED,width=2)
    d.rectangle((118,315,154,337),fill=RUST_LIGHT,outline=RUST,width=2)
    for x,w in [(sx(0),4.2*15),(sx(115),4.2*15)]:
        d.rectangle((x+16,355,x+w-16,478),fill='#e3e8e1',outline=MUTED,width=2)
        d.rounded_rectangle((x,296,x+w,358),radius=5,fill=TEAL_LIGHT,outline=TEAL,width=2)
    for x in [sx(20),sx(106)]:
        d.rectangle((x,451,x+17,478),fill='#e3e8e1',outline=MUTED,width=2)
    d.rectangle((sx(20),439,sx(110),452),fill='#d9e0da',outline=MUTED,width=2)
    d.rounded_rectangle((sx(0),315,sx(130),337),radius=5,fill='#d5dcd6',outline=MUTED,width=2)
    period=2*4.2;phase=(turns%1)*period
    for n in range(-2,70):
        x=sx(0)+n*period+phase
        a=max(sx(0),x);b=min(sx(130),x+period*.7)
        if a<=b:line(d,[(a,335),(b,317)],'#7d8f85',2)
    d.rectangle((center-25,336,center+25,407),fill=TEAL_LIGHT,outline=TEAL,width=2)
    d.rounded_rectangle((center-63,405,center+63,439),radius=4,fill=TEAL_LIGHT,outline=TEAL,width=3)
    d.rounded_rectangle((center-42,307,center+42,346),radius=5,fill=RUST_LIGHT,outline=RUST,width=3)
    txt(d,(248,200),'Nut + carriage move together',22,INK,True)
    line(d,[(center,236),(center,302)],MUTED,2)
    txt(d,(72,259),'Motor',20,MUTED)
    txt(d,(154,370),'Fixed',20,TEAL)
    txt(d,(624,370),'Floating',20,TEAL)
    txt(d,(269,454),'Separate linear guide',20,MUTED)
    arrow(d,(sx(40),530),(sx(90),530),MUTED,2,8,True)
    txt(d,(301,541),'50 mm useful travel',20,MUTED)
    # A separate phase marker shows rotation; the screw does not translate.
    dial=(692,221);circle(d,dial,26,WHITE,RUST,2)
    phase=2*math.pi*turns-math.pi/2
    q=(dial[0]+21*math.cos(phase),dial[1]+21*math.sin(phase))
    line(d,[dial,q],TEAL,4);circle(d,q,4,TEAL,TEAL,1)
    txt(d,(613,175),'Screw rotation',18,MUTED)
    metrics(d,[('Nut travel',f'{travel:.2f} mm'),('Screw rotation',f'{turns:.2f} turns'),('Lead','2 mm / rev')],'At the target 20 mm/s, the screw needs 600 rpm. This clip is slowed for clarity.')
    footer(d,'High axial force from modest motor torque.','Small lead needs more turns; friction and backlash matter.','A separate guide, axial support, nut fit, and duty.')
    return image

def tendon(time):
    p=progress(time);theta=math.pi/3*p;spool_angle=theta*10/8
    travel=10*theta
    image,d=base(3,'Constant radius makes the motion predictable.','A wrapped tendon links a remote spool to one hinged finger.')
    hinge=(490,390);spool=(220,282);R=60;r=48;finger=180;half=24
    # Both axes stay fixed. This is a front-view schematic, not a support drawing.
    dashed(d,(96,390),(744,390),LINE,1)
    txt(d,(78,190),'Spool radius 8 mm',22,INK,True)
    txt(d,(474,190),'Sector radius 10 mm',22,INK,True)
    circle(d,spool,r,RUST_LIGHT,RUST,2)
    circle(d,hinge,R,TEAL_LIGHT,TEAL,2)
    def local(x,y):return (hinge[0]+x*math.cos(theta)-y*math.sin(theta),hinge[1]-x*math.sin(theta)-y*math.cos(theta))
    arm=[local(0,-half),local(finger,-half),local(finger,half),local(0,half)]
    d.polygon(arm,fill=TEAL_LIGHT);line(d,arm+[arm[0]],TEAL,3)
    # The attached anchor begins at -60 degrees relative to the finger.
    end=60-math.degrees(theta)
    d.arc((hinge[0]-R,hinge[1]-R,hinge[0]+R,hinge[1]+R),-90,end,fill=RUST,width=6)
    anchor=(hinge[0]+R*math.cos(math.radians(end)),hinge[1]+R*math.sin(math.radians(end)))
    circle(d,anchor,6,WHITE,RUST,3)
    line(d,[(spool[0],spool[1]+r),(hinge[0],hinge[1]-R)],RUST,6)
    # Clockwise spool winding consumes cord; opposite contact sides reverse direction.
    spool_degrees=math.degrees(spool_angle)
    d.arc((spool[0]-r,spool[1]-r,spool[0]+r,spool[1]+r),90,270+spool_degrees,fill=RUST,width=6)
    phase=math.radians(270+spool_degrees)
    spool_anchor=(spool[0]+r*math.cos(phase),spool[1]+r*math.sin(phase))
    circle(d,spool_anchor,6,WHITE,RUST,3)
    line(d,[spool,spool_anchor],TEAL,3)
    circle(d,spool,10,WHITE,MUTED,3);circle(d,hinge,10,WHITE,MUTED,3)
    # Cord markers move toward the spool while the straight tangent stays fixed.
    offset=(travel*6)%44
    for x in range(250,490,44):
        q=x-offset
        if spool[0]+10<q<hinge[0]-10:circle(d,(q,330),3,WHITE,RUST,1)
    txt(d,(88,425),'Cord winds onto spool',20,RUST)
    arrow(d,(369,353),(288,353),RUST,3,10)
    wrapped(d,(455,479),'Anchor rotates with the finger; the wrapped arc gets shorter.',325,20,MUTED)
    line(d,[(555,469),anchor],MUTED,2)
    txt(d,(85,535),'Fixed axes · constant radii · one taut tendon layer',20,MUTED)
    metrics(d,[('Finger closes',f'{math.degrees(theta):.1f}°'),('Tendon take-up',f'{travel:.2f} mm'),('Spool winds clockwise',f'{spool_degrees:.1f}°')],'In this routing the spool and finger turn in opposite directions. The radii set the ratio.')
    footer(d,'Move motor mass away from the finger.','Stretch, friction, slack, and spool layers change behavior.','Cord routing, retained wrap, anchoring, and spring load.')
    return image

CLIPS = [
    {
        'id':'motion-belt','chapter':5,'title':'Watch a 3:1 belt reduction',
        'description':'A silent original schematic animation: three turns of a 20-tooth input pulley produce one turn of a 60-tooth output pulley.',
        'watch_for':'Follow the green rotation marks and the turn counters. Both pulleys turn in the same direction; the larger output completes one turn while the input completes three.',
        'tradeoff':'A belt lets you move the motor away from the joint. Reduction trades output speed for torque; belt stretch, alignment, and tension add constraints on precision and shaft support.',
        'limits':'Pitch-circle kinematics only. Tooth marks are illustrative, not pulley profiles. The ideal torque gain excludes losses, and this animation does not simulate belt tension, deflection, bearings, or physical motion.',
        'renderer':belt,
        'captions':[(0,4,'The 20-tooth input turns clockwise and drives a 60-tooth output pulley.'),(4,8,'Both pulleys turn in the same direction. The larger pulley rotates at one third of the input speed.'),(8,12,'Three input turns produce one output turn. Ideal torque gain is three; real transmission losses reduce it.')],
        'transcript':'''The input pulley has20 teeth and the output pulley has60. Their pitch circles share a matched2 mm pitch belt. The axes are58.61153 mm apart for the candidate200 mm pitch-length belt used in the guide. The tooth marks in the drawing are only schematic.

As the input makes three clockwise turns, the output makes one clockwise turn. An open belt preserves rotation direction. Reduction G=60/20=3 makes output speed one third of input speed. In an ideal lossless drive, output torque is three times input torque; real torque gain during forward power transmission is reduced by efficiency.

The benefit is flexible motor placement and a visible, serviceable transmission. The costs include belt elasticity, alignment sensitivity and support loads from belt tension. Check the matching tooth system, installation tension, shaft supports and allowable load. No bearing or belt load rating is established by the animation.'''
    },
    {
        'id':'motion-screw','chapter':6,'title':'Watch rotation become linear travel',
        'description':'A silent original schematic animation: a rotating screw advances a guided nut and carriage through50 mm of useful travel.',
        'watch_for':'The screw rotates without translating. The nut and carriage move together, while the separate guide keeps the carriage on its path. Twenty-five turns at2 mm lead produce50 mm of travel.',
        'tradeoff':'A small lead provides considerable force leverage but requires more motor revolutions for a given travel. Nut friction, backlash, axial support and guide alignment constrain the result.',
        'limits':'A simplified kinematic side view, with the guide shown below the screw for clarity. The helix is a symbol, not a thread profile. Timing is slowed; the clip does not model acceleration, thrust bearing details, screw buckling, preload, or backdrivability.',
        'renderer':screw,
        'captions':[(0,4,'The screw rotates in place. The guided nut and carriage begin moving along the axis.'),(4,8,'Lead is travel per revolution:2 mm in this example. The separate guide carries lateral loads.'),(8,12,'Twenty-five revolutions give50 mm travel. At the separate target speed of20 mm per second, the screw would need600 rpm.')],
        'transcript':'''The screw is held axially at its fixed support. A far support locates it radially while allowing the intended axial accommodation. The nut drives the carriage, and a separate linear guide carries lateral forces and moments. The motor coupling is not the thrust bearing.

For a2 mm-per-revolution lead,25 screw revolutions produce50 mm of nut travel. The animation is slowed to make the relationship visible. At the guide's separate steady-speed target of20 mm/s, required speed is20/2=10 revolutions per second, or600 rpm.

A smaller lead reduces the ideal torque required for an axial force but increases the number of motor turns needed for a move. Friction and preload raise drive torque; thread backlash and structural flex affect positioning. Check lead rather than assuming thread pitch equals travel per turn. Support, nut engagement, guide alignment and power-loss behavior require their own design checks. The depicted helix is a symbol, not a manufacturing profile.'''
    },
    {
        'id':'motion-tendon','chapter':7,'title':'Watch the tendon wrap and spool together',
        'description':'A silent original schematic animation: a constant-radius finger sector closes60° as an8 mm effective-radius spool takes up10.47 mm of tendon.',
        'watch_for':'Follow the tendon from the spool’s lower tangent to the finger sector’s upper tangent, around the wrapped arc, and into the moving anchor. The spool winds75° clockwise while the finger closes60° counterclockwise.',
        'tradeoff':'Remote actuation can reduce moving finger mass. A constant effective radius makes the motion ratio predictable, but cord stretch, routing friction, slack, changing spool layers and return-spring force affect real behavior.',
        'limits':'Ideal, taut, inextensible tendon with constant10 mm finger radius and8 mm spool radius, one layer, and adequate retained wrap. This shows kinematics only; no contact-force, spring, friction, compliance, or support-load simulation is performed.',
        'renderer':tendon,
        'captions':[(0,4,'The tendon reaches the finger on a tangent and remains wrapped around its circular sector to the anchor.'),(4,8,'The spool winds clockwise while the finger closes counterclockwise. The finger’s wrapped arc shortens as cord is taken up.'),(8,12,'Sixty degrees at a10 mm radius uses10.47 mm of tendon. An8 mm spool turns75 degrees to take up that length.')],
        'transcript':'''The finger sector has a constant10 mm effective radius and the spool has an8 mm effective radius. Their axes remain fixed. The straight tendon touches the bottom of the spool and the top of the finger sector, so this routing makes their rotation directions opposite.

The finger anchor begins60° below the finger’s forward direction. As the finger closes60° counterclockwise, the wrapped angle from the upper tangent to the anchor decreases from150° to90°. The arc remains connected to the moving anchor; a line ending at the tangent point alone would not drive the finger.

Tendon take-up is radius times angle in radians:10×π/3=10.47198 mm. The8 mm spool therefore winds10.47198/8=1.309 radians, or75° clockwise. The clip does not show a contact force; these are motion relationships. At the guide’s specified perpendicular5 N tip load30 mm from the hinge, the ideal static tension is15 N and spool torque0.12 N·m, before spring and friction.

The benefit is placing motor mass away from the finger. Constraints include maintaining the intended tangent and effective radii, enough retained wrap, a reliable anchor, low routing friction, and controlled cord tension. Stretch, slack, layered winding and return springs change the actual position/force relationship. The hinge and spool need their own support structure, which is omitted from this motion schematic.'''
    },
]

def timestamp(seconds):
    whole=int(seconds);ms=round((seconds-whole)*1000)
    return f'00:{whole//60:02}:{whole%60:02}.{ms:03}'

def readable(text):
    text=re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text)
    return re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)

def render(clip):
    filename=HERE/(clip['id']+'.mp4')
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(filename)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for frame in range(FPS*SECONDS):proc.stdin.write(clip['renderer'](frame/FPS).tobytes())
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError(f'ffmpeg failed for {filename.name}')
    clip['renderer'](10.5).save(HERE/(clip['id']+'-poster.png'),optimize=True)
    vtt='WEBVTT\n\n'+'\n\n'.join(f'{timestamp(a)} --> {timestamp(b)}\n{readable(text)}' for a,b,text in clip['captions'])+'\n'
    (HERE/(clip['id']+'.vtt')).write_text(vtt)
    transcript=f"# {clip['title']}\n\nSilent original schematic animation; no physical experiment is shown. Duration: 12 seconds.\n\n{clip['transcript']}\n"
    # Author text stays readable; no concatenated number/unit sentences in downloads.
    transcript=readable(transcript)
    (HERE/(clip['id']+'-transcript.md')).write_text(transcript)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames:format=duration,size','-of','json',str(filename)],text=True))
    assert float(info['format']['duration'])==SECONDS
    stream=info['streams'][0]
    assert stream['codec_name']=='h264' and stream['pix_fmt']=='yuv420p'
    assert stream['width']==W and stream['height']==H and int(stream['nb_frames'])==FPS*SECONDS
    return info

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only',choices=['belt','screw','tendon']);args=parser.parse_args()
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):raise SystemExit('ffmpeg and ffprobe must be on PATH.')
    checks={}
    for clip in CLIPS:
        if not args.only or clip['id']=='motion-'+args.only:checks[clip['id']]=render(clip)
    records=[]
    for clip in CLIPS:
        item={key:readable(clip[key]) if isinstance(clip[key],str) and key!='id' else clip[key] for key in ['id','chapter','title','description','watch_for','tradeoff','limits']}
        item.update(src=f"media/{clip['id']}.mp4",poster=f"media/{clip['id']}-poster.png",captions=f"media/{clip['id']}.vtt",transcript=f"media/{clip['id']}-transcript.md",duration_seconds=SECONDS,silent=True,kind='original schematic animation')
        records.append(item)
    (HERE/'manifest.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()

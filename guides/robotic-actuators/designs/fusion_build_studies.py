"""Fusion Python script: create/export three separate educational envelope studies.

Not fabrication parts. Does not edit the user's existing document. Run through
Fusion Scripts and Add-Ins after setting OUTPUT_DIR to this script's directory.
Native archives contain editable sketches/extrusions and component envelopes.
Assembly positions are snapshots, not a finished associative mechanism.
"""
import adsk.core, adsk.fusion, json, math
from pathlib import Path

OUTPUT_DIR = str(Path(__file__).resolve().parent)  # Keep the layout JSON files beside this script.

def pt(x,y,z=0): return adsk.core.Point3D.create(x/10,y/10,z/10)
def val(v):return adsk.core.ValueInput.createByString(str(v)+' mm')

def component(root,name,position=(0,0,0),axis='z'):
    m=adsk.core.Matrix3D.create()
    if axis=='x':m.setToRotation(math.pi/2,adsk.core.Vector3D.create(0,1,0),pt(0,0,0))
    m.translation=adsk.core.Vector3D.create(*[v/10 for v in position])
    o=root.occurrences.addNewComponent(m);o.component.name=name
    return o.component

def box(root,name,x,y,z,w,h,t):
    c=component(root,name,(x,y,z));s=c.sketches.add(c.xYConstructionPlane);s.name=name+' footprint'
    lines=s.sketchCurves.sketchLines.addTwoPointRectangle(pt(0,0),pt(w,h))
    # Fixed rectangular footprints make an honest editable envelope, not a fully
    # constrained product model; the manual recipe teaches the native constraints.
    for l in lines:l.isFixed=True
    e=c.features.extrudeFeatures.addSimple(s.profiles.item(0),val(t),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    e.name=name+' thickness';e.bodies.item(0).name=name;s.isVisible=False
    return c

def cylinder(root,name,pos,od,length,bore=0,axis='z'):
    c=component(root,name,pos,axis);s=c.sketches.add(c.xYConstructionPlane);s.name=name+' section'
    circle=s.sketchCurves.sketchCircles.addByCenterRadius(pt(0,0),od/20)
    s.geometricConstraints.addCoincident(circle.centerSketchPoint,s.originPoint)
    s.sketchDimensions.addDiameterDimension(circle,pt(od,od)).parameter.expression=str(od)+' mm'
    if bore:
        hole=s.sketchCurves.sketchCircles.addByCenterRadius(pt(0,0),bore/20)
        s.geometricConstraints.addCoincident(hole.centerSketchPoint,s.originPoint)
        s.sketchDimensions.addDiameterDimension(hole,pt(-od,-od)).parameter.expression=str(bore)+' mm'
    profiles=[p for p in s.profiles if p.profileLoops.count==(2 if bore else 1)]
    e=c.features.extrudeFeatures.addSimple(profiles[0],val(length),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    e.name=name+' length';e.bodies.item(0).name=name;s.isVisible=False
    return c

def belt(root,p):
    C=p['center_distance'];R=60/math.pi;r=20/math.pi
    cylinder(root,'Metal output shaft envelope',(0,0,-15),8,60)
    for z,tag in [(0,'A'),(30,'B')]:
        cylinder(root,'608 bearing '+tag+' envelope',(0,0,z-3.5),22,7,8)
        cylinder(root,'Housing '+tag+' envelope',(0,0,z-4.5),32,9,22)
        box(root,'Housing '+tag+' foot envelope',-16,-27,z-4.5,32,16,9)
    cylinder(root,'60T PITCH CYLINDER no teeth',(0,0,10),2*R,10,8)
    cylinder(root,'20T PITCH CYLINDER no teeth',(C,0,10),2*r,10,5)
    box(root,'Motor body GENERIC envelope',C-21,-21,-40,42,42,40)
    box(root,'Motor bracket envelope no fasteners',C-23,-35,-43,46,14,43)
    cylinder(root,'Motor shaft GENERIC envelope',(C,0,0),5,22)
    box(root,'Arm clamp envelope no fasteners',-6,0,-13,12,100,6)
    box(root,'Base envelope no mounts',-24,-35,-5,C+50,8,40)
    s=root.sketches.add(root.xYConstructionPlane);s.name='Belt tangent reference at z0 (actual belt plane z15)'
    a=math.asin((R-r)/C)
    for sign in [-1,1]:
        l=s.sketchCurves.sketchLines.addByTwoPoints(pt(R*math.sin(a),sign*R*math.cos(a)),pt(C+r*math.sin(a),sign*r*math.cos(a)))
        l.isConstruction=True
    s.isVisible=False

def screw(root,p):
    box(root,'Base envelope',-24,-18,0,164,62,6)
    cylinder(root,'8 mm screw envelope NO THREAD',(-10,0,20),8,140,axis='x')
    cylinder(root,'Nut envelope NO THREAD',(55,0,20),16,20,8,axis='x')
    cylinder(root,'Nut carrier sleeve envelope',(55,0,20),22,20,16,axis='x')
    cylinder(root,'Nut carrier left shoulder envelope',(53,0,20),22,2,8,axis='x')
    cylinder(root,'Nut carrier right removable cap envelope',(75,0,20),22,2,8,axis='x')
    for x,n in [(0,'Fixed axial support selection required'),(115,'Floating radial support selection required')]:
        cylinder(root,n,(x,0,20),28,15,8,axis='x')
        box(root,n+' foot',x,-14,6,15,28,7)
    box(root,'Guide rail envelope',20,21,8,90,8,6)
    box(root,'Guide mounting pedestal envelope',20,21,6,90,8,2)
    box(root,'Guide block mid travel envelope',50,12,14,30,26,10)
    box(root,'Carriage bridge envelope',50,-8,28,30,46,4)
    box(root,'Block standoff envelope',50,12,24,30,26,4)
    for x in [15,110]:box(root,'Removable end stop envelope '+str(x),x,12,6,5,26,24)
    cylinder(root,'Flexible coupling envelope NOT thrust support',(-20,0,20),18,20,8,axis='x')
    box(root,'Motor generic 32 square envelope',-64,-16,4,40,32,32)
    cylinder(root,'Motor mounting plate clearance envelope',(-24,0,20),40,4,18,axis='x')
    box(root,'Motor bracket foot envelope',-24,-20,0,4,40,10)
    cylinder(root,'Motor shaft generic envelope',(-24,0,20),5,13,axis='x')

def tendon(root,p):
    cylinder(root,'Metal hinge pin envelope',(0,0,-7),4,22)
    cylinder(root,'Finger sector PITCH surface no groove',(0,0,0),20,8,4)
    box(root,'Finger arm envelope',0,-4,0,30,8,8)
    for z,n in [(-4.3,'front'),(8.3,'rear')]:
        cylinder(root,'Clevis '+n+' hinge envelope',(0,0,z),24,4,4)
        box(root,'Clevis '+n+' leg envelope',-12,-27,z,24,17,4)
    box(root,'Base envelope',-58,-35,-4.3,100,8,16.6)
    cylinder(root,'Spool PITCH surface no groove',(-45,18,0),16,8,4)
    cylinder(root,'Spool shaft envelope',(-45,18,-8),4,25)
    for z,n in [(-4.3,'front'),(8.3,'rear')]:
        cylinder(root,'Spool bearing support '+n+' envelope',(-45,18,z),12,4,4)
        box(root,'Spool support '+n+' leg envelope',-51,-27,z,12,42,4)
    # Rear structure joins both stops to the base, clear of the moving finger.
    box(root,'Stop support far-side plate envelope',8,-27,-4.3,26,60,4)
    box(root,'Open-stop nominal contact at 0deg',24,-9,-.3,8,5,8.6)
    box(root,'Closed-stop nominal contact at 60deg',8,30*math.sin(math.pi/3)+4*math.cos(math.pi/3),-.3,6,5,8.6)
    # String is reference construction geometry in the proper tendon plane.
    plane=root.constructionPlanes.createInput();plane.setByOffset(root.xYConstructionPlane,val(4));pl=root.constructionPlanes.add(plane)
    s=root.sketches.add(pl);s.name='Tendon tangent and 60deg travel reference'
    for a,b in [((-45,10),(0,10)),((0,0),(15,30*math.sin(math.pi/3)))]:
        l=s.sketchCurves.sketchLines.addByTwoPoints(pt(*a),pt(*b));l.isConstruction=True
    s.isVisible=True

def run(_context: str):
    out=Path(OUTPUT_DIR);app=adsk.core.Application.get();before=app.activeDocument
    original=[{'name':d.name,'modified':d.isModified} for d in app.documents]
    created=[];report=[]
    try:
        for slug,build in [('belt-joint',belt),('screw-stage',screw),('tendon-gripper',tendon)]:
            spec=json.loads((out/(slug+'-layout.json')).read_text());p={x[0]:x[2] for x in spec['parameters']}
            doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);created.append(doc);doc.name=spec['title']+' - UNRATED ENVELOPE STUDY'
            d=adsk.fusion.Design.cast(app.activeProduct);d.designType=adsk.fusion.DesignTypes.ParametricDesignType
            root=d.rootComponent
            for n,u,v in spec['parameters']:d.userParameters.add(n,adsk.core.ValueInput.createByString(str(v)+((' '+u) if u else '')),u,'Study reference input; envelope positions require manual regeneration')
            build(root,p);adsk.doEvents()
            bad=[{'name':i.name,'message':i.errorOrWarningMessage} for i in d.timeline if i.healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
            assert not bad,bad
            for o in root.occurrences:
                for b in o.component.bRepBodies:assert b.isSolid and b.volume>0
            camera=app.activeViewport.camera
            if slug=='screw-stage':
                camera.eye=pt(210,-240,180);camera.target=pt(30,8,16);camera.upVector=adsk.core.Vector3D.create(0,0,1)
            else:
                camera.viewOrientation=adsk.core.ViewOrientations.IsoTopRightViewOrientation
            camera.isFitView=True;app.activeViewport.camera=camera;app.activeViewport.fit();app.activeViewport.refresh();adsk.doEvents()
            assert app.activeViewport.saveAsImageFile(str(out/(slug+'-fusion.png')),1500,1000)
            ex=d.exportManager
            assert ex.execute(ex.createFusionArchiveExportOptions(str(out/(slug+'-envelopes.f3d'))))
            assert ex.execute(ex.createSTEPExportOptions(str(out/(slug+'-envelopes.step'))))
            report.append({'study':slug,'components':root.occurrences.count,'bodies':sum(o.component.bRepBodies.count for o in root.occurrences),'timeline_features':d.timeline.count,'timeline_healthy':True,'is_fabrication_ready':False})
            doc.close(False);created.remove(doc)
    finally:
        for doc in created:doc.close(False)
        if before:before.activate()
    after=[{'name':d.name,'modified':d.isModified} for d in app.documents]
    assert original==after,{'original':original,'after':after}
    (out/'fusion-export-checks.json').write_text(json.dumps({'studies':report,'existing_documents_preserved':original==after,'active_document_restored':before.name if before else None,'limits':'Healthy solid envelope components only; no mechanical qualification, associative assembly, tooth/thread geometry or print validation.'},indent=2)+'\n')
    print(json.dumps({'studies':report,'existing_documents_preserved':True}))

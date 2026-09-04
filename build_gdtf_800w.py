#!/usr/bin/env python3
"""grandMA3 GDTF for an 800W CMY framing spot, 42-channel mode."""
import xml.etree.ElementTree as ET, zipfile
from xml.sax.saxutils import escape

def C(attr, pretty, feature, unit="None", nbytes=1, geo="Beam",
      act=None, color=None, main=None, sets=None, pfrom=None, pto=None):
    return dict(attr=attr, pretty=pretty, feature=feature, unit=unit, nbytes=nbytes,
                geo=geo, act=act, color=color, main=main, sets=sets or [],
                pfrom=pfrom, pto=pto)

CH = [
    C("Pan","P","Position.PanTilt","Angle",2,"Yoke","PanTilt",pfrom=-270,pto=270),
    C("Tilt","T","Position.PanTilt","Angle",2,"Head","PanTilt",pfrom=-135,pto=135),
    C("XY_Speed","PT Spd","Position.PanTilt","None",1,"Head",sets=[(0,"Fast..slow")]),
    C("ColorSub_C","C","Color.RGB","ColorComponent",1,"Beam","ColorRGB"),
    C("ColorSub_M","M","Color.RGB","ColorComponent",1,"Beam","ColorRGB"),
    C("ColorSub_Y","Y","Color.RGB","ColorComponent",1,"Beam","ColorRGB"),
    C("CTO","CTO","Color.Color","Temperature",1,"Beam",sets=[(0,"0..100%")]),
    C("CRI","CRI","Color.Color","None",1,"Beam",sets=[(0,"CRI filter out"),(128,"CRI filter in")]),
    C("Color1","Col Wheel","Color.Color","None",2,"Beam","ColorRGB",sets=[
        (0,"White"),(6,"Indexing"),(116,"White"),(121,"Colour 1"),(131,"Colour 2"),
        (141,"Colour 3"),(151,"Colour 4"),(161,"Colour 5"),(171,"White"),
        (193,"CCW fast..slow"),(224,"Stop"),(225,"CW slow..fast")]),
    C("Gobo1","Gobo","Gobo.Gobo","None",1,"Beam","Gobo",sets=[
        (0,"Open/White"),(8,"Gobo 1"),(21,"Gobo 2"),(34,"Gobo 3"),(47,"Gobo 4"),
        (60,"Gobo 5"),(73,"Gobo 6"),(86,"Gobo 7"),(99,"Gobo 1 shake"),(112,"Gobo 2 shake"),
        (125,"Gobo 3 shake"),(138,"Gobo 4 shake"),(151,"Gobo 5 shake"),(164,"Gobo 6 shake"),
        (177,"Gobo 7 shake"),(190,"CCW scroll fast..slow"),(222,"Stop"),(224,"CW scroll slow..fast")]),
    C("Gobo1Pos","Gobo Rot","Gobo.Gobo","Angle",2,"Beam",sets=[
        (0,"Index 0-360"),(128,"CCW fast..slow"),(191,"Stop"),(193,"CW slow..fast")]),
    C("Gobo2","Pattern","Gobo.Gobo","None",1,"Beam","Gobo",sets=[
        (0,"White"),(6,"Gobo 1"),(17,"Gobo 2"),(28,"Gobo 3"),(39,"Gobo 4"),(50,"Gobo 5"),
        (61,"Gobo 6"),(72,"Gobo 7"),(83,"Gobo 8"),(94,"Gobo 1 shake"),(106,"Gobo 2 shake"),
        (118,"Gobo 3 shake"),(130,"Gobo 4 shake"),(142,"Gobo 5 shake"),(154,"Gobo 6 shake"),
        (166,"Gobo 7 shake"),(178,"Gobo 8 shake"),(190,"CCW fast..slow"),(222,"Stop"),(224,"CW slow..fast")]),
    C("Gobo2Pos","Patt FX","Gobo.Gobo","Angle",1,"Beam",sets=[
        (0,"Effect cut out"),(7,"Index 0-360"),(64,"CCW fast..slow"),(127,"Stop"),
        (129,"CW slow..fast"),(192,"Back-and-forth slow..fast")]),
    C("Iris","Iris","Beam.Beam","None",2,"Beam",sets=[
        (0,"Large..small"),(226,"Slow open fast close"),(236,"Slow close fast open"),
        (246,"Slow close slow open")]),
    C("Prism1","Prism1","Beam.Beam","None",1,"Beam",sets=[(0,"Out"),(8,"In")]),
    C("Prism1Pos","Pr1 Rot","Beam.Beam","Angle",1,"Beam",sets=[
        (0,"Index 0-360"),(128,"CCW fast..slow"),(190,"Stop"),(194,"CW slow..fast")]),
    C("Prism2","Prism2","Beam.Beam","None",1,"Beam",sets=[(0,"Out"),(8,"In")]),
    C("Prism2Pos","Pr2 Rot","Beam.Beam","Angle",1,"Beam",sets=[
        (0,"Index 0-360"),(128,"CCW fast..slow"),(190,"Stop"),(194,"CW slow..fast")]),
    C("Frost1","Frost","Beam.Beam","None",1,"Beam",sets=[(0,"Off"),(128,"On")]),
    C("Zoom","Zoom","Focus.Focus","Angle",2,"Beam",sets=[(0,"Wide..narrow")]),
    C("Focus1","Focus","Focus.Focus","None",2,"Beam",sets=[(0,"0..100%")]),
    C("Shutter1Strobe","Strobe","Beam.Beam","Frequency",1,"Beam",main="Shutter1",sets=[
        (0,"Closed"),(4,"Sync strobe"),(100,"Pulse strobe"),(150,"Flash strobe"),
        (200,"Random strobe"),(250,"Open")]),
    C("Dimmer","Dim","Dimmer.Dimmer","LuminousIntensity",2,"Beam"),
    C("BladeRot","Blade Rot","Shapers.Shapers","Angle",2,"Beam",sets=[(0,"0-180 deg")]),
    C("Blade1A","Blade Up A","Shapers.Shapers","None",1,"Beam"),
    C("Blade1B","Blade Up B","Shapers.Shapers","None",1,"Beam"),
    C("Blade2A","Blade Lf A","Shapers.Shapers","None",1,"Beam"),
    C("Blade2B","Blade Lf B","Shapers.Shapers","None",1,"Beam"),
    C("Blade3A","Blade Dn A","Shapers.Shapers","None",1,"Beam"),
    C("Blade3B","Blade Dn B","Shapers.Shapers","None",1,"Beam"),
    C("Blade4A","Blade Rg A","Shapers.Shapers","None",1,"Beam"),
    C("Blade4B","Blade Rg B","Shapers.Shapers","None",1,"Beam"),
    C("Control1","Macro","Control.Control","None",1,"Head",sets=[
        (0,"No function"),(6,"H reverse open"),(21,"H reverse close"),(26,"V reverse open"),
        (31,"V reverse close"),(36,"Mobile light block ON"),(41,"Mobile light block OFF"),
        (46,"No function"),(51,"Fan auto"),(56,"Fan high speed"),(61,"Fan high silent"),
        (66,"Fan ultra-quiet"),(71,"Curve linear"),(76,"Curve square"),(81,"Curve inv square"),
        (86,"Curve S"),(91,"400Hz"),(96,"1200Hz"),(101,"2000Hz"),(106,"4000Hz"),(111,"6000Hz"),
        (116,"8000Hz"),(121,"16kHz"),(126,"24kHz"),(131,"Display backlight on"),(136,"Backlight 15s"),
        (141,"Backlight 30s"),(146,"Backlight 60s"),(151,"Dimmer speed smooth"),(156,"Dimmer speed fast"),
        (161,"Reset Pan/Tilt"),(166,"Reset moving head"),(171,"Reset all"),(176,"Signal keep on"),
        (181,"Signal keep off"),(186,"No function")]),
]

FEATUREGROUPS=[("Position",["PanTilt"]),("Dimmer",["Dimmer"]),("Color",["RGB","Color"]),
    ("Gobo",["Gobo"]),("Beam",["Beam"]),("Focus",["Focus"]),("Shapers",["Shapers"]),
    ("Control",["Control"])]

def A(**kw): return " ".join(f'{k}="{escape(str(v))}"' for k,v in kw.items() if v not in (None,""))
POS=("{1.000000,0.000000,0.000000,0.000000}{0.000000,1.000000,0.000000,0.000000}"
     "{0.000000,0.000000,1.000000,%s}{0.000000,0.000000,0.000000,1.000000}")

L=['<?xml version="1.0" encoding="UTF-8"?>','<GDTF DataVersion="1.1">']
L.append('  <FixtureType '+A(Name="Moving Head 800W 42CH",ShortName="MH800",
    LongName="800W CMY Framing Spot 42CH",Description="800W CMY framing spot moving head, 42CH mode",
    Manufacturer="Generic",FixtureTypeID="6A1B2C3D-0000-4000-8000-000000000042")+'>')
L.append('    <AttributeDefinitions>')
L.append('      <ActivationGroups>')
for a in ["PanTilt","ColorRGB","Gobo"]: L.append(f'        <ActivationGroup Name="{a}"/>')
L.append('      </ActivationGroups>')
L.append('      <FeatureGroups>')
for fg,fs in FEATUREGROUPS:
    L.append(f'        <FeatureGroup Name="{fg}" Pretty="{fg}">')
    for f in fs: L.append(f'          <Feature Name="{f}"/>')
    L.append('        </FeatureGroup>')
L.append('      </FeatureGroups>')
L.append('      <Attributes>')
seen=set()
# declare Shutter1 main attribute (referenced by Shutter1Strobe)
L.append('        <Attribute Name="Shutter1" Pretty="Sh1" Feature="Beam.Beam"/>')
seen.add("Shutter1")
for c in CH:
    if c["attr"] in seen: continue
    seen.add(c["attr"])
    L.append('        <Attribute '+A(Name=c["attr"],Pretty=c["pretty"],ActivationGroup=c["act"],
        Feature=c["feature"],PhysicalUnit=(c["unit"] if c["unit"]!="None" else None),
        Color=c["color"],MainAttribute=c["main"])+'/>')
L.append('      </Attributes>')
L.append('    </AttributeDefinitions>')
L.append('    <Wheels/>')
L.append('    <Models>')
L.append('      <Model Name="Base" Length="0.4" Width="0.4" Height="0.2" PrimitiveType="Cube"/>')
L.append('      <Model Name="Yoke" Length="0.5" Width="0.15" Height="0.45" PrimitiveType="Cube"/>')
L.append('      <Model Name="Head" Length="0.35" Width="0.35" Height="0.5" PrimitiveType="Cylinder"/>')
L.append('      <Model Name="Beam" Length="0.1" Width="0.1" Height="0.03" PrimitiveType="Cylinder"/>')
L.append('    </Models>')
L.append('    <Geometries>')
L.append('      <Geometry Name="Base" Model="Base">')
L.append(f'        <Axis Name="Yoke" Model="Yoke" Position="{POS%"-0.300000"}">')
L.append(f'          <Axis Name="Head" Model="Head" Position="{POS%"-0.150000"}">')
L.append(f'            <Beam Name="Beam" Model="Beam" Position="{POS%"-0.250000"}" LampType="Discharge" PowerConsumption="800" LuminousFlux="35000" ColorTemperature="7500" BeamAngle="18" FieldAngle="22" BeamRadius="0.05" BeamType="Spot" ColorRenderingIndex="90"/>')
L.append('          </Axis>')
L.append('        </Axis>')
L.append('      </Geometry>')
L.append('    </Geometries>')
L.append('    <DMXModes>')
L.append('      <DMXMode '+A(Name="42CH",Geometry="Base")+'>')
L.append('        <DMXChannels>')
offset=1
for c in CH:
    if c["nbytes"]==2: off=f"{offset},{offset+1}"; default="32768/2"; offset+=2
    else: off=f"{offset}"; default="0/1"; offset+=1
    L.append('          <DMXChannel '+A(DMXBreak="1",Offset=off,Default=default,Geometry=c["geo"])+'>')
    L.append(f'            <LogicalChannel Attribute="{c["attr"]}">')
    cf=dict(Attribute=c["attr"],Name=c["attr"]+" 1",DMXFrom="0/1",Default=default)
    if c["pfrom"] is not None: cf.update(PhysicalFrom=c["pfrom"],PhysicalTo=c["pto"])
    if c["sets"]:
        L.append('              <ChannelFunction '+A(**cf)+'>')
        for d,nm in c["sets"]:
            L.append(f'                <ChannelSet Name="{escape(nm)}" DMXFrom="{d}/1"/>')
        L.append('              </ChannelFunction>')
    else:
        L.append('              <ChannelFunction '+A(**cf)+'/>')
    L.append('            </LogicalChannel>')
    L.append('          </DMXChannel>')
L.append('        </DMXChannels>')
L.append('      </DMXMode>')
L.append('    </DMXModes>')
L.append('  </FixtureType>')
L.append('</GDTF>')
xml="\n".join(L)
ET.fromstring(xml)
fp=offset-1
assert fp==42,fp
with zipfile.ZipFile("Moving_Head_800W_42CH.gdtf","w",zipfile.ZIP_DEFLATED) as z:
    z.writestr("description.xml",xml)
print(f"Moving_Head_800W_42CH.gdtf written; logical channels={len(CH)} footprint={fp}")

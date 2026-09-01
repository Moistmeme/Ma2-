#!/usr/bin/env python3
"""Generate grandMA3-compatible GDTF fixtures for the 29CH laser and 39CH moving head.

A .gdtf file is a zip archive containing description.xml. This script builds the
description.xml for each fixture from a compact channel table, validates the DMX
footprint, and writes the zipped .gdtf.
"""
import xml.etree.ElementTree as ET
import zipfile, uuid, os
from xml.sax.saxutils import escape

# ---- channel model -------------------------------------------------------
# each channel: (attr, pretty, feature, phys_unit, bytes, geometry, activation,
#                color, sets)  where sets = list of (dmx_from_8bit, name)
def ch(attr, pretty, feature, unit="None", nbytes=1, geo="Beam",
       activation=None, color=None, sets=None):
    return dict(attr=attr, pretty=pretty, feature=feature, unit=unit,
                nbytes=nbytes, geo=geo, activation=activation, color=color,
                sets=sets or [])

STROBE9 = [(0,"Open"),(6,"Closed"),(11,"Pulse random slow..fast"),
           (36,"Ramp up random slow..fast"),(61,"Ramp down random slow..fast"),
           (86,"Random strobe"),(111,"Strobe break effect"),
           (136,"Strobe slow..fast"),(251,"Open")]

# ---------- LASER 29CH ----------
laser = [
    ch("Pan","P","Position.PanTilt","Angle",2,"Yoke","PanTilt"),
    ch("Tilt","T","Position.PanTilt","Angle",2,"Head","PanTilt"),
    ch("XY_Speed","XY Spd","Position.PanTilt","None",1,"Head",
       sets=[(0,"Max"),(1,"Fast..Slow")]),
    ch("FixtureGlobalReset","Reset","Control.Control","None",1,"Head",
       sets=[(0,"No function"),(251,"Reset (3s)")]),
    ch("Dimmer","Dim","Dimmer.Dimmer","LuminousIntensity",1,"Beam",
       sets=[(0,"Off"),(1,"1..100%")]),
    ch("EffectSpeed","FX Spd","Control.Control","None",1,"Head",
       sets=[(0,"Default auto"),(27,"Auto slow..fast"),(128,"Voice sensitivity")]),
    ch("Gobo1","Pat Grp","Gobo.Gobo","None",1,"Beam","Gobo",
       sets=[(0,"Pattern group (per16)"),(128,"Effect group (per16)")]),
    ch("Gobo2","Pat Sel","Gobo.Gobo","None",1,"Beam","Gobo",
       sets=[(0,"Pattern / effect select")]),
    ch("Shutter1Strobe","Strobe","Beam.Beam","Frequency",1,"Beam",
       sets=[(0,"Open"),(1,"Strobe slow..fast")]),
    ch("Zoom","Pat Size","Focus.Focus","None",1,"Beam",
       sets=[(0,"Large..small")]),
    ch("PatternXPos","H Pos","Position.PanTilt","None",1,"Head",
       sets=[(0,"Left (off outside)"),(128,"Centre"),(129,"Right (off outside)")]),
    ch("PatternYPos","V Pos","Position.PanTilt","None",1,"Head",
       sets=[(0,"Down (off outside)"),(128,"Centre"),(129,"Up (off outside)")]),
    ch("Color1","Colour","Color.Color","None",1,"Beam","ColorRGB",
       sets=[(0,"Original"),(4,"Fixed (per4)"),(32,"Rainbow"),(36,"RGB change"),
             (40,"Colour change"),(44,"Flow (per4)"),(240,"Gradual draw")]),
    ch("ColorSpeed","Col Spd","Color.Color","None",1,"Beam",
       sets=[(0,"Off"),(4,"Slow..fast +"),(128,"Slow..fast -")]),
    ch("PatternLine","Line","Beam.Beam","None",1,"Beam",
       sets=[(0,"Highlight line scan"),(64,"Line scan"),(128,"Point scan")]),
    ch("Gobo1Pos","Rot Z","Gobo.Gobo","Angle",1,"Beam",
       sets=[(0,"Angle"),(128,"Speed")]),
    ch("Gobo2Pos","Rot X","Gobo.Gobo","Angle",1,"Beam",
       sets=[(0,"Angle"),(128,"Speed")]),
    ch("Gobo3Pos","Rot Y","Gobo.Gobo","Angle",1,"Beam",
       sets=[(0,"Angle"),(128,"Speed")]),
    ch("HMovement","H Move","Control.Control","None",1,"Head",
       sets=[(0,"Position"),(128,"Speed")]),
    ch("VMovement","V Move","Control.Control","None",1,"Head",
       sets=[(0,"Position"),(128,"Speed")]),
    ch("PatternZoom","Zoom","Focus.Focus","None",1,"Beam",
       sets=[(0,"Size large..small"),(128,"Zoom speed")]),
    ch("GradualDraw","Draw","Control.Control","None",1,"Head",
       sets=[(0,"Off"),(1,"Speed")]),
    ch("Waves","Waves","Control.Control","None",1,"Head",
       sets=[(0,"Off"),(1,"X wave"),(128,"Y wave")]),
    ch("LED_Dimmer","LED Dim","Dimmer.Dimmer","LuminousIntensity",1,"Beam",
       sets=[(0,"0..100%")]),
    ch("LED_Effect","LED FX","Control.Control","None",1,"Head",
       sets=[(0,"Effect (per8)")]),
    ch("LED_EffectSpeed","LED Spd","Control.Control","None",1,"Head",
       sets=[(0,"Slow..quick")]),
    ch("LED_Strobe","LED Strb","Beam.Beam","Frequency",1,"Beam",
       sets=[(0,"Open"),(1,"Strobe slow..fast")]),
]

# ---------- MOVING HEAD 39CH ----------
RGB = "Color.RGB"
mh = [
    ch("Pan","P","Position.PanTilt","Angle",2,"Yoke","PanTilt"),
    ch("Tilt","T","Position.PanTilt","Angle",2,"Head","PanTilt"),
    ch("XY_Speed","XY Spd","Position.PanTilt","None",1,"Head",
       sets=[(0,"Fast..slow")]),
    ch("Zoom","Zoom","Focus.Focus","Angle",2,"Beam",
       sets=[(0,"Small..large")]),
    ch("Dimmer","Dim","Dimmer.Dimmer","LuminousIntensity",2,"Beam"),
    ch("Shutter1Strobe","Strobe","Beam.Beam","Frequency",1,"Beam",sets=STROBE9),
    ch("ColorAdd_R","R",RGB,"ColorComponent",2,"Beam","ColorRGB","0.6400,0.3300,21.30"),
    ch("ColorAdd_G","G",RGB,"ColorComponent",2,"Beam","ColorRGB","0.3000,0.6000,71.50"),
    ch("ColorAdd_B","B",RGB,"ColorComponent",2,"Beam","ColorRGB","0.1500,0.0600,7.20"),
    ch("ColorAdd_W","W",RGB,"ColorComponent",2,"Beam","ColorRGB","0.3130,0.3290,100.0"),
    ch("Inner_Dimmer","In Dim","Dimmer.Dimmer","LuminousIntensity",1,"Beam"),
    ch("Inner_R","In R",RGB,"ColorComponent",1,"Beam"),
    ch("Inner_G","In G",RGB,"ColorComponent",1,"Beam"),
    ch("Inner_B","In B",RGB,"ColorComponent",1,"Beam"),
    ch("Inner_WW","In WW",RGB,"ColorComponent",1,"Beam"),
    ch("Inner_Strobe","In Strb","Beam.Beam","Frequency",1,"Beam",sets=STROBE9),
    ch("Outer_Dimmer","Out Dim","Dimmer.Dimmer","LuminousIntensity",1,"Beam"),
    ch("Outer_R","Out R",RGB,"ColorComponent",1,"Beam"),
    ch("Outer_G","Out G",RGB,"ColorComponent",1,"Beam"),
    ch("Outer_B","Out B",RGB,"ColorComponent",1,"Beam"),
    ch("Outer_WW","Out WW",RGB,"ColorComponent",1,"Beam"),
    ch("Outer_Strobe","Out Strb","Beam.Beam","Frequency",1,"Beam",sets=STROBE9),
    ch("CTC","CCT","Color.Color","ColorComponent",1,"Beam",
       sets=[(0,"Off"),(6,"1800K"),(22,"2000K"),(38,"2500K"),(54,"2700K"),
             (70,"3000K"),(86,"3200K"),(102,"3500K"),(118,"4000K"),(134,"4500K"),
             (150,"5000K"),(166,"5600K"),(182,"6000K"),(198,"6500K"),(214,"7200K"),
             (230,"8000K")]),
    ch("Tint","Tint","Color.Color","None",1,"Beam",
       sets=[(0,"Off"),(1,"Magenta..Off"),(128,"Off"),(129,"Off..Green")]),
    ch("ColorMacro1","Macro","Color.Color","None",1,"Beam",
       sets=[(0,"Off"),(6,"Magenta"),(11,"Peacock Blue"),(16,"Steel Blue"),
             (21,"Light Blue"),(26,"Dark Blue"),(31,"Leaf Green"),(36,"Dark Green"),
             (41,"Mauve"),(46,"Deep Golden Amber"),(51,"Pale Lavender"),
             (56,"Primary Green"),(61,"Bright Blue"),(66,"Apricot"),(71,"Pale Gold"),
             (76,"Rainbow"),(136,"Macro jump"),(195,"Macro gradient")]),
    ch("Inner_FX","In FX","Control.Control","None",1,"Head",
       sets=[(0,"Off"),(10,"Effect 1"),(35,"Effect 2"),(60,"Effect 3"),(85,"Effect 4"),
             (110,"Effect 5"),(135,"Effect 6"),(160,"Effect 7"),(185,"Effect 8"),
             (210,"Effect 9"),(235,"Effect 10"),(245,"Built-in 1-10")]),
    ch("Inner_FXSpeed","In FX Spd","Control.Control","None",1,"Head",
       sets=[(0,"Index"),(128,"Stop"),(129,"CW fast..slow"),(192,"Stop"),(193,"CCW slow..fast")]),
    ch("Outer_FX","Out FX","Control.Control","None",1,"Head",
       sets=[(0,"Off"),(10,"Effect 1"),(35,"Effect 2"),(60,"Effect 3"),(85,"Effect 4"),
             (110,"Effect 5"),(135,"Effect 6"),(160,"Effect 7"),(185,"Effect 8"),
             (210,"Effect 9"),(235,"Effect 10"),(245,"Built-in 1-10")]),
    ch("Outer_FXSpeed","Out FX Spd","Control.Control","None",1,"Head",
       sets=[(0,"Index"),(128,"Stop"),(129,"CW fast..slow"),(192,"Stop"),(193,"CCW slow..fast")]),
    ch("Function","Func","Control.Control","None",1,"Head",
       sets=[(0,"No function"),(5,"Display on"),(10,"Display 10s"),(15,"Display 30s"),
             (20,"Display 1min"),(25,"Screen lock off"),(30,"Screen lock on"),
             (35,"Signal hold"),(40,"Black field"),(60,"Standard dim"),(65,"Fast dim"),
             (70,"Slow dim"),(85,"Linear"),(90,"Square"),(95,"S-curve"),(110,"4000Hz"),
             (115,"8000Hz"),(120,"16000Hz"),(125,"24000Hz"),(140,"Fan auto"),
             (145,"Silent fan"),(150,"Fan full"),(165,"Red drift off"),(170,"Red drift on"),
             (180,"Pan reverse off"),(185,"Pan reverse on"),(190,"Pan err corr off"),
             (195,"Pan err corr on"),(200,"Tilt reverse off"),(205,"Tilt reverse on"),
             (210,"Tilt err corr off"),(215,"Tilt err corr on"),(220,"Pan/Tilt reset"),
             (225,"Zoom reset"),(230,"Reset all")]),
    ch("Mode","Mode","Control.Control","None",1,"Head",
       sets=[(0,"DMX mode"),(16,"Mixed (pixel)"),(239,"ArtNet mode")]),
]

FEATUREGROUPS = [
    ("Position",[("PanTilt","PanTilt")]),
    ("Dimmer",[("Dimmer","Dimmer")]),
    ("Color",[("RGB","RGB"),("Color","Color")]),
    ("Gobo",[("Gobo","Gobo")]),
    ("Beam",[("Beam","Beam")]),
    ("Focus",[("Focus","Focus")]),
    ("Control",[("Control","Control")]),
]
ACTIVATION = ["PanTilt","ColorRGB","Gobo"]

def phys_range(c):
    if c["attr"]=="Pan":   return (-270,270)
    if c["attr"]=="Tilt":  return (-115,115)
    return None

def build(name, short, long_, chans, fid):
    def A(**kw):  # attribute string
        return " ".join(f'{k}="{escape(str(v))}"' for k,v in kw.items() if v not in (None,""))
    L=[]
    L.append('<?xml version="1.0" encoding="UTF-8"?>')
    L.append('<GDTF DataVersion="1.1">')
    L.append(f'  <FixtureType {A(Name=name,ShortName=short,LongName=long_,Description=long_,Manufacturer="Generic",FixtureTypeID=fid)}>')
    # attribute definitions
    L.append('    <AttributeDefinitions>')
    L.append('      <ActivationGroups>')
    for a in ACTIVATION: L.append(f'        <ActivationGroup Name="{a}"/>')
    L.append('      </ActivationGroups>')
    L.append('      <FeatureGroups>')
    for fg,feats in FEATUREGROUPS:
        L.append(f'        <FeatureGroup Name="{fg}" Pretty="{fg}">')
        for fn,fp in feats: L.append(f'          <Feature Name="{fn}"/>')
        L.append('        </FeatureGroup>')
    L.append('      </FeatureGroups>')
    L.append('      <Attributes>')
    seen=set()
    for c in chans:
        if c["attr"] in seen: continue
        seen.add(c["attr"])
        L.append('        <Attribute '+A(Name=c["attr"],Pretty=c["pretty"],
                 ActivationGroup=c["activation"],Feature=c["feature"],
                 PhysicalUnit=(c["unit"] if c["unit"]!="None" else None),
                 Color=c["color"])+'/>')
    L.append('      </Attributes>')
    L.append('    </AttributeDefinitions>')
    # wheels / models / geometry
    L.append('    <Wheels/>')
    L.append('    <Models>')
    L.append('      <Model Name="Base" Length="0.3" Width="0.3" Height="0.15" PrimitiveType="Cube"/>')
    L.append('      <Model Name="Yoke" Length="0.4" Width="0.1" Height="0.3" PrimitiveType="Cube"/>')
    L.append('      <Model Name="Head" Length="0.25" Width="0.25" Height="0.3" PrimitiveType="Cylinder"/>')
    L.append('      <Model Name="Beam" Length="0.05" Width="0.05" Height="0.02" PrimitiveType="Cylinder"/>')
    L.append('    </Models>')
    I="{1.000000,0.000000,0.000000,0.000000}{0.000000,1.000000,0.000000,0.000000}{0.000000,0.000000,1.000000,%s}{0.000000,0.000000,0.000000,1.000000}"
    L.append('    <Geometries>')
    L.append('      <Geometry Name="Base" Model="Base">')
    L.append(f'        <Axis Name="Yoke" Model="Yoke" Position="{I%"-0.225000"}">')
    L.append(f'          <Axis Name="Head" Model="Head" Position="{I%"-0.100000"}">')
    L.append(f'            <Beam Name="Beam" Model="Beam" Position="{I%"-0.150000"}" LampType="LED" PowerConsumption="200" LuminousFlux="6000" ColorTemperature="6500" BeamAngle="15" FieldAngle="20" BeamRadius="0.03" BeamType="Spot" ColorRenderingIndex="80"/>')
    L.append('          </Axis>')
    L.append('        </Axis>')
    L.append('      </Geometry>')
    L.append('    </Geometries>')
    # dmx mode
    L.append('    <DMXModes>')
    L.append(f'      <DMXMode Name="{name}" Geometry="Base">')
    L.append('        <DMXChannels>')
    offset=1
    for c in chans:
        if c["nbytes"]==2:
            off=f"{offset},{offset+1}"; default="32768/2"; offset+=2
        else:
            off=f"{offset}"; default="0/1"; offset+=1
        hl='255/1' if c["attr"] in ("Dimmer",) else None
        pr=phys_range(c)
        L.append('          <DMXChannel '+A(DMXBreak="1",Offset=off,Default=default,
                 Highlight=hl,Geometry=c["geo"])+'>')
        L.append(f'            <LogicalChannel Attribute="{c["attr"]}">')
        cf=dict(Attribute=c["attr"],Name=c["attr"]+" 1",DMXFrom="0/1",Default=default)
        if pr: cf.update(PhysicalFrom=pr[0],PhysicalTo=pr[1])
        if c["sets"]:
            L.append('              <ChannelFunction '+A(**cf)+'>')
            for i,(d,nm) in enumerate(c["sets"]):
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
    # validate well-formed + footprint
    ET.fromstring(xml)
    fp=offset-1
    return xml, fp

def write_gdtf(path, xml):
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("description.xml", xml)

if __name__=="__main__":
    jobs=[("Laser Moving Head 29CH","LASER29","Laser Moving Head 29CH STD",laser,
           "Laser_Moving_Head_29CH.gdtf","6A1B2C3D-0000-4000-8000-000000000029"),
          ("Moving Head 39CH","MH39","RGB+L Moving Head with Aura Rings 39CH",mh,
           "Moving_Head_39CH.gdtf","6A1B2C3D-0000-4000-8000-000000000039")]
    for name,short,long_,chans,fn,fid in jobs:
        xml,fp=build(name,short,long_,chans,fid)
        write_gdtf(fn,xml)
        print(f"{fn}: channels={len(chans)} footprint={fp}")
        assert fp==(29 if '29' in fn else 39), "footprint mismatch"
    print("OK")

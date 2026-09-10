#!/usr/bin/env python3
"""grandMA2 native fixture XML for a 750W CMY moving profile, 37CH mode."""
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def ranges(sets):
    out=[]
    for i,(s,nm) in enumerate(sets):
        e=sets[i+1][0]-1 if i+1<len(sets) else 255
        out.append((s,e,nm));
    return out

def C(attr,feat,pre,nb=1,sets=None,hv=None):
    return dict(attr=attr,feat=feat,pre=pre,nb=nb,sets=sets or [],hv=hv)

WHEEL=[(0,"White"),(10,"Colour 1"),(20,"Colour 2"),(30,"Colour 3"),(40,"Colour 4"),
    (50,"White+C1"),(60,"C1+C2"),(70,"C2+C3"),(80,"C3+C4"),
    (90,"Rotate fwd fast..slow"),(164,"Rotate rev slow..fast")]
PRROT=[(0,"0-360 index"),(128,"Rotate fwd fast..slow"),(188,"Stop"),(196,"Rotate rev slow..fast")]

CH=[
    C("PAN","POSITION","POSITION",2),
    C("TILT","POSITION","POSITION",2),
    C("PT_SPEED","POSITION","POSITION",1,sets=[(0,"Fast..slow")]),
    C("SHUTTER","BEAM","BEAM",1,sets=[(0,"Dark"),(4,"Pulse strobe slow..fast"),
        (104,"Open"),(108,"Fade strobe slow..fast"),(208,"Open"),
        (213,"Random strobe slow..fast"),(252,"Open")]),
    C("DIM","DIMMER","DIMMER",1,hv=255,sets=[(0,"0..100%")]),
    C("CYAN","COLOR","COLOR",1),
    C("MAGENTA","COLOR","COLOR",1),
    C("YELLOW","COLOR","COLOR",1),
    C("CTO","COLOR","COLOR",1),
    C("COLOR1","COLOR","COLOR",1,sets=[(0,"White"),(128,"Colour 1"),(192,"Colour 2")]),
    C("COLOR2","COLOR","COLOR",1,sets=WHEEL),
    C("COLOR3","COLOR","COLOR",1,sets=WHEEL),
    C("GOBO1","GOBO","GOBO",1,sets=[(0,"White"),(5,"Gobo 1"),(10,"Gobo 2"),(15,"Gobo 3"),
        (20,"Gobo 4"),(25,"Gobo 5"),(30,"Gobo 6"),(35,"Gobo 7"),(40,"Gobo 8"),(45,"Gobo 9"),
        (50,"Gobo 10"),(55,"Shake G1"),(60,"Shake G2"),(65,"Shake G3"),(70,"Shake G4"),
        (75,"Shake G5"),(80,"Shake G6"),(85,"Shake G7"),(90,"Shake G8"),(95,"Shake G9"),
        (100,"Shake G10"),(105,"Rotate fwd fast..slow"),(164,"Rotate rev slow..fast")]),
    C("EFT_GOBO","GOBO","GOBO",1,sets=[(0,"None"),(6,"Rotate slow..fast")]),
    C("GOBO2","GOBO","GOBO",1,sets=[(0,"White"),(10,"Gobo 1"),(20,"Gobo 2"),(30,"Gobo 3"),
        (40,"Gobo 4"),(50,"Gobo 5"),(60,"Gobo 6"),(70,"Gobo 7"),(80,"Shake G1"),(90,"Shake G2"),
        (100,"Shake G3"),(110,"Shake G4"),(120,"Shake G5"),(130,"Shake G6"),(140,"Shake G7"),
        (150,"Rotate rev fast..slow"),(191,"Stop"),(193,"Rotate fwd slow..fast")]),
    C("GOBO2_POS","GOBO","GOBO",1,sets=[(0,"0-360 index"),(128,"Rotate rev fast..slow"),
        (191,"Stop"),(193,"Rotate fwd slow..fast")]),
    C("ZOOM","FOCUS","FOCUS",1,sets=[(0,"Large..small")]),
    C("FOCUS","FOCUS","FOCUS",2,sets=[(0,"Far..near")]),
    C("PRISM1","BEAM","BEAM",1,sets=[(0,"None"),(128,"Insert prism 1")]),
    C("PRISM1_POS","BEAM","BEAM",1,sets=PRROT),
    C("PRISM2","BEAM","BEAM",1,sets=[(0,"None"),(128,"Insert prism 2")]),
    C("PRISM2_POS","BEAM","BEAM",1,sets=PRROT),
    C("FROST1","BEAM","BEAM",1,sets=[(0,"None"),(128,"Insert frost")]),
    C("CUT1","SHAPERS","SHAPERS",1),
    C("CUT2","SHAPERS","SHAPERS",1),
    C("CUT3","SHAPERS","SHAPERS",1),
    C("CUT4","SHAPERS","SHAPERS",1),
    C("CUT5","SHAPERS","SHAPERS",1),
    C("CUT6","SHAPERS","SHAPERS",1),
    C("CUT7","SHAPERS","SHAPERS",1),
    C("CUT8","SHAPERS","SHAPERS",1),
    C("CUT_ROT","SHAPERS","SHAPERS",1,sets=[(0,"0-360 deg")]),
    C("FRAME_MACRO","CONTROL","CONTROL",1),
    C("RESET","CONTROL","CONTROL",1,sets=[(0,"None"),(210,"Reset XY (3s)"),(216,"None"),
        (220,"Reset effect motor (3s)"),(236,"None"),(240,"Reset fixture (3s)")]),
]

L=['<?xml version="1.0" encoding="utf-8"?>']
L.append('<MA xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         'xsi:schemaLocation="http://schemas.malighting.de/grandma2/xml/MA http://schemas.malighting.de/grandma2/xml/2.8.123/MA.xsd" '
         'major_vers="2" minor_vers="8" stream_vers="123" xmlns="http://schemas.malighting.de/grandma2/xml/MA">')
L.append('\t<FixtureType name="Moving Profile 750W" mode="37">')
L.append('\t\t<InfoItems><Info type="Revision" date="2026-09-10">750W CMY moving profile, 37CH mode</Info></InfoItems>')
L.append('\t\t<short_name>MP750</short_name>')
L.append('\t\t<manufacturer>Generic</manufacturer>')
L.append('\t\t<short_manufacturer>Generic</short_manufacturer>')
L.append('\t\t<Modules>')
L.append('\t\t\t<Module name="Main Module" class="Head" beamtype="Spot" beam_angle="17" beam_intensity="30000">')
off=1
for c in CH:
    coarse=off; fine=off+1 if c["nb"]==2 else None; off+=c["nb"]
    a=f'attribute="{c["attr"]}" feature="{c["feat"]}" preset="{c["pre"]}" coarse="{coarse}"'
    if fine: a+=f' fine="{fine}"'
    if c["hv"] is not None: a+=f' highlight_value="{c["hv"]}"'
    L.append(f'\t\t\t\t<ChannelType {a}>')
    cf=(f'from="0" to="100" min_dmx_24="0" max_dmx_24="16777215" physfrom="0" physto="100" '
        f'subattribute="{c["attr"]}" attribute="{c["attr"]}" feature="{c["feat"]}" preset="{c["pre"]}"')
    if c["sets"]:
        L.append(f'\t\t\t\t\t<ChannelFunction {cf}>')
        for s,e,nm in ranges(c["sets"]):
            L.append(f'\t\t\t\t\t\t<ChannelSet name="{escape(nm)}" from_dmx="{s}" to_dmx="{e}" />')
        L.append('\t\t\t\t\t</ChannelFunction>')
    else:
        L.append(f'\t\t\t\t\t<ChannelFunction {cf} />')
    L.append('\t\t\t\t</ChannelType>')
L.append('\t\t\t</Module>')
L.append('\t\t</Modules>')
L.append('\t\t<Instances><Instance module_index="0" patch="1" locked="true" /></Instances>')
L.append('\t\t<Wheels />')
L.append('\t</FixtureType>')
L.append('</MA>')
xml="\n".join(L)
ET.fromstring(xml)
fp=off-1; assert fp==37, fp
open("Moving_Profile_750W_37CH.xml","w",encoding="utf-8").write(xml+"\n")
print(f"Moving_Profile_750W_37CH.xml written; ChannelTypes={len(CH)} footprint={fp}")

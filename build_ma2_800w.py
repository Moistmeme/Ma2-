#!/usr/bin/env python3
"""grandMA2 native fixture XML for the 800W CMY framing spot, 42CH mode.
Same verified schema as the 29/39/17CH profiles: ChannelType in a Module with
coarse(/fine) DMX offsets, ChannelSet from_dmx/to_dmx, one Instance patch."""
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def C(attr, feature, preset, nbytes=1, sets=None, hv=None):
    return dict(attr=attr, feature=feature, preset=preset, nbytes=nbytes,
                sets=sets or [], hv=hv)

COLWHEEL=[(0,"White"),(6,"Indexing"),(116,"White"),(121,"Colour 1"),(131,"Colour 2"),
    (141,"Colour 3"),(151,"Colour 4"),(161,"Colour 5"),(171,"White"),
    (193,"CCW fast..slow"),(224,"Stop"),(225,"CW slow..fast")]
GOBO1=[(0,"Open/White"),(8,"Gobo 1"),(21,"Gobo 2"),(34,"Gobo 3"),(47,"Gobo 4"),(60,"Gobo 5"),
    (73,"Gobo 6"),(86,"Gobo 7"),(99,"Gobo 1 shake"),(112,"Gobo 2 shake"),(125,"Gobo 3 shake"),
    (138,"Gobo 4 shake"),(151,"Gobo 5 shake"),(164,"Gobo 6 shake"),(177,"Gobo 7 shake"),
    (190,"CCW scroll fast..slow"),(222,"Stop"),(224,"CW scroll slow..fast")]
ROT=[(0,"Index 0-360"),(128,"CCW fast..slow"),(191,"Stop"),(193,"CW slow..fast")]
GOBO2=[(0,"White"),(6,"Gobo 1"),(17,"Gobo 2"),(28,"Gobo 3"),(39,"Gobo 4"),(50,"Gobo 5"),
    (61,"Gobo 6"),(72,"Gobo 7"),(83,"Gobo 8"),(94,"Gobo 1 shake"),(106,"Gobo 2 shake"),
    (118,"Gobo 3 shake"),(130,"Gobo 4 shake"),(142,"Gobo 5 shake"),(154,"Gobo 6 shake"),
    (166,"Gobo 7 shake"),(178,"Gobo 8 shake"),(190,"CCW fast..slow"),(222,"Stop"),(224,"CW slow..fast")]
PATTFX=[(0,"Effect cut out"),(7,"Index 0-360"),(64,"CCW fast..slow"),(127,"Stop"),
    (129,"CW slow..fast"),(192,"Back-and-forth slow..fast")]
IRIS=[(0,"Large..small"),(226,"Slow open fast close"),(236,"Slow close fast open"),(246,"Slow close slow open")]
PRROT=[(0,"Index 0-360"),(128,"CCW fast..slow"),(190,"Stop"),(194,"CW slow..fast")]
STROBE=[(0,"Closed"),(4,"Sync strobe"),(100,"Pulse strobe"),(150,"Flash strobe"),(200,"Random strobe"),(250,"Open")]
MACRO=[(0,"No function"),(6,"H reverse open"),(21,"H reverse close"),(26,"V reverse open"),
    (31,"V reverse close"),(36,"Mobile light block ON"),(41,"Mobile light block OFF"),(46,"No function"),
    (51,"Fan auto"),(56,"Fan high speed"),(61,"Fan high silent"),(66,"Fan ultra-quiet"),
    (71,"Curve linear"),(76,"Curve square"),(81,"Curve inv square"),(86,"Curve S"),(91,"400Hz"),
    (96,"1200Hz"),(101,"2000Hz"),(106,"4000Hz"),(111,"6000Hz"),(116,"8000Hz"),(121,"16kHz"),
    (126,"24kHz"),(131,"Display backlight on"),(136,"Backlight 15s"),(141,"Backlight 30s"),
    (146,"Backlight 60s"),(151,"Dimmer speed smooth"),(156,"Dimmer speed fast"),(161,"Reset Pan/Tilt"),
    (166,"Reset moving head"),(171,"Reset all"),(176,"Signal keep on"),(181,"Signal keep off"),(186,"No function")]

CH=[
    C("PAN","POSITION","POSITION",2),
    C("TILT","POSITION","POSITION",2),
    C("PT_SPEED","POSITION","POSITION",1,sets=[(0,"Fast..slow")]),
    C("CYAN","COLOR","COLOR",1),
    C("MAGENTA","COLOR","COLOR",1),
    C("YELLOW","COLOR","COLOR",1),
    C("CTO","COLOR","COLOR",1),
    C("CRI","COLOR","COLOR",1,sets=[(0,"CRI filter out"),(128,"CRI filter in")]),
    C("COLOR1","COLOR","COLOR",2,sets=COLWHEEL),
    C("GOBO1","GOBO","GOBO",1,sets=GOBO1),
    C("GOBO1_POS","GOBO","GOBO",2,sets=ROT),
    C("GOBO2","GOBO","GOBO",1,sets=GOBO2),
    C("GOBO2_POS","GOBO","GOBO",1,sets=PATTFX),
    C("IRIS","BEAM","BEAM",2,sets=IRIS),
    C("PRISM1","BEAM","BEAM",1,sets=[(0,"Out"),(8,"In")]),
    C("PRISM1_POS","BEAM","BEAM",1,sets=PRROT),
    C("PRISM2","BEAM","BEAM",1,sets=[(0,"Out"),(8,"In")]),
    C("PRISM2_POS","BEAM","BEAM",1,sets=PRROT),
    C("FROST1","BEAM","BEAM",1,sets=[(0,"Off"),(128,"On")]),
    C("ZOOM","FOCUS","FOCUS",2,sets=[(0,"Wide..narrow")]),
    C("FOCUS","FOCUS","FOCUS",2),
    C("SHUTTER","BEAM","BEAM",1,sets=STROBE),
    C("DIM","DIMMER","DIMMER",2,hv=255),
    C("BLADE_ROT","SHAPERS","SHAPERS",2,sets=[(0,"0-180 deg")]),
    C("BLADE_UP_A","SHAPERS","SHAPERS",1),
    C("BLADE_UP_B","SHAPERS","SHAPERS",1),
    C("BLADE_LF_A","SHAPERS","SHAPERS",1),
    C("BLADE_LF_B","SHAPERS","SHAPERS",1),
    C("BLADE_DN_A","SHAPERS","SHAPERS",1),
    C("BLADE_DN_B","SHAPERS","SHAPERS",1),
    C("BLADE_RG_A","SHAPERS","SHAPERS",1),
    C("BLADE_RG_B","SHAPERS","SHAPERS",1),
    C("MACRO","CONTROL","CONTROL",1,sets=MACRO),
]

def ranges(sets):
    out=[]
    for i,(s,nm) in enumerate(sets):
        e = sets[i+1][0]-1 if i+1<len(sets) else 255
        out.append((s,e,nm))
    return out

L=['<?xml version="1.0" encoding="utf-8"?>']
L.append('<MA xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         'xsi:schemaLocation="http://schemas.malighting.de/grandma2/xml/MA http://schemas.malighting.de/grandma2/xml/2.8.123/MA.xsd" '
         'major_vers="2" minor_vers="8" stream_vers="123" xmlns="http://schemas.malighting.de/grandma2/xml/MA">')
L.append('\t<FixtureType name="Moving Head 800W 42CH" mode="42">')
L.append('\t\t<InfoItems><Info type="Revision" date="2026-09-04">800W CMY framing spot, 42CH mode</Info></InfoItems>')
L.append('\t\t<short_name>MH800</short_name>')
L.append('\t\t<manufacturer>Generic</manufacturer>')
L.append('\t\t<short_manufacturer>Generic</short_manufacturer>')
L.append('\t\t<Modules>')
L.append('\t\t\t<Module name="Main Module" class="Head" beamtype="Spot" beam_angle="18" beam_intensity="35000">')
off=1
for c in CH:
    coarse=off
    fine=off+1 if c["nbytes"]==2 else None
    off += c["nbytes"]
    attrs=f'attribute="{c["attr"]}" feature="{c["feature"]}" preset="{c["preset"]}" coarse="{coarse}"'
    if fine: attrs+=f' fine="{fine}"'
    if c["hv"] is not None: attrs+=f' highlight_value="{c["hv"]}"'
    L.append(f'\t\t\t\t<ChannelType {attrs}>')
    cf=(f'from="0" to="100" min_dmx_24="0" max_dmx_24="16777215" physfrom="0" physto="100" '
        f'subattribute="{c["attr"]}" attribute="{c["attr"]}" feature="{c["feature"]}" preset="{c["preset"]}"')
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
fp=off-1
assert fp==42, fp
open("Moving_Head_800W_42CH.xml","w",encoding="utf-8").write(xml+"\n")
print(f"Moving_Head_800W_42CH.xml written; ChannelTypes={len(CH)} footprint={fp}")

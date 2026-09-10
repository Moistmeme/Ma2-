#!/usr/bin/env python3
"""grandMA2 native fixture XML for the 117CH pixel batten.
Flat single-module profile (guaranteed import, same schema as the other MA2
profiles): 5 master channels + 32 RGB pixels + 16 White pixels = 117 channels.
Per-pixel colour controls from the encoders (labelled P01R..P32B / W01..W16)."""
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def ranges(sets):
    out=[]
    for i,(s,nm) in enumerate(sets):
        e=sets[i+1][0]-1 if i+1<len(sets) else 255
        out.append((s,e,nm))
    return out

# (attribute, feature, preset, sets, highlight_value)
CH=[
    ("DIM","DIMMER","DIMMER",[(0,"0..100%")],255),
    ("STRB_DUR","BEAM","BEAM",[],None),
    ("STRB_RATE","BEAM","BEAM",[],None),
    ("SHUTTER","BEAM","BEAM",[(0,"Open"),(1,"Strobe slow..fast")],None),
    ("ATOMIZE","CONTROL","CONTROL",[(0,"Off"),(1,"Diffuse low..high")],None),
]
for p in range(1,33):
    CH.append((f"P{p:02d}R","COLOR","COLOR",[],None))
    CH.append((f"P{p:02d}G","COLOR","COLOR",[],None))
    CH.append((f"P{p:02d}B","COLOR","COLOR",[],None))
for w in range(1,17):
    CH.append((f"W{w:02d}","COLOR","COLOR",[],255))

L=['<?xml version="1.0" encoding="utf-8"?>']
L.append('<MA xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         'xsi:schemaLocation="http://schemas.malighting.de/grandma2/xml/MA http://schemas.malighting.de/grandma2/xml/2.8.123/MA.xsd" '
         'major_vers="2" minor_vers="8" stream_vers="123" xmlns="http://schemas.malighting.de/grandma2/xml/MA">')
L.append('\t<FixtureType name="Pixel Batten 117CH" mode="117">')
L.append('\t\t<InfoItems><Info type="Revision" date="2026-09-10">Pixel batten: master + 32 RGB pixels + 16 White pixels, 117CH mode</Info></InfoItems>')
L.append('\t\t<short_name>PIX117</short_name>')
L.append('\t\t<manufacturer>Generic</manufacturer>')
L.append('\t\t<short_manufacturer>Generic</short_manufacturer>')
L.append('\t\t<Modules>')
L.append('\t\t\t<Module name="Main Module" class="Conventional" beamtype="Wash" beam_angle="110" beam_intensity="8000">')
off=1
for attr,feat,pre,sets,hv in CH:
    a=f'attribute="{attr}" feature="{feat}" preset="{pre}" coarse="{off}"'
    if hv is not None: a+=f' highlight_value="{hv}"'
    L.append(f'\t\t\t\t<ChannelType {a}>')
    cf=(f'from="0" to="100" min_dmx_24="0" max_dmx_24="16777215" physfrom="0" physto="100" '
        f'subattribute="{attr}" attribute="{attr}" feature="{feat}" preset="{pre}"')
    if sets:
        L.append(f'\t\t\t\t\t<ChannelFunction {cf}>')
        for s,e,nm in ranges(sets):
            L.append(f'\t\t\t\t\t\t<ChannelSet name="{escape(nm)}" from_dmx="{s}" to_dmx="{e}" />')
        L.append('\t\t\t\t\t</ChannelFunction>')
    else:
        L.append(f'\t\t\t\t\t<ChannelFunction {cf} />')
    L.append('\t\t\t\t</ChannelType>')
    off+=1
L.append('\t\t\t</Module>')
L.append('\t\t</Modules>')
L.append('\t\t<Instances><Instance module_index="0" patch="1" locked="true" /></Instances>')
L.append('\t\t<Wheels />')
L.append('\t</FixtureType>')
L.append('</MA>')
xml="\n".join(L)
ET.fromstring(xml)
fp=off-1
assert fp==117, fp
open("Pixel_Batten_117CH.xml","w",encoding="utf-8").write(xml+"\n")
print(f"Pixel_Batten_117CH.xml written; ChannelTypes={len(CH)} footprint={fp}")

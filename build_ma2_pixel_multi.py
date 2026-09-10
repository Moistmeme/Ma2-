#!/usr/bin/env python3
"""grandMA2 MULTI-INSTANCE fixture XML for the 117CH pixel batten.

Master module (5 ch) + one RGB-pixel module instanced 32x + one White-pixel
module instanced 16x, so MA2 patches it as a fixture with 48 colour-pickable
pixel sub-fixtures (X.1 .. X.48). Each RGB pixel uses COLORRGB1/2/3 so the
colour picker drives it.

NOTE: hand-built multi-instance - test-import in grandMA2 onPC before a show.
The flat Pixel_Batten_117CH.xml remains the guaranteed-import fallback.
"""
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

MASTER=[("DIM","DIMMER","DIMMER",255),("STRB_DUR","BEAM","BEAM",None),
        ("STRB_RATE","BEAM","BEAM",None),("SHUTTER","BEAM","BEAM",None),
        ("ATOMIZE","CONTROL","CONTROL",None)]
RGB=[("COLORRGB1","COLOR","COLOR"),("COLORRGB2","COLOR","COLOR"),("COLORRGB3","COLOR","COLOR")]
WHITE=[("COLORRGB4","COLOR","COLOR")]

def chtype(attr,feat,pre,coarse,hv=None):
    a=f'attribute="{attr}" feature="{feat}" preset="{pre}" coarse="{coarse}"'
    if hv is not None: a+=f' highlight_value="{hv}"'
    cf=(f'from="0" to="100" min_dmx_24="0" max_dmx_24="16777215" physfrom="0" physto="100" '
        f'subattribute="{attr}" attribute="{attr}" feature="{feat}" preset="{pre}"')
    return [f'\t\t\t\t<ChannelType {a}>', f'\t\t\t\t\t<ChannelFunction {cf} />',
            '\t\t\t\t</ChannelType>']

L=['<?xml version="1.0" encoding="utf-8"?>']
L.append('<MA xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         'xsi:schemaLocation="http://schemas.malighting.de/grandma2/xml/MA http://schemas.malighting.de/grandma2/xml/2.8.123/MA.xsd" '
         'major_vers="2" minor_vers="8" stream_vers="123" xmlns="http://schemas.malighting.de/grandma2/xml/MA">')
L.append('\t<FixtureType name="Pixel Batten 117CH Pixels" mode="117">')
L.append('\t\t<InfoItems><Info type="Revision" date="2026-09-10">Pixel batten, multi-instance: 5 master + 32 RGB pixels + 16 White pixels</Info></InfoItems>')
L.append('\t\t<short_name>PIX117M</short_name>')
L.append('\t\t<manufacturer>Generic</manufacturer>')
L.append('\t\t<short_manufacturer>Generic</short_manufacturer>')
L.append('\t\t<Modules>')
# module 0: master
L.append('\t\t\t<Module name="Master" class="Conventional" beamtype="Wash" beam_angle="110" beam_intensity="8000">')
for i,(attr,feat,pre,hv) in enumerate(MASTER,1):
    L+=chtype(attr,feat,pre,i,hv)
L.append('\t\t\t</Module>')
# module 1: RGB pixel
L.append('\t\t\t<Module name="RGB Pixel" class="Conventional" beamtype="Wash" beam_angle="110" beam_intensity="200">')
for i,(attr,feat,pre) in enumerate(RGB,1):
    L+=chtype(attr,feat,pre,i)
L.append('\t\t\t</Module>')
# module 2: white pixel
L.append('\t\t\t<Module name="White Pixel" class="Conventional" beamtype="Wash" beam_angle="110" beam_intensity="200">')
for i,(attr,feat,pre) in enumerate(WHITE,1):
    L+=chtype(attr,feat,pre,i)
L.append('\t\t\t</Module>')
L.append('\t\t</Modules>')
# instances
L.append('\t\t<Instances>')
L.append('\t\t\t<Instance module_index="0" patch="1" locked="true" name="Master" />')
addr=set(range(1,6))
for k in range(32):
    patch=6+3*k
    L.append(f'\t\t\t<Instance module_index="1" patch="{patch}" name="Pixel {k+1}" />')
    for j in range(3): addr.add(patch+j)
for k in range(16):
    patch=102+k
    L.append(f'\t\t\t<Instance module_index="2" patch="{patch}" name="White {k+1}" />')
    addr.add(patch)
L.append('\t\t</Instances>')
L.append('\t\t<Wheels />')
L.append('\t</FixtureType>')
L.append('</MA>')
xml="\n".join(L)
ET.fromstring(xml)
assert addr==set(range(1,118)), (min(addr),max(addr),len(addr))
open("Pixel_Batten_117CH_MultiInstance.xml","w",encoding="utf-8").write(xml+"\n")
print(f"Pixel_Batten_117CH_MultiInstance.xml written; instances={1+32+16} "
      f"footprint {min(addr)}..{max(addr)}={len(addr)} (contiguous, no overlap)")

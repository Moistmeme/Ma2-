#!/usr/bin/env python3
"""Generate a grandMA3 GDTF for the 117-channel pixel batten.

Layout (117ch): 5 master channels, then 32 RGB pixels (ch6-101) and 16 White
pixels (ch102-117). Built as a proper GDTF matrix: the RGB pixel and White pixel
are each defined once as a referenced geometry, then instantiated via
GeometryReference/Break so grandMA3 sees 48 individually controllable pixels.

Break DMXOffset applies a shift of (DMXOffset - 1) to the channels authored on
the referenced geometry (per GDTF spec, verified against the 4-head example).
"""
import xml.etree.ElementTree as ET
import zipfile
from xml.sax.saxutils import escape

N_RGB = 32          # RGB pixels, ch 6..101
N_W   = 16          # White pixels, ch 102..117
RGB_BASE = 6        # first RGB channel (Red 1)
W_BASE   = RGB_BASE + N_RGB*3   # 102, first White channel

def A(**kw):
    return " ".join(f'{k}="{escape(str(v))}"' for k,v in kw.items() if v not in (None,""))

POS = ("{1.000000,0.000000,0.000000,%.6f}"
       "{0.000000,1.000000,0.000000,0.000000}"
       "{0.000000,0.000000,1.000000,0.000000}"
       "{0.000000,0.000000,0.000000,1.000000}")

def xpos(k, n, span=1.0):
    if n == 1: return 0.0
    return -span/2 + k*(span/(n-1))

L = []
L.append('<?xml version="1.0" encoding="UTF-8"?>')
L.append('<GDTF DataVersion="1.1">')
L.append('  '+ '<FixtureType '+A(
    Name="Pixel Batten 117CH", ShortName="PIXBAT117",
    LongName="RGB+W Pixel Batten 117CH (32 RGB + 16 White pixels)",
    Description="Pixel batten: master dimmer/strobe/atomization + 32 RGB pixels + 16 White pixels",
    Manufacturer="Generic",
    FixtureTypeID="6A1B2C3D-0000-4000-8000-000000000117")+'>')

# ---- attribute definitions ----
L.append('    <AttributeDefinitions>')
L.append('      <ActivationGroups>')
L.append('        <ActivationGroup Name="ColorRGB"/>')
L.append('      </ActivationGroups>')
L.append('      <FeatureGroups>')
for fg,feats in [("Dimmer",["Dimmer"]),("Color",["RGB"]),
                 ("Beam",["Beam"]),("Control",["Control"])]:
    L.append(f'        <FeatureGroup Name="{fg}" Pretty="{fg}">')
    for fn in feats: L.append(f'          <Feature Name="{fn}"/>')
    L.append('        </FeatureGroup>')
L.append('      </FeatureGroups>')
L.append('      <Attributes>')
attrs = [
    ("Dimmer","Dim","Dimmer.Dimmer","LuminousIntensity",None,None),
    ("StrobeDuration","Strb Dur","Beam.Beam","Time",None,None),
    ("StrobeRate","Strb Rate","Beam.Beam","Frequency",None,None),
    ("Shutter1Strobe","Strobe","Beam.Beam","Frequency",None,None),
    ("Atomization","Atomize","Control.Control","None",None,None),
    ("ColorAdd_R","R","Color.RGB","ColorComponent","ColorRGB","0.6400,0.3300,21.30"),
    ("ColorAdd_G","G","Color.RGB","ColorComponent","ColorRGB","0.3000,0.6000,71.50"),
    ("ColorAdd_B","B","Color.RGB","ColorComponent","ColorRGB","0.1500,0.0600,7.20"),
    ("ColorAdd_W","W","Color.RGB","ColorComponent","ColorRGB","0.3130,0.3290,100.0"),
]
for name,pretty,feat,unit,act,color in attrs:
    L.append('        <Attribute '+A(Name=name,Pretty=pretty,ActivationGroup=act,
             Feature=feat,PhysicalUnit=(unit if unit!="None" else None),Color=color)+'/>')
L.append('      </Attributes>')
L.append('    </AttributeDefinitions>')

# ---- wheels / models ----
L.append('    <Wheels/>')
L.append('    <Models>')
L.append('      <Model Name="Body" Length="1.0" Width="0.12" Height="0.10" PrimitiveType="Cube"/>')
L.append('      <Model Name="Pixel" Length="0.03" Width="0.03" Height="0.02" PrimitiveType="Cylinder"/>')
L.append('      <Model Name="WPixel" Length="0.03" Width="0.03" Height="0.02" PrimitiveType="Cylinder"/>')
L.append('    </Models>')

# ---- geometries ----
L.append('    <Geometries>')
L.append('      <Beam '+A(Name="RGBPixel",Model="Pixel",LampType="LED",PowerConsumption="10",
         LuminousFlux="800",ColorTemperature="6500",BeamAngle="110",FieldAngle="110",
         BeamRadius="0.015",BeamType="Wash",ColorRenderingIndex="80")+'/>')
L.append('      <Beam '+A(Name="WhitePixel",Model="WPixel",LampType="LED",PowerConsumption="8",
         LuminousFlux="900",ColorTemperature="6500",BeamAngle="110",FieldAngle="110",
         BeamRadius="0.015",BeamType="Wash",ColorRenderingIndex="80")+'/>')
L.append('      <Geometry Name="Body" Model="Body">')
for k in range(N_RGB):
    off = 3*k + 1                       # shift = off-1 = 3k
    L.append(f'        <GeometryReference {A(Name=f"RGB{k+1}",Geometry="RGBPixel",Position=POS%xpos(k,N_RGB))}>')
    L.append(f'          <Break DMXOffset="{off}"/>')
    L.append('        </GeometryReference>')
for k in range(N_W):
    off = k + 1                         # shift = k
    L.append(f'        <GeometryReference {A(Name=f"W{k+1}",Geometry="WhitePixel",Position=POS%xpos(k,N_W))}>')
    L.append(f'          <Break DMXOffset="{off}"/>')
    L.append('        </GeometryReference>')
L.append('      </Geometry>')
L.append('    </Geometries>')

# ---- dmx mode ----
def chan(offset, attr, geo, default="0/1", highlight=None, sets=None):
    o=[]
    o.append('          <DMXChannel '+A(DMXBreak="1",Offset=str(offset),Default=default,
             Highlight=highlight,Geometry=geo)+'>')
    o.append(f'            <LogicalChannel Attribute="{attr}">')
    cf=A(Attribute=attr,Name=attr+" 1",DMXFrom="0/1",Default=default)
    if sets:
        o.append('              <ChannelFunction '+cf+'>')
        for d,nm in sets:
            o.append(f'                <ChannelSet Name="{escape(nm)}" DMXFrom="{d}/1"/>')
        o.append('              </ChannelFunction>')
    else:
        o.append('              <ChannelFunction '+cf+'/>')
    o.append('            </LogicalChannel>')
    o.append('          </DMXChannel>')
    return o

L.append('    <DMXModes>')
L.append('      <DMXMode '+A(Name="117CH",Geometry="Body")+'>')
L.append('        <DMXChannels>')
# master channels on Body
L += chan(1,"Dimmer","Body",highlight="255/1",sets=[(0,"0..100%")])
L += chan(2,"StrobeDuration","Body")
L += chan(3,"StrobeRate","Body")
L += chan(4,"Shutter1Strobe","Body",sets=[(0,"Open"),(1,"Strobe slow..fast")])
L += chan(5,"Atomization","Body",sets=[(0,"Off"),(1,"Diffuse low..high")])
# one RGB pixel definition (authored at absolute pixel-1 offsets), replicated by references
L += chan(RGB_BASE+0,"ColorAdd_R","RGBPixel",highlight="255/1")
L += chan(RGB_BASE+1,"ColorAdd_G","RGBPixel",highlight="255/1")
L += chan(RGB_BASE+2,"ColorAdd_B","RGBPixel",highlight="255/1")
# one White pixel definition, replicated by references
L += chan(W_BASE,"ColorAdd_W","WhitePixel",highlight="255/1")
L.append('        </DMXChannels>')
L.append('      </DMXMode>')
L.append('    </DMXModes>')
L.append('  </FixtureType>')
L.append('</GDTF>')

xml="\n".join(L)
ET.fromstring(xml)  # well-formed check

# ---- validate expanded footprint ----
addr=set()
def add(a):
    assert a not in addr, f"overlap at {a}"
    addr.add(a)
for a in range(1,6): add(a)
for k in range(N_RGB):
    shift=(3*k+1)-1
    for base in (RGB_BASE,RGB_BASE+1,RGB_BASE+2): add(base+shift)
for k in range(N_W):
    shift=(k+1)-1
    add(W_BASE+shift)
lo,hi=min(addr),max(addr)
assert lo==1 and hi==117 and len(addr)==117 and addr==set(range(1,118)), (lo,hi,len(addr))

with zipfile.ZipFile("Pixel_Batten_117CH.gdtf","w",zipfile.ZIP_DEFLATED) as z:
    z.writestr("description.xml",xml)
print(f"Pixel_Batten_117CH.gdtf written; expanded footprint {lo}..{hi} = {len(addr)} channels (contiguous, no overlap)")
print(f"RGB pixels: {N_RGB} (ch{RGB_BASE}-{RGB_BASE+N_RGB*3-1}) | White pixels: {N_W} (ch{W_BASE}-{W_BASE+N_W-1})")

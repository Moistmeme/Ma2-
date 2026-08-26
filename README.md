# Laser Moving Head — grandMA2 Fixture Profile (29CH STD)

grandMA2 fixture type for a generic **laser moving head** in its **STD / 29-channel** DMX mode,
built from the manufacturer's DMX-512 channel description.

- **File:** `Laser_Moving_Head_29CH.xml`
- **Mode:** `29CH STD`
- **DMX footprint:** 29 channels (Pan and Tilt are 16-bit, so they use 2 DMX slots each)
- **Target:** grandMA2 v3.x (onPC or console). The file declares schema `3.9.60`; MA auto-migrates on import.

> The `PRO / 46CH` mode in the manual (dual-pattern function switch) is **not** included — that
> table is truncated in the source photos. Once the full 46CH list is available it can be added as a
> second `<Mode>` in the same fixture type.

## Import into grandMA2

1. `Setup` → `Patch & Fixture Schedule` → `Fixture Types`.
2. Press `Import` and select `Laser_Moving_Head_29CH.xml`
   (copy it to `gma2/importexport/` on the console/USB first, or browse to it in onPC).
3. Patch fixtures using the `29CH STD` mode.

## Channel plot (STD mode — 29 channels)

| DMX | Parameter | MA Attribute | Feature | Ranges |
|----:|-----------|--------------|---------|--------|
| 1 | X-axis (Pan) coarse | PAN | Position / PanTilt | 16-bit with ch 2 |
| 2 | X-axis (Pan) fine | PAN (fine) | Position / PanTilt | — |
| 3 | Y-axis (Tilt) coarse | TILT | Position / PanTilt | 16-bit with ch 4 |
| 4 | Y-axis (Tilt) fine | TILT (fine) | Position / PanTilt | — |
| 5 | X/Y speed | PT SPEED | Position / PanTilt | 0 = max, 1–255 fast→slow |
| 6 | Head system reset | RESET | Control | 0–250 none · 251–255 reset (3 s delay) |
| 7 | Switching lights / dimmer | DIM | Dimmer | 0 = off · 1–255 = 1–100% |
| 8 | Auto effect speed / voice | EFFECT SPEED | Effect | 0–26 default · 27–127 slow→fast · 128–255 voice sensitivity |
| 9 | Pattern / effect group | GOBO1 | Gobo | 0–127 pattern grp (per 16) · 128–255 effect grp (per 16) |
| 10 | Pattern / effect select | GOBO2 | Gobo | pattern per 5; effect: 0–1 all, then per 2 |
| 11 | Strobe | STROBE | Beam / Shutter | 0 open · 1–255 slow→fast |
| 12 | Pattern size | ZOOM | Beam / Zoom | 0–255 large→small |
| 13 | Horizontal position MSB | XYZ_X | Position / PanTilt | 128 = centre; light off outside boundary |
| 14 | Vertical position MSB | XYZ_Y | Position / PanTilt | 128 = centre; light off outside boundary |
| 15 | Colour | COLOR1 | Color | 0–3 original · 4–31 fixed (per 4) · 32–35 rainbow · 36–39 RGB · 40–43 change · 44–239 flow (per 4) · 240–255 gradual draw |
| 16 | Colour speed | COLOR SPEED | Color | 0–3 off · 4–127 slow→fast · 128–255 slow→fast reversed |
| 17 | Pattern line / point | EFFECT | Beam | 0–63 highlight line · 64–127 line scan · 128–255 point scan |
| 18 | Rotate Z | GOBO1_POS | Gobo | 0–127 angle · 128–255 speed |
| 19 | Rotate X | GOBO2_POS | Gobo | 0–127 angle · 128–255 speed |
| 20 | Rotate Y | GOBO3_POS | Gobo | 0–127 angle · 128–255 speed |
| 21 | Horizontal movement | EFFECT2 | Effect | 0–127 position · 128–255 speed |
| 22 | Vertical movement | EFFECT3 | Effect | 0–127 position · 128–255 speed |
| 23 | Pattern size / zoom | ZOOM2 | Beam / Zoom | 0–127 size large→small · 128–255 zoom speed |
| 24 | Gradual drawing | EFFECT4 | Effect | 0 off · 1–255 speed |
| 25 | X / Y waves | EFFECT5 | Effect | 0 off · 1–127 X wave · 128–255 Y wave |
| 26 | LED brightness | DIM2 | Dimmer | 0–255 = 0–100% |
| 27 | LED effects | EFFECT6 | Effect | select per 8 |
| 28 | LED effects speed | EFFECT7 | Effect | 0–255 slow→quick |
| 29 | LED strobe | STROBE2 | Beam / Shutter | 0 open · 1–255 slow→fast |

## Mapping notes

- **Pan / Tilt** are 16-bit (coarse+fine). Physical ranges are placeholders: Pan `540°`, Tilt `270°` —
  set these to your actual fixture's travel in the fixture editor if you need accurate 3D/position values.
- **Pattern / rotate channels** are mapped onto MA's `Gobo` attributes so they land on the Gobo
  encoders — natural for a laser's pattern engine.
- **Two dimmers and two strobes** exist: laser output (ch 7 / 11) and the on-board **LED** wash
  (ch 26 / 29). They are mapped to `DIM`/`DIM2` and `STROBE`/`STROBE2` so both live on sensible encoders.
- **CH13/CH14 horizontal & vertical position** are the pattern's in-field offset (128 = centre), which
  is distinct from the head's Pan/Tilt — mapped to `XYZ_X`/`XYZ_Y` to keep them off the main Pan/Tilt encoders.
- Attribute names such as `EFFECT2…7` are generic; rename any of them in the fixture editor
  (`Edit` the channel → `Attribute`) if you prefer different encoder labels.

## Verify before the show

MA's XML import is strict. After importing, open the fixture type and confirm all 29 channels appear
in the `29CH STD` mode with the ranges above, then patch one unit and check Pan/Tilt, dimmer, strobe,
and pattern encoders respond. The table above is the authoritative spec, so anything MA rejects on
import can be finished in a couple of minutes in the fixture editor. Recommended: test-import in
**grandMA2 onPC** (free) first.

# RGB+L Moving Head with Aura Rings — grandMA2 Fixture Profile (39CH)

grandMA2 fixture type for a moving head with a 120 W RGB+L engine plus **inner and outer
Aura-style LED rings**, in its **39-channel** mode (DMX / ArtNet / sACN).

- **File:** `Moving_Head_39CH.xml`
- **Mode name:** `39`
- **DMX footprint:** 39 channels
- **Schema:** native grandMA2 `2.8.123` (imports on MA2 2.x and 3.x)
- **Structure:** one `<Module>`, each channel a `<ChannelType>` with its DMX slot on `coarse` (`fine` for 16-bit), one `<Instance patch="1">`. Same verified layout as the 29CH laser profile.

## Import

`Setup` → `Patch & Fixture Schedule` → `Fixture Types` → `Import` → select `Moving_Head_39CH.xml`.

## Channel plot (39CH)

| DMX | Function | MA Attribute | Group | Notes |
|----:|----------|--------------|-------|-------|
| 1–2 | Pan (16-bit) | PAN | Position | 540° |
| 3–4 | Tilt (16-bit) | TILT | Position | 230° |
| 5 | X/Y speed | PT_SPEED | Position | fast→slow |
| 6–7 | Zoom (16-bit) | ZOOM | Beam | small→large angle |
| 8–9 | 120 W LED dimmer (16-bit) | DIM | Dimmer | 0–100% |
| 10 | Strobe | SHUTTER | Beam | open/closed/pulse/ramp/random/break/strobe |
| 11–12 | Red (16-bit) | COLORRGB1 | Color | main engine |
| 13–14 | Green (16-bit) | COLORRGB2 | Color | main engine |
| 15–16 | Blue (16-bit) | COLORRGB3 | Color | main engine |
| 17–18 | L / White (16-bit) | COLORRGB4 | Color | main engine 4th emitter |
| 19 | Inner ring dimmer | INNER_DIM | Dimmer | |
| 20 | Inner ring Red | INNER_R | Color | |
| 21 | Inner ring Green | INNER_G | Color | |
| 22 | Inner ring Blue | INNER_B | Color | |
| 23 | Inner ring Warm White | INNER_WW | Color | |
| 24 | Inner ring Strobe | INNER_STROBE | Beam | same 9-state table as ch10 |
| 25 | Outer ring dimmer | OUTER_DIM | Dimmer | |
| 26 | Outer ring Red | OUTER_R | Color | |
| 27 | Outer ring Green | OUTER_G | Color | |
| 28 | Outer ring Blue | OUTER_B | Color | |
| 29 | Outer ring Warm White | OUTER_WW | Color | |
| 30 | Outer ring Strobe | OUTER_STROBE | Beam | same 9-state table as ch10 |
| 31 | CCT | CTC | Color | Off, 1800K…8000K (16 steps) |
| 32 | Tint | TINT | Color | Magenta↔Off↔Green (128 = off) |
| 33 | Colour macros | COLORMACRO | Color | 15 gels + rainbow/jump/gradient |
| 34 | Inner ring effect | INNER_FX | Control | Off, Effect 1–10, Built-in 1–10 |
| 35 | Inner ring effect speed | INNER_FXSPEED | Control | index / stop / CW / CCW |
| 36 | Outer ring effect | OUTER_FX | Control | Off, Effect 1–10, Built-in 1–10 |
| 37 | Outer ring effect speed | OUTER_FXSPEED | Control | index / stop / CW / CCW |
| 38 | Function / settings / reset | FUNCTION | Control | display, dimming curve, PWM, fan, reversals, resets (hold ~3 s) |
| 39 | Working mode | MODE | Control | DMX / Mixed(pixel) / ArtNet |

## Mapping notes

- **Main colour engine (ch 11–18)** is mapped to MA's real `COLORRGB1–4`, so the **colour picker
  drives the beam** directly. All four are 16-bit (coarse+fine).
- **The two rings** are given clearly-labelled custom colour attributes (`INNER_*` / `OUTER_*`).
  They control fully from the encoders but are **not** driven by the main colour picker, because a
  single flat fixture can only hold one `COLORRGB1–4` set.
  → If you want each ring to behave as its own colour-pickable sub-fixture, I can rebuild this as a
  **multi-instance** fixture (Main + Inner Ring + Outer Ring sub-fixtures). Say the word.
- **CCT / Tint / Colour macros** sit on the Color encoders. `CTC` is MA's colour-temperature
  attribute; `TINT` centres at 128.
- **Effects, Function and Mode** are placed under `Control` for a guaranteed import; rename or
  re-home any of them in the fixture editor if you prefer different encoder pages.
- **`L` (ch 17/18)** is the engine's 4th emitter, mapped to White (`COLORRGB4`). If it's actually
  Lime on your unit, tell me and I'll switch it to `COLORRGB7` (Lime).

## Verify before the show

After import, confirm **DMX Footprint = 39**, Pan/Tilt/Zoom/Dimmer read as 16-bit, the colour picker
drives the main beam, and both rings + strobes respond on their encoders. The table above is the
authoritative spec if you want to fine-tune anything in the editor.

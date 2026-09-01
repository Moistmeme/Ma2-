# grandMA3 (GDTF) versions — Laser 29CH & Moving Head 39CH

grandMA3 imports fixtures as **GDTF** files (a `.gdtf` is a zip containing `description.xml`).
These are GDTF re-creations of the two MA2 profiles.

- `Laser_Moving_Head_29CH.gdtf` — 29-channel laser moving head (footprint 29)
- `Moving_Head_39CH.gdtf` — RGB+L moving head with inner/outer Aura rings (footprint 39)
- `build_gdtf.py` — generator/source for both (edit + re-run to regenerate)

Both are GDTF **DataVersion 1.1**, one `DMXMode` each, with a Base→Yoke→Head→Beam geometry tree
so Pan/Tilt drive the axes in the 3D view.

## Import into grandMA3

1. Copy the `.gdtf` file(s) to a USB stick (or the gma3 library folder).
2. In grandMA3: `Menu` → `Patch` → `Import` (or **Fixture Types** → Import) → pick the `.gdtf`.
3. Patch using the single DMX mode in each.

## What maps to real GDTF attributes

- **Pan / Tilt** (16-bit), **Dimmer**, **Shutter1Strobe**, **Zoom**, **Gobo1/Gobo2** and
  **Gobo1Pos/Gobo2Pos/Gobo3Pos** (pattern rotate), **Color1**, **ColorMacro1**, **CTC** — all
  standard GDTF attributes, so they land on the right MA3 encoders and icons.
- **39CH main colour** → `ColorAdd_R/G/B/W` (16-bit each) with CIE values, so the **MA3 colour
  picker drives the main beam**.
- **Laser-specific / ring / effect functions** (X/Y speed, pattern position, waves, gradual draw,
  the two Aura rings, per-ring effects, Function, Mode, etc.) use **custom attributes** with sensible
  feature groups (Position / Color / Beam / Control). They control fully from the encoders; the ring
  colours are custom attributes, so — as in the MA2 version — they are not driven by the main colour
  picker. Ask if you want a multi-instance (sub-fixture) ring version.

## Notes

- Pan 540° / Tilt 230° (laser Tilt 230°→ set as ±115). Adjust in the GDTF Builder if your unit differs.
- `FixtureGlobalReset` carries the laser's head-reset; `Function` carries the moving head's
  settings/reset menu.
- If you'd rather have native MA3 `.xml` fixture exports instead of GDTF, tell me — but GDTF is the
  recommended, portable route for MA3.

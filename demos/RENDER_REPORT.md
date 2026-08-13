# Demo Render Report

Rendered offline via Spotify pedalboard 0.9.17 (Python 3.11 venv at ~/sebastianmacan/demos-venv).
Script: ~/sebastianmacan/demos-work/render_demos.py. All audio 44.1kHz stereo, WAV normalized to -1 dBFS peak.
MP3s (192kbps) encoded with pedalboard's built-in LAME — no ffmpeg required.

## Source material (synthesized with numpy)
- Drum loop: 8 bars @ 120bpm — synthesized kick (pitch-swept sine + click), snare (filtered noise + 190Hz body), panned closed/open hats; light tanh glue.
- Pad loop: Am–F–C–G progression, detuned 3-osc saw stack, one-pole LP @ 2.2kHz, 16s.

## Renders — ALL SUCCEEDED
| File | Duration | Notes |
|---|---|---|
| chaos_dry.wav/.mp3 | 16.0s | drum loop, unprocessed |
| chaos_wet.wav/.mp3 | 16.0s | seed=-1, chaos_amount=0.85, all 6 slots enabled, dry/wet=0.8 (picked most-different of 4 seeds by RMS diff) |
| ghost_dry.wav/.mp3 | 16.0s | pad loop, unprocessed |
| ghost_wet.wav/.mp3 | 16.0s | chunked render (0.25s blocks); freeze engaged at 50%, position swept sinusoidally, pitch rises +12st, scatter opens up; shimmer 0.5, smear 0.6, reverb 0.6, mix 0.85 |
| dusty_vhs_memories.wav/.mp3 | 14.7s | MIDI chord progression (Am9–Fmaj7–C–G/B rolled chords @ 82bpm) + top melody |
| dusty_dusty_rhodes.wav/.mp3 | 14.7s | same MIDI, 'Dusty Rhodes' preset |
| dusty_thrift_store_bells.wav/.mp3 | 14.7s | same MIDI, 'Thrift Store Bells' preset |

## Plugin loading facts
- Chaos: FX, 30 params (seed, chaos_amount, lock, dry_wet, 6 slots x enable+3 params). Loaded clean.
- Ghost: FX, 15 params (freeze, position, grain_size, density, scatter, pitch ±24st, shimmer, reverse, smear, drift, tone, reverb, mix, output). Loaded clean. Parameter automation between process() blocks works (reset=False).
- Dusty: is_instrument=True, 30 factory presets exposed via `program` parameter. Accepts raw MIDI as (bytes, timestamp) tuples — mido not needed.

## Caveats
- MP3 lossy encoding overshoots peaks slightly (chaos_dry.mp3 peaks +2.5 dBFS inter-sample); WAVs are exactly -1 dBFS. If this matters for web playback, re-normalize MP3 sources to -3 dB.
- Chaos seed values 0.33/0.77/-1.0 produced identical output (seed appears binary/randomize-trigger); seed=0.0 was slightly different.

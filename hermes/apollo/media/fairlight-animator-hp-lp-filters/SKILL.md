---
name: fairlight-animator-hp-lp-filters
description: "High/Low Pass filters for Fairlight Animator Modifier."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fairlight, Animator, Audio, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Fairlight Animator Modifier HP/LP Filters

## When to Use

Use when you need to selectively include/exclude frequency ranges from source audio to drive animation parameters. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 9:42-10:01
- **Resolve Page:** Fairlight

## Tool Location
Fairlight page → Animator Modifier → Filter controls

## New Filter Controls
| Filter | Function | Use Case |
|--------|----------|----------|
| High Pass | Exclude low frequencies | Remove rumble, isolate transients |
| Low Pass | Exclude high frequencies | Isolate bass, remove harshness |

## Workflow
1. Add Animator Modifier to parameter
2. Select audio source track
3. Enable High Pass Filter
4. Set cutoff frequency (e.g., 200Hz)
5. Enable Low Pass Filter
6. Set cutoff frequency (e.g., 5kHz)
6. Parameter now driven by filtered band

## Parameter Mapping
| Parameter | Frequency Range | Animation Use |
|-----------|-----------------|---------------|
| Bass/Kick | 20-200Hz (LP 200Hz) | Scale, position punch |
| Midrange | 200-5kHz (HP 200, LP 5k) | Color, rotation |
| Treble/Snare | 5-20kHz (HP 5kHz) | Opacity, particle emission |

## Use Cases
- Bass-driven scale animations
- Snare-triggered flash effects
- Vocal-driven parameter modulation
- Frequency-specific visualizers
- Dialogue-synced animations

## Tips
- Combine HP+LP for band-pass isolation
- Animate cutoff frequencies for sweeps
- Use multiple Animators with different bands
- Preview audio waveform in Animator panel

## Cross-References
- **Related Skills:** `fairlight-audio-mixing`, `fusion-animator-basics`
- **Tags:** `fairlight`, `animator`, `filters`, `audio-driven`, `v21.1`
- **Collection:** `fairlight-animator`
---
name: camera-gear-workflow
description: Camera hardware selection and setup for video production
category: camera-hardware
tags: [camera, gear, sensor, lens-mount, codec, workflow, setup]
difficulty: beginner
---

# Camera Gear Workflow

Selecting, configuring, and managing camera equipment for professional video production.

## Sensor Formats & Implications

| Format | Crop Factor | Typical Use | Trade-offs |
|--------|-------------|-------------|------------|
| **Full Frame** (36×24mm) | 1.0x | Cinema, high-end photo | Best low-light, shallow DOF, expensive lenses |
| **Super 35 / APS-C** (~23×15mm) | 1.5x | Cinema, broadcast | Cinema standard, lens options, good DR |
| **Micro 4/3** (17×13mm) | 2.0x | Documentary, gimbal, drone | Compact, deep DOF, speedboosters available |
| **1-inch** (13×9mm) | 2.7x | Broadcast, webcam, compact | Portable, limited DOF control |
| **Medium Format** (44×33mm) | 0.79x | High-end commercial | Ultimate detail, slow, expensive |

## Codec & Recording Options

### Internal Recording
| Codec | Bit Depth | Chroma | Typical Bitrate | Use Case |
|-------|-----------|--------|-----------------|----------|
| **H.264** | 8-bit | 4:2:0 | 100-400 Mbps | Delivery, quick turnaround |
| **H.265/HEVC** | 10-bit | 4:2:0/4:2:2 | 200-800 Mbps | HDR, efficient storage |
| **All-I** | 8/10-bit | 4:2:2 | 400-600 Mbps | Editing-friendly, no GOP |
| **ProRes** | 10-bit | 4:2:2 | 470-1800 Mbps | Pro post, Mac optimized |
| **RAW** (BRAW, ProRes RAW, CinemaDNG) | 12-16-bit | — | 1-6 Gbps | Maximum latitude, heavy |

### External Recording (Atomos, Blackmagic)
- **Benefits**: Better codecs, monitoring, longer record times
- **Common**: ProRes RAW, BRAW, ProRes 422 HQ
- **HDMI/SDI**: 10-bit 4:2:2 output from most mirrorless

## Picture Profiles & Log Curves

| Manufacturer | Log Profile | Dynamic Range | Middle Gray | White Clip |
|-------------|-------------|---------------|-------------|------------|
| **Sony** | S-Log3 | 14+ stops | 41% IRE | 94% IRE |
| **Canon** | C-Log3 / C-Log2 | 13-14 stops | 40-45% IRE | 92% IRE |
| **Panasonic** | V-Log / V-LogL | 14+ stops | 42% IRE | 95% IRE |
| **Nikon** | N-Log | 12-13 stops | 38% IRE | 90% IRE |
| **Fujifilm** | F-Log2 | 14+ stops | 36% IRE | 92% IRE |
| **Blackmagic** | BRAW / Film | 13-14 stops | 40% IRE | 95% IRE |
| **DJI** | D-Log / D-Log M | 12-13 stops | 40% IRE | 90% IRE |

**Exposure Rule**: Expose Log 1-2 stops OVER middle gray for clean shadows.

## Lens Mount Systems

| Mount | Flange Distance | Diameter | Notable Cameras |
|-------|----------------|----------|-----------------|
| **E-mount** | 18mm | 46mm | Sony, Zeiss, Sigma, Tamron |
| **RF-mount** | 20mm | 54mm | Canon |
| **Z-mount** | 16mm | 55mm | Nikon |
| **L-mount** | 20mm | 51mm | Panasonic, Leica, Sigma |
| **X-mount** | 17.7mm | 44mm | Fujifilm |
| **MFT** | 19.25mm | 38mm | Panasonic, OM System, Blackmagic |
| **PL-mount** | 52mm | 54mm | Cinema (Arri, RED, Sony Venice) |

**Adapters**: Speedboosters (0.71x, 0.64x) gain 1-1.33 stops + wider FOV.

## Essential Accessories

### Monitoring
- **On-camera**: 5-7" 1000+ nits (SmallHD, PortKeys, Feelworld)
- **External REC+Monitor**: Atomos Ninja V, Shinobi
- **Waveform/Vector**: Built-in or external (Atomos, SmallHD)

### Audio
- **On-camera**: Rode VideoMic NTG, Deity V-Mic D4
- **Wireless**: DJI Mic, Rode Wireless GO II, Sennheiser AVX
- **Field recorder**: Zoom F6, Sound Devices MixPre-3
- **Timecode**: Tentacle Sync, UltraSync Blue

### Power
- **V-Mount / Gold Mount**: High capacity (95-200Wh)
- **NP-F / BP-U**: Mirrorless standard (20-50Wh)
- **PD USB-C**: 65-100W for modern cameras
- **Dummy batteries**: NP-FW50, LP-E6, EN-EL15

### Stabilization
- **Gimbal**: DJI RS 3/4, Zhiyun Weebill 3, Moza AirCross
- **Shoulder rig**: Tilta, SmallRig, Wooden Camera
- **Easyrig**: Weight distribution for long takes

## DaVinci Resolve Camera Integration

### Camera RAW Panel
- **Clip Attributes** → **RAW** tab
- Decode Quality: Full / Half / Quarter
- Color Space / Gamma override
- Highlight Recovery, Noise Reduction

### Color Management (Project Settings)
```
Color Science: DaVinci YRGB Color Managed
Input Color Space: [Camera Log] (auto-detect from RAW)
Timeline Color Space: DaVinci Wide Gamut Intermediate
Output Color Space: Rec.709 / P3 / Rec.2020
```

### LUT Workflow
1. **Camera LUT** (Technical): Log → Scene-referred
2. **Creative LUT**: Look development
3. **Output LUT** (Technical): Scene → Display

## Media Management

### Folder Structure
```
/ProjectName
  /01_CAMERA_ORIGINALS
    /A_CAM
      /YYYYMMDD
        /CLIPS
    /B_CAM
  /02_AUDIO
  /03_PROJECT_FILES
  /04_EXPORTS
  /05_LUTS
```

### Naming Convention
```
PROJ_SCENE_SHOT_TAKE_CAM_SETTINGS
EX: COMM_012_003_04_A_SLOG3_4K24
```

### Backup Protocol
- **3-2-1 Rule**: 3 copies, 2 media types, 1 offsite
- **Checksum**: xxHash / MD5 verify on copy
- **Verify**: Spot-check frames after transfer

## Tags
`camera` `gear` `sensor` `lens-mount` `codec` `workflow` `setup` `log` `raw` `media-management`
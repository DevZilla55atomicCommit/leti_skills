---
name: photon-setup-guide
description: "Guide for configuring iMessage (via Photon) in Hermes Agent, including troubleshooting steps."
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  category: apple
  created: 2026-07-13
---
# Photon (iMessage) Setup Guide

## Overview
This document captures the correct procedure for configuring iMessage (via Photon) within Hermes Agent, including common pitfalls and troubleshooting steps.

## Prerequisites
- Hermes Agent installed and running
- Gateway service active
- macOS system with iMessage accounts configured

## Step-by-Step Setup

1. **Enable the Photon platform plugin**
   ```bash
   hermes plugins enable photon-platform
   ```

2. **Restart the gateway service**
   ```bash
   hermes gateway restart
   ```

3. **Launch gateway setup**
   ```bash
   hermes gateway setup
   ```

4. **Select iMessage platform**
   - When presented with the platform menu, choose option **17** (iMessage via Photon)
   - If option 17 is not visible, verify that the `photon-platform` plugin is enabled and the gateway was restarted

## Common Issues & Fixes

### Invalid Command Error
If you encounter:
```
hermes: error: argument command: invalid choice: 'photon'
```
This indicates that `photon` is not a valid subcommand. The correct workflow is to use the **gateway setup** flow and select option **17** (iMessage via Photon) rather than attempting to run a standalone `photon` command.

### Option Not Listed
- Ensure the photon platform plugin is enabled: `hermes plugins list` should show `photon-platform` as enabled
- Restart the gateway after enabling new plugins: `hermes gateway restart`
- If the option still doesn't appear, check gateway logs: `~/.hermes/logs/gateway.log`

### Authentication Failures
- Verify your macOS iMessage login works independently
- Check that your Apple ID has proper permissions for iMessage
- Ensure no network restrictions are blocking the Photon connection

## Reference Materials
- Gateway configuration: `~/.hermes/config.yaml`
- Plugin list: `hermes plugins list`
- Gateway logs: `~/.hermes/logs/gateway.log`
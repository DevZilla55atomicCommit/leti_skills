---
title: Outlook.com with M365 Developer Program (No Payment)
name: outlook-m365-dev-program
description: Connect Outlook.com via M365 Developer Program for Hermes Agent
---

When using a personal Outlook.com account with Hermes, you can avoid Azure costs by leveraging the **M365 Developer Program** (free tier). This provides an Azure AD tenant and allows app registration for the Microsoft Graph MCP server.

## Steps
1. **Join the M365 Developer Program** at https://developer.microsoft.com/microsoft-365/dev-program
2. **Switch directories** in the Azure portal to your new tenant (e.g., `yourname.onmicrosoft.com`).
3. **Create an App Registration** → fill in:
   - Name: `Hermes MCP Email`
   - Supported account types: *Accounts in any organizational directory and personal Microsoft accounts*
   - Redirect URI: `http://localhost:3000/callback`
4. **Copy the Application (client) ID**, **Directory (tenant) ID**, and **Client Secret**.
5. **Add API permissions** → Microsoft Graph → Delegated permissions:
   - `Mail.Read`
   - `Mail.Send`
   - `Mail.ReadWrite`
   - `MailboxSettings.Read`
   - `User.Read`
6. **Update `~/.hermes/config.yaml`** with the values under `mcp_servers.ms_graph`.
7. **Restart Hermes** → first run will open a browser for sign‑in and consent.

## Pitfalls
- **Directory switch required** – the portal defaults to the old tenant; you must manually switch to the new one.
- **Client secret value is only shown once** – copy it immediately; you cannot retrieve it later.
- **First MCP run opens a browser** – ensure your environment can display a browser; headless servers need a VNC or X server.

*Note: This reference file can be loaded via `skill_view` to provide step‑by‑step guidance without modifying protected bundled skills.*
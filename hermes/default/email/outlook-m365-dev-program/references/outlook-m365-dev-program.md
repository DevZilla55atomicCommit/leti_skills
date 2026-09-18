This reference file contains the step‑by‑step guide for connecting Outlook.com via the M365 Developer Program. It includes instructions on joining the program, creating an app registration, setting up API permissions, and configuring Hermes Agent.

## Steps Overview
1. Join the M365 Developer Program.
2. Switch directories in Azure portal.
3. Create an App Registration with required URI.
4. Copy client ID, tenant ID, and client secret.
5. Add Microsoft Graph permissions.
6. Update `~/.hermes/config.yaml`.
7. Restart Hermes and complete sign‑in consent.

## Common Pitfalls
- **Directory switch required** – ensure you select the new tenant.
- **Client secret only visible once** – copy it immediately.
- **Browser required for consent** – needed for first MCP run.

*Keep this file in the `references/` directory for easy access when working with Outlook.com integration.*
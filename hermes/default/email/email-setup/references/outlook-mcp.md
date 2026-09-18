## 1. Install MCP server
npm install -g @modelcontextprotocol/server-microsoft-graph

## 2. Register a Microsoft App
- Go to Azure Portal → Azure Active Directory → App registrations
- Create a new registration
- Note the Client ID and Tenant ID

## 3. Add API permissions
- Add Mail.Read Mail.Send Mail.ReadWrite scopes
- Grant admin consent

## 4. Configure MCP server
In `~/.hermes/config.yaml` add:

mcp_servers:
  ms_graph:
    command: npx
    args: [-y, @modelcontextprotocol/server-microsoft-graph]
    env:
      MICROSOFT_CLIENT_ID: 'your-client-id'
      MICROSOFT_TENANT_ID: 'common'
      MICROSOFT_SCOPES: Mail.Read Mail.Send Mail.ReadWrite

## 5. Use MCP tools
- mcp_ms_graph_list_folders
- mcp_ms_graph_read_email <message-id>
- mcp_ms_graph_send_email ...

## Troubleshooting
- AUTHENTICATE failed indicates you need a work/school account or proper OAuth flow
- Personal accounts require forwarding or OAuth2
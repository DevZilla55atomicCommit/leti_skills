# ChatGPT (Codex) Application Settings Location

- **App Identity**: The desktop client shown as "ChatGPT" is actually OpenAI's **Codex** app (bundle ID `com.openai.codex`).

- **Sandbox Container**:  
  - Path: `~/Library/Containers/com.openai.codex/`  

- **Preferences File**:  
  - Location: `~/Library/Application Support/Codex/Default/Preferences`  
  - Content: JSON configuration covering account state, extensions, autofill, and UI preferences.

- **Secure Preferences**:  
  - Location: `~/Library/Application Support/Codex/Default/Secure Preferences`  
  - Stores sensitive data (auth tokens, cookies).

- **Account Data**:  
  - Location: `~/Library/Application Support/Codex/Default/Account Web Data`  

- **Quick Access**:  
  - Direct open with `open -a "OpenAI Codex"` or via Finder at the above paths.  

- **Diagnostic Tip**:  
  - Use `read_file` with `offset`/`limit` for large JSON files; verify file existence with `ls -la`.
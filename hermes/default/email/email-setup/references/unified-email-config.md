# Unified Email Configuration for Himalaya CLI

This reference covers setting up multiple email providers (Gmail, Outlook/iCloud, generic IMAP) with proper folder alias mapping and app password handling.

## Gmail Setup
- **Email**: your-email@gmail.com  
- **App Password**: 16-character password from Google Account → Security → App Passwords  
- **IMAP Settings**:  
  - Host: imap.gmail.com  
  - Port: 993  
  - TLS Encryption  
- **SMTP Settings**:  
  - Host: smtp.gmail.com  
  - Port: 587  
  - StartTLS Encryption  
- **Folder Aliases**:  
  - inbox = "INBOX"  
  - sent = "[Gmail]/Sent Mail"  
  - drafts = "[Gmail]/Drafts"  
  - trash = "[Gmail]/Trash"

## Outlook/Office 365 Setup
- **Email**: your-email@outlook.com  
- **App Password**: Create via Security → App passwords  
- **IMAP Settings**:  
  - Host: outlook.office365.com  
  - Port: 993  
  - TLS Encryption  
- **SMTP Settings**:  
  - Host: smtp.office365.com  
  - Port: 587  
  - StartTLS Encryption  
- **Folder Aliases**:  
  - inbox = "Inbox"  
  - sent = "Sent Items"  
  - drafts = "Drafts"  
  - trash = "Deleted Items"

## iCloud Setup
- **Email**: your-email@icloud.com  
- **App Password**: Generate via appleid.apple.com → Security → App-Specific Passwords  
- **IMAP Settings**:  
  - Host: imap.mail.me.com  
  - Port: 993  
  - TLS Encryption  
- **SMTP Settings**:  
  - Host: smtp.mail.me.com  
  - Port: 587  
  - StartTLS Encryption  
- **Folder Aliases**:  
  - inbox = "INBOX"  
  - sent = "Sent"  
  - drafts = "Drafts"  
  - trash = "Trash"

## Security Notes
- Never store raw passwords in config files. Use `security find-generic-password` command on macOS or a password manager like `pass`.  
- Ensure each provider's "App Password" is used instead of account password.  
- Verify folder mapping matches your provider's actual folder names to avoid save failures.

## Hermes Integration Tips
- Use `--output json` for programmatic parsing.  
- For sending non-interactive emails, pipe via `cat << EOF | himalaya template send`.  
- When moving/copying messages between folders across providers, verify alias mappings.
# Email Preferences

- **Draft‑first, send‑never** – always iterate on drafts collaboratively before sending.
- **Concise, direct answers** – avoid verbose tables or exploratory explanations unless explicitly requested.
- **Newsletter summaries** – provide a brief bullet list of key topics.
- **Actionable steps** – prioritize clear next actions over procedural fluff.
- **Email checks always include junk/spam** – every inbox check covers Gmail `[Gmail]/Spam` (via himalaya) plus Exchange `Junk Email` (via Apple Mail). Flag obvious phishing/scam (forged dates, yandex/ru senders, Medicare-kit lures) explicitly; offer to delete confirmed-malicious items.
- **User‑corrected style** – keep answers short, avoid verbose formatting, and respect explicit ‘stop doing X’ feedback.
- **ACH/form emails** – strip form field details from body; keep only: sender, purpose, dates, and next action. Attach the form separately.

These preferences guide all email‑related interactions.

---

# AppleScript Pattern: Create Draft with Attachment (Exchange/Outlook)

```applescript
tell application "Mail"
    set newMessage to make new outgoing message with properties {
        subject:"ACH Recurring Payment Authorization Form - Signed and Completed (Falupengh Akaula)",
        content:"Dear [Recipient Name],

Please find attached the completed and signed ACH Recurring Payment Authorization Form for Konark LLC.

The form has been fully executed with signature dated August 28, 2026. This authorization allows for automatic monthly ACH debits beginning September 1, 2026, as outlined in the agreement.

Please confirm receipt and let me know if any additional documentation is required.

Best regards,
Alfred Kamisese
akaula84@gmail.com
408-598-1612",
        visible:true
    }
    
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"[Recipient Email Address]"}
        make new attachment with properties {file name:"/Users/alfredkamisese/Downloads/AHC Form_Aug_31st.jpeg"} at after the last paragraph
    end tell
    
    save newMessage in mailbox "Drafts" of account "Exchange"
end tell
```

**Key points:**
- Use `visible:true` to keep draft window accessible
- `make new to recipient` sets the To field
- `make new attachment with properties {file name:"/absolute/path"} at after the last paragraph` attaches file
- `save newMessage in mailbox "Drafts" of account "Exchange"` puts it in Exchange Drafts folder
- Works for Outlook/Exchange accounts configured in Apple Mail
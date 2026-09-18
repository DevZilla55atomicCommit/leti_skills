# Apple Mail Attachment Handling (Verified 2026-08-19)

## Working Pattern for Multiple Attachments
```applescript
set newMsg to make new outgoing message with properties {subject:"...", visible:true}
tell newMsg
    make new to recipient at end of to recipients with properties {address:"recipient@example.com"}
    set content to "..."
    -- Add attachments ONE AT A TIME with save between each
    make new attachment with properties {file name:"/path/to/file1.pdf"} at after the last paragraph
    save
    delay 1
    make new attachment with properties {file name:"/path/to/file2.pdf"} at after the last paragraph
    save
    delay 1
    make new attachment with properties {file name:"/path/to/file3.pdf"} at after the last paragraph
    save
    -- send or save as draft
end tell
```

## Critical Pitfalls
1. **Multiple attachments in one script block fail silently** — only 2 of 3 attach. Sequential with `save` between each works.
2. **Moving between mailboxes fails** (`-10024`) — `move newMsg to mailbox "[Gmail]/Drafts"` doesn't work. Create in correct account or accept default account's Drafts.
3. **Default account sends** — `make new outgoing message` uses first account in list. Set `sender` property explicitly or create in account context.
4. **Repeated runs create duplicate compose windows** — always delete existing drafts/messages first.
5. **File permissions matter** — `chmod 644` PDFs before attaching.

## Account Context
| Account | Default Drafts Mailbox | Notes |
|---------|-------------------|-------|
| Exchange | "Drafts" | Default account on this system |
| Google/Gmail | "[Gmail]/Drafts" | Moving to this fails (-10024) |
| iCloud | "Drafts" | Untested |

## Search/Delete Drafts Across All Accounts
```applescript
tell application "Mail"
    set allAccounts to every account
    repeat with acct in allAccounts
        try
            set theMailboxes to every mailbox of acct
            repeat with mb in theMailboxes
                try
                    set recentMsgs to (every message of mb whose subject contains "SearchTerm")
                    repeat with msg in recentMsgs
                        delete msg
                    end repeat
                end try
            end repeat
        end try
    end repeat
end tell
```
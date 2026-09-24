tell application "Mail"
    set unreadCount to 0
    repeat with account in (accounts)
        repeat with mailbox in (mailboxes of account)
            if name of mailbox is "Inbox" then
                set unreadCount to count of messages of mailbox whose content is not read of mailbox
                exit repeat
            end if
        end repeat
    end repeat
    return unreadCount
end tell
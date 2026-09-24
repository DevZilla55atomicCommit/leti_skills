(* check_unread.applescript - Fetch unread email subjects from all Mail accounts *)
tell application "Mail"
    repeat with acct in every mail account
        set acctName to name of acct
        set acctType to class of acct
        try
            set unreadMessages to every message of mailbox "Inbox" of acct whose read status is false
            if (count of unreadMessages) > 0 then
                repeat with msg in unreadMessages
                    set subjectText to subject of msg
                    set senderText to sender of msg
                    say "Unread: " & subjectText & " from " & senderText
                end repeat
            end if
        end try
    end repeat
end tell
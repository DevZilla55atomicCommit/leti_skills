(* Robustly get unread messages across all accounts, handling varied inbox names *)

set unreadMessages to {}
tell application "Mail"
    repeat with acct in (every account)
        set acctName to name of acct
        set mailboxNames to name of every mailbox of acct
        repeat with mbName in mailboxNames
            if mbName is equal to "Inbox" or mbName is equal to "INBOX" then
                try
                    set msgs to (every message of mailbox mbName of acct whose read status is false)
                    repeat with m in msgs
                        set end of unreadMessages to {account: acctName, mailbox: mbName, subject: subject of m, sender: sender of m, date: date received of m, id: id of m}
                    end repeat
                end try
            end repeat
        end repeat
    end repeat
    return unreadMessages
end tell
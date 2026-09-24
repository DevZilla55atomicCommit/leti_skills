---
name: multi-account-best-practices
description: Best practices for configuring and troubleshooting multiple email accounts with Himalaya
category: email
---

# Multi-Account Setup & Troubleshooting

## Configuring Multiple Accounts

- Use `himalaya account list` to see configured account names.
- Address names may differ from display names (e.g., "gmail" appears as "Google").
- Specify the exact account name with `--account <NAME>` on commands like `envelope list`, `message read`, etc.
- Example: `himalaya envelope list --account gmail --folder INBOX`.

## Handling Authentication Failures

- Errors like `cannot find configuration for account <NAME>` indicate the named account does not exist in the config.
- Verify the account name from `himalaya account list` and use the exact string.
- For Gmail, the account may be configured as `gmail` but appears as `Google` in some listings; use the configured identifier.

## Alias Syntax Changes (v1.2.0+)

- Folder alias definitions now live under `[accounts.<NAME>.folder.aliases]` (plural `aliases`).
- Using the singular `alias` form is ignored; always use the plural key.
- This affects `sent`, `drafts`, `trash` aliases; ensure they are defined under the correct TOML section.

## Debugging Tips

- Enable debug logs: `RUST_LOG=debug himalaya envelope list`.
- Use `--output json` for structured output to parse programmatically.
- Capture full error messages; search logs for `AUTHENTICATE failed` or `cannot find configuration`.

## Common Pitfalls

- **Pitfall**: Using wrong case or extra spaces in account name.
  **Fix**: Copy-paste the name from `himalaya account list` output.
- **Pitfall**: Assuming account name matches email address.
  **Fix**: Account names are logical labels; they can be anything you set in the config.
- **Pitfall**: Forgetting to set `default = true` if you want to omit `--account`.
  **Fix**: Either set `default = true` in config or always pass `--account`.

## Recommended Workflow

1. List accounts: `himalaya account list`.
2. Identify the correct identifier for the account you need.
3. Use that identifier with `--account` on any command that needs to target a specific account.
4. For commands that default to an account (e.g., envelope list), ensure the desired account is set as default or explicitly specify `--account`.
5. When reading messages, include `--account` to avoid reading from the wrong mailbox.

---
By following these steps, you can reliably manage multiple email accounts with Himalaya and avoid common configuration errors.
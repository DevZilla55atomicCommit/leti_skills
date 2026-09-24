# macOS Application Settings Location Patterns

## Standard App Bundle
- **Location**: `/Applications/<App>.app/Contents/`
- **Key files**: `Info.plist`, `Resources/`, `PlugIns/`

## Sandboxed App Container
- **Root**: `~/Library/Containers/<bundle.id>/`
  - Subpaths of interest:
    - `Data/`
    - `Library/Application Support/<vendor>/`
    - `Library/Containers/<bundle.id>/Data/Library/Application Support/`

## Application Support Directory
- **Root**: `~/Library/Application Support/`
- **Typical vendor subfolders**:
  - `~/Library/Application Support/<Vendor>/`
  - `~/Library/Application Support/<Vendor>/Default/`
  - `~/Library/Application Support/<Vendor>/Secure Preferences/`

## Preference Files
- **Naming patterns**: `Preferences`, `Default/`, `Secure Preferences`
- **Formats**: JSON, plist, YAML
- **Reading**: Use `read_file` with `offset`/`limit` for large files.

## Concrete Example: OpenAI Codex
- **Preferences file**: `~/Library/Application Support/Codex/Default/Preferences`
- **Secure preferences**: `~/Library/Application Support/Codex/Default/Secure Preferences`
- **Account data**: `~/Library/Application Support/Codex/Default/Account Web Data`
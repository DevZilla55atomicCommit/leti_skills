# Instagram Saved Collections Export — JSON Structure

## Top-Level
```json
[
  {
    "timestamp": 1775842668,           // Collection creation time (Unix)
    "media": [],                        // Empty array (legacy?)
    "label_values": [...],              // Collection metadata + items
    "fbid": "123456789"                 // Facebook ID
  }
]
```

## label_values Array
Each collection has 5 `label_values` entries (indices 0-4):

| Index | Label | Purpose |
|-------|-------|---------|
| 0 | `Name` | Collection name (e.g., "Color grading") |
| 1 | `Type` | Always "Default" |
| 2 | `Privacy` | Always "Private" |
| 3 | `Update time` | Unix timestamp of last modification |
| 4 | **Media** | Container for all saved items |

### Media Container (index 4)
```json
{
  "dict": [                           // Array of media items (reels/posts)
    {
      "dict": [                       // Each item has 6 sub-elements
        {"label": "URL", "value": "https://www.instagram.com/reel/ABC123/", "href": "..."},
        {"label": "Caption", "value": "Caption text..."},
        {"label": "Title", "value": ""},
        {"dict": [...], "title": "Hashtags"},
        {"dict": [...], "title": "Owner"},
        {"dict": [...], "title": "Brand partner"}
      ],
      "title": ""                     // Empty string
    }
  ],
  "title": "Media"
}
```

## Media Item Sub-Elements (6 elements in `item.dict`)

| Index | Title | Structure |
|-------|-------|-----------|
| 0 | *(none)* | `{"label": "URL", "value": "...", "href": "..."}` |
| 1 | *(none)* | `{"label": "Caption", "value": "..."}` |
| 2 | *(none)* | `{"label": "Title", "value": ""}` |
| 3 | **Hashtags** | `{"dict": [{"dict": [{"label": "Name", "value": "hashtag1"}]}, {"dict": [{"label": "Name", "value": "hashtag2"}]}], "title": "Hashtags"}` |
| 4 | **Owner** | `{"dict": [{"dict": [{"label": "URL", "value": "..."}, {"label": "Name", "value": "Creator Name"}, {"label": "Username", "value": "handle"}]}], "title": "Owner"}` |
| 5 | **Brand partner** | `{"dict": [{"dict": [{"label": "Name", "value": "Brand Name"}]}], "title": "Brand partner"}` |

## Key Parsing Notes

1. **Hashtags**: The actual tag is in `label` OR `value` field of the innermost dict (both work, `value` is more reliable)
2. **Owner**: Name and Username are separate entries in the innermost `dict` array
3. **Brand partner**: Only present if post has paid partnership tag; `dict` array is empty if none
4. **Caption**: Contains Unicode escape sequences (`\u00e2\u0080\u0099` = apostrophe) — decode with `json.loads()` or Python `json.load()` handles automatically
5. **URL format**: Both `value` and `href` fields present; `value` is canonical

## Example Minimal Item
```json
{
  "dict": [
    {"label": "URL", "value": "https://www.instagram.com/reel/ABC123/", "href": "..."},
    {"label": "Caption", "value": "Great color grade tutorial #davinciresolve"},
    {"label": "Title", "value": ""},
    {"dict": [
      {"dict": [{"label": "Name", "value": "davinciresolve"}]}
    ], "title": "Hashtags"},
    {"dict": [
      {"dict": [
        {"label": "URL", "value": "https://www.instagram.com/creator/"},
        {"label": "Name", "value": "Creator Name"},
        {"label": "Username", "value": "creator_handle"}
      ]}
    ], "title": "Owner"},
    {"dict": [], "title": "Brand partner"}
  ],
  "title": ""
}
```
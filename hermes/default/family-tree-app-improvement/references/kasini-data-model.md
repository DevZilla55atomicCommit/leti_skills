# Tongan Genealogy Extension (TGE) Schema

## Core Concepts

### 1. Ha'a (Clan/Lineage)
- **Entity**: `ha_a`
- **Fields**: `id`, `name`, `founding_ancestor`, `fonua_origin`, `description`, `oral_history`
- **Relationships**: Linked to `person.ha_a_id` and `fonua` origin

### 2. Fonua (Village/Land)
- **Entity**: `fonua`
- **Fields**: `id`, `name`, `type` (village|burial|title_land|ancestral_path), `geometry`, `parent_id`, `associated_ha_a[]`, `associated_titles[]`
- **Spatial**: GeoJSON polygon for land boundaries

### 3. Hereditary Title
- **Entity**: `hereditary_title`
- **Fields**: `id`, `name`, `rank`, `estate_id`, `current_holder`, `succession_type`, `succession_order[]`
- **Succession Rules**: Configurable inheritance rules

### 4. Koeuhi (Oral History/Chant)
- **Entity**: `koeuhi`
- **Fields**: `id`, `title`, `performer`, `recorded_at`, `recorded_location`, `audio_url`, `transcript_tongan`, `transcript_english`, `interlinear_json`, `duration`, `occasion`, `generation_depth`

### 5. Person (Extended)
- **Extended Fields**: 
  - `hingoa_fakafonua` (title), `ha_a_id`, `fonua_matu_a`, `generation_number`, 
  - `koeuhi_ids[]`, `burial_place`, `title_succession_history[]`

## Relationships

```mermaid
erDiagram
    PERSON ||--o{ HA'A : "member_of"
    PERSON ||--o{ HEREDITARY_TITLE : "holds_title"
    HA'A ||--o{ FONUA : "originates_from"
    FONUA ||--o{ HEREDITARY_TITLE : "supports_title"
    PERSON ||--o{ KOEHUI : "associated_chants"
    FONUA ||--o{ KOEHUI : "associated_chants"
```

## Validation Rules

1. **Title Succession**: 
   - If `succession_type` = "primogeniture", `succession_order` must be ordered by birth date
   - `current_holder` must be in `succession_order` and match next position

2. **Fonua Geometry**: 
   - Must be valid POLYGON with non-zero area
   - Must contain at least one `associated_ha_a`

3. **Koeuhi Duration**: 
   - Must be > 0 seconds
   - Audio length must match transcript duration (approx)

4. **Person Generations**: 
   - `generation_number` must be positive integer
   - Must be consistent with parent's `generation_number - 1`

## Tongan-Specific Constraints

- All `name` fields must support fakau'a (ʻ) and macron (ā) characters
- `occasion` field limited to: 'Kava', 'Katoanga', 'Fakafofonga', 'Fānau', 'Faitaha'
- `rank` field limited to: 'King', 'Noble', 'Matapule', 'Kao'
- Land names (`fonua.name`) must be unique within their island group
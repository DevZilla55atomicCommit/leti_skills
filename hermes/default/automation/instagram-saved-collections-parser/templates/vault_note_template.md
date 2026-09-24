# Vault Note Template for Collection Import

When importing collections to Obsidian vault, use this frontmatter + structure:

```yaml
---
collection: "{collection_name}"
item_count: {count}
date_range: "{earliest} to {latest}"
top_hashtags: [{hashtags}]
top_creators: [{creators}]
tags: [instagram, saved, {discipline}]
source: instagram-saved-export
parsed: {date}
---
```

## Collection Note Structure

```markdown
# {collection_name}

**Items:** {count} | **Date Range:** {earliest} to {latest}

## Top Hashtags
{hashtag_list}

## Top Creators
{creator_list}

## Items

| # | URL | Caption Preview | Hashtags | Creator |
|---|-----|-----------------|----------|---------|
{rows}
```

## Discipline Mapping

| Collection Pattern | Discipline Folder | Tags |
|--------------------|-------------------|------|
| Color grading, DaVinci, Speed Ramp | `Post-Production/Color_Grading` | color-grading, davinci-resolve |
| Gimbal, Drone, Car Shooting | `Camera_Movement` | camera-movement, gimbal, drone |
| Lightroom, Photoshop, Skin Retouch | `Photography/Photo_Editing` | lightroom, photoshop, retouch |
| Video Effect, Cinematic, Text Effects | `Video_Effects` | vfx, cinematic, text-effects |
| Lighting, Wedding | `Lighting` | lighting, wedding |
| Fitness, Pickleball, Diet | `Personal/Fitness` | fitness, pickleball |
| Business, Marketing | `Business` | business, marketing |
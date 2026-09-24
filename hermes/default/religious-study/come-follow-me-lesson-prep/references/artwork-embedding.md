# Artwork Embedding Guide — Come Follow Me Lesson Prep

## Official Church Lesson Header Images

### Location on churchofjesuschrist.org
Each weekly lesson page has a **header image** at the top, usually:
- First `<img>` tag on the page
- `alt` text describes the artwork (e.g., "Job surrounded by other people")
- High-resolution URL from Church CDN

### Extraction Workflow

#### 1. Navigate to Lesson Page
```bash
# Official lesson URL pattern
https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026/{lesson-slug}?lang=eng
```

#### 2. Extract Image Data
```python
# In browser_exec:
images = Array.from(document.querySelectorAll('img'))
images.forEach((img, i) => console.log(i, img.src, img.alt, img.width, img.height))
```

#### 3. Identify Header Image
- Usually **index 0** or **index 1**
- `alt` text = descriptive (not "study icon", "seminary icon")
- Dimensions typically 512x288 or similar
- URL pattern: `https://www.churchofjesuschrist.org/imgs/{hash}/full/%21500%2C/0/default`

#### 4. Download
```bash
curl -sL -o /Users/alfredkamisese/filename.png "https://www.churchofjesuschrist.org/imgs/{hash}/full/%21500%2C/0/default"
```

#### 5. Embed in HTML
```html
<div style="text-align: center; margin: 20px 0;">
    <img src="filename.png" alt="[alt text from page]" 
         style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
</div>
```

### Image Sources by Type

| Image Type | Where to Find | Typical Use |
|------------|---------------|-------------|
| **Lesson header** | First img on lesson page | Top of study guide |
| **Teaching Children artwork** | Teaching Children section imgs | Kids section |
| **Scripture Helps images** | "Scripture Helps" section | Deep doctrine boxes |
| **BYU Studies artwork** | byustudies.byu.edu page | Podcast/scholar sections |

### Official Church Media Library (Backup)
```
https://www.churchofjesuschrist.org/media/library
```
- Search by scripture reference
- High-res downloads available
- Categories: Gospel Art, Temples, Scripture Figures, etc.

### Gospel Art Book (Alternative)
- Many lesson images correspond to Gospel Art Book numbers
- Search: "Gospel Art Book [figure name]"
- Consistent style across lessons

### File Naming Convention
```bash
# Pattern: {scripture}_{description}.png
job_lesson_header.png
psalms_shepherd_header.png
genesis_fall_header.png
```

### HTML Embedding Best Practices

```html
<!-- Centered, responsive, subtle shadow -->
<div style="text-align: center; margin: 20px 0;">
    <img src="job_lesson_header.png" 
         alt="Job surrounded by other people" 
         style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <p style="font-size: 0.85em; color: #888; margin-top: 8px;">
        Official Come Follow Me lesson artwork — churchofjesuschrist.org
    </p>
</div>
```

### Attribution
Always include caption:
> Official Come Follow Me lesson artwork — churchofjesuschrist.org

### Quality Check
- [ ] Image downloads without redirect/auth issues
- [ ] Dimensions reasonable (not tiny icon, not huge banner)
- [ ] Alt text preserved from source
- [ ] File size < 500KB (compress if needed)
- [ ] Embedded in HTML with relative path
- [ ] Caption with attribution included

### Batch Download Script (Future)
```python
# Could automate: for each week, fetch lesson page → extract first content image → download → name → embed
```
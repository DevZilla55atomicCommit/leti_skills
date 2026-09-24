# Come Follow Me Lesson Study Guide Template

## Structure for Creating Colorful HTML Study Guides

### 1. Header Section
```html
<h1>Come, Follow Me</h1>
<p class="subtitle">"Lesson Title"<br>Scripture References</p>
<p class="subtitle" style="font-size: 1em;">Date Range • Book Year</p>
```

### 2. Story Summary (3 Sentences)
```html
<div class="key-point">
    <strong>1.</strong> [Setup - who, what happened, WHY]
</div>
<div class="key-point">
    <strong>2.</strong> [Conflict - wrong ideas, opposition]
</div>
<div class="key-point">
    <strong>3.</strong> [Resolution - God's answer, transformation]
</div>
```

### 3. Core Message Box
```html
<div class="takeaway-box">
    <h3>The Core Message</h3>
    <p style="font-size: 1.15em; line-height: 1.7;">
        <strong>[One-sentence summary]</strong><br>
        [Practical application sentence]<br>
        <span style="color: #d4a537;">"Key verse quote" (Reference)</span>
    </p>
</div>
```

### 4. Questions & Answers (Repeat for each lesson question)
```html
<div class="question-box">
    <div class="question-text">Q#: "Exact question from manual" (Scripture Ref)</div>
    <div class="answer-text">
        <strong>Simple Answer:</strong> [Plain English answer]<br><br>
        <strong>Key Points:</strong>
        <ul>
            <li>[Bullet points with scripture references]</li>
        </ul>
    </div>
    <span class="resource-tag">📖 Scripture Reference</span>
</div>
```

### 5. Podcast/External Insights Section
```html
<div class="podcast-header">
    <h2>🎧 Insights from [Podcast Name] with [Guest]</h2>
    <p>Episode details</p>
</div>

<div class="podcast-insight">
    <h4>💡 Key Teaching: [Quote/Concept Title]</h4>
    <p><strong>From [source]:</strong></p>
    <div class="comment-quote">
        "[Direct quote from podcast/comment]"
        <div class="author">— [Attribution]</div>
    </div>
    <p><strong>Application:</strong> [How to apply this]</p>
</div>
```

### 6. Children's Teaching Table
```html
<table>
    <thead>
        <tr><th>Topic</th><th>Kid-Level Answer</th><th>Scripture/Resource</th></tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>[Scripture Range] — [Theme]</strong></td>
            <td>"[Simple language a child understands]"</td>
            <td>[References]</td>
        </tr>
    </tbody>
</table>
```

### 7. Cheat Sheet Cards
```html
<div class="cheat-sheet">
    <div class="cheat-card">
        <div class="cheat-question">"Common Question"</div>
        <div class="cheat-answer">[One-sentence answer]</div>
        <div class="cheat-scripture">Reference</div>
    </div>
    <!-- Repeat for 8-12 cards -->
</div>
```

### 8. Homework/Prep Checklist
```html
<div class="takeaway-box" style="margin-top: 30px;">
    <h3>Your Homework (5 Minutes)</h3>
    <ol style="text-align: left; max-width: 400px; margin: 15px auto;">
        <li><strong>[Action 1]</strong></li>
        <li><strong>[Action 2]</strong></li>
        <li><strong>[Action 3]</strong></li>
    </ol>
</div>
```

### CSS Color Palette (Consistent Across Guides)
```css
/* Primary Colors */
--navy: #1a3c5e;
--teal: #2c5f7c;
--blue: #3d7a9e;
--light-blue: #4a8fae;
--gold: #d4a537;
--light-gold: #e8d5b7;
--cream: #fff8e7;
--warm-white: #fef9f0;
--bg-gradient: linear-gradient(135deg, #fdfbf7 0%, #f5f0e8 100%);

/* Section Backgrounds */
.question-box { background: var(--warm-white); border-color: var(--light-gold); }
.podcast-insight { background: linear-gradient(135deg, #f0f7ff 0%, #e8f0fe 100%); }
.key-point { background: #e8f4f8; border-left-color: var(--blue); }
.takeaway-box { background: var(--navy); }
.cheat-card { border-color: var(--gold); }
```

### Printing to PDF
1. Open HTML in Safari/Chrome
2. Press `Cmd+P` (Print)
3. Destination: "Save as PDF"
4. Settings: Letter size, margins default, background graphics ON
5. Save

### File Naming Convention
`[Book]_[LessonTitle]_[DateRange].html`
Example: `Job_YetWillITrust_Him_August10-16.html`
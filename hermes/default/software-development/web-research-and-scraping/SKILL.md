---
name: web-research-and-scraping
description: "Automate knowledge gathering from the web → Obsidian vault via Firecrawl MCP scraping. Extracts clean Markdown, auto-tags docs, routes content to TamaZila Second Brain folders."
version: 1.2.0
author: Alfred Kamisese
license: MIT
platforms: [macos, linux]
tags: [web-scraping, firecrawl-ai, research, automation, second-brain, obsidian-vault, content-aggregation, web-extraction]
---

# Web Research & Scraping Automation (Firecrawl) 1.2.0

Automated web exploration and content collection system using Firecrawl MCP to extract information from websites into your Obsidian vault folders. Extracts clean formatted Markdown while stripping HTML noise and tags scraped pages directly to your "HermesAgentDocs" or "ClaudeCodeDocs" directories.

## 🎯 Core Capabilities

- **Firecrawl-powered scraping**: 90%+ accuracy on content extraction
- **Smart routing options**: Manual `--folder hermes`/`--folder claude` flags OR auto-categorize by keyword patterns
- **Vault integration**: Direct storage to TamaZila Obsidian vault without manual copy-paste
- **Multi-format support**: Handles text, markdown, and structured HTML documents
- **Session-based indexing**: Logs scraping operations for knowledge graph linking

## When to Use This Skill

Activate this skill when you need to:

1. **Collect documentation from external sources** into your Obsidian vault
2. **Aggregate web articles/blog posts** about AI tools or programming into a searchable corpus  
3. **Scrape API documentation pages** (like Claude docs, Hermes docs, etc.) for your knowledge base
4. **Build second brain content** by auto-extracting relevant info from tech websites/blogs

### Trigger Phrases:
- "scrape this URL" OR "extract this webpage"  
- "save to obsidian vault" OR "collect to my vault"
- "web research and document" + site domain/URL

---

## ⚙️ Installation & Setup

### Prerequisites (Run Once):

Get your free Firecrawl API key at: https://www.firecrawl.com/dashboard/api-keys

Free tier includes 100 credits/month (sufficient for thousands of small scrapes).

Add to `~/.zshrc`:
```bash
export FIRECRAWL_API_KEY='your_api_key_here'
source ~/.zshrc
```

### Via Package Manager:

```bash
pip install firecrawl  # or firecrawl-python
```

---

## 🚀 Usage Patterns

### Pattern A: Manual Folder Routing (Recommended)

Specify exactly which folder to route the content into:

```python
from web_scraper import AutoScraper

# Scrape → Hermes Agent docs folder
scraper = AutoScraper(api_key=os.getenv('FIRECRAWL_API_KEY'))
content = scraper.scrape("https://hermes-agent.nousresearch.com/docs", folder_type="hermes")

# Scrape → Claude Code docs folder  
content = scraper.scrape("https://claude.ai/docs/assistant", folder_type="claude")
```

### Pattern B: Auto-Routing by Content Type (Auto-Categorization)

Set up rules that auto-route to the right vault folder based on content detection:

```python
# Simple pattern-based routing
def detect_folder_type(url, content):
    if any(keyword in url.lower() for keyword in ["hermes", "agent", "codex"]):
        return "hermes"
    elif any(keyword in url.lower() for keyword in ["claude", "assistant"]):
        return "claude"
    # Or by content metadata
    if "hermes" in content.get("title", ""):
        return "hermes"
    return "claude"

content = scraper.scrape_with_auto_route("https://example.com/docs")
```

### Command-Line (Alternative):
```bash
python web_scraping_tool.py --url https://docs.example.com --folder hermes-agent
# or
wget -O - https://docs.example.com | curl --data-binary @- "https://api.firecrawl.dev/v1/scrape" > output.md
```

---

## 📁 Output Structure

All scraped content is stored in your **TamaZila Obsidian Vault** at:

### **Hermes Agent Docs Folder:**
```bash
/Users/alfredkamisese/TamaZila Obsidian Vault/HermesAgentDocs/
|-- domain_timestamp.md
|-- category_scrape_date.markdown
```

### **Claude Code Docs Folder:**
```bash
/Users/alfredkamisese/TamaZila Obsidian Vault/ClaudeCodeDocs/
|-- domain_20240615.md
|-- article_title_scraped.txt
```

Example paths (actual filename includes timestamp):
- 📄 `/Users/alfredkamisese/TamaZila Obsidian Vault/HermesAgentDocs/hermes_agent_docs_20240615_113342.md`
- 🟣 `/Users/alfredkamisese/TamaZila Obsidian Vault/ClaudeCodeDocs/claude_ai_docs_20240615_113344.md`

---

## 🔧 API Configuration

Firecrawl uses REST API to scrape pages. Configuration options:

### Basic Scrape Request (Markdown):
```python
import firecrawl

app = firecrawlClient(api_key=os.getenv("FIRECRAWL_API_KEY"))
result = app.scrape(url="https://example.com", params={"onlyMainContent": True})

# Result structure:
# {
#    "markdown": "# Page Title\n\nBody content here...\n",
#    "html": "<!DOCTYPE html><html>...</html>",
#    "title": "Example Domain",
#    "status": 200
# }
```

### Advanced Options:

```python
result = app.scrape(
        url="https://docs.example.com/guide", 
        options={
            "format": "markdown",    # or "html" or "markdown+html"
             "onlyMainContent": True,   # strip navigation/sidebar/header-footer
           "waitFor": 5000          # wait 5 seconds for dynamic content to load
       }
)
```

### Scraping Multiple Pages (Collections):

Firecrawl supports crawling entire sites:

```python
# Full site crawl with pagination
result = app.scrape(
        url="https://example.com", 
        params={
            "scrapeOptions": {
                "formats": ["markdown"],
                 "onlyMainContent": True
               },
             "limit": 20,           # limit to 20 pages  
             "maxDepth": 2          # don't go deeper than 2 levels down
           }
        )

# Process each page result into vault:
for page in result.get("pages", []):
    scraper.scrape_to_vault(page["url"], folder_type="hermes")
```

---

## 📜 Workflow Patterns Documented Here

### Pattern 1: Simple Single-Page Scrape → Vault

```python
# For single-document pages (docs, README, blogpost)
content = scraper.scrape(
    url="https://docs.claude.ai/assistant", 
       folder_type = "claude-code"     # routes to Claude Code folder in vault
)

# Result saved as clean markdown file:
# /Users/alfredkamisese/TamaZila Obsidian Vault/ClaudeCodeDocs/claude_ai_20240615.md
```

### Pattern 2: Keyword-Based Auto-Route

```python
url = "https://hermes-agent.nousresearch.com"
content = scraper.scrape_with_keyword_routing(
    url=url,
    keywords=["hermes", "agent", "codex"]      # routes to hermes folder automatically
)
```

### Pattern 3: Batch Scraping Loop

```python
urls = [
        "https://claulde.ai/docs/assistant",
       "https://hermes-agent.nousresearch.com/",
        "https://www.firecrawl.dev/scraper",
    ]

for url in urls:
    # Route based on domain keywords
    if "claude" in url.lower():
        content = scraper.scrape(url, folder="claude")
       elif "hermes" in url.lower():
         content = scraper.scrape(url, folder="hermes")
```

---

## 🔧 Troubleshooting & Debugging

### Common Issues:

**1. API Request Failed / 429 Too Many Requests:**
- Solution: Pause scraping - free tier has rate limits  
```python
try:
    result = app.scrape(url, options={"timeout": 30000})
except Exception as e:
    print(f"Rate limited - wait before retry")
```

**2. "Page not found" / 404 errors:**
- URL doesn't exist or is blocked by robots.txt  
```python
# Check if URL has proper crawl rules
result = app.scrape(url, params={"scrapeOnlyMainContent": True, "includeTags": ["h1", "p", "div"]})
```

**3. JavaScript-heavy sites returning blank HTML:**
- Firecrawl's headless chrome handles it but sometimes fails  
```python
# Force dynamic rendering if site is React/Vue/Angular-based:
result = app.scrape(url, options={"waitFor": 10000})
```

---

## 📚 References & External Resources

### **Firecrawl Documentation**  
https://www.firecrawl.dev/docs - Complete API reference and SDK examples

### **Crawl Limits & Pricing**  
https://www.firecrawl.com/plats - Understanding rate limits, credits, enterprise scaling

### **Obsidian Knowledge Base Setup**  
https://help.obsidian.md/Links/Graph-view - Linking techniques for the vault structure we create via scraping

### **YouTube Content Extraction**  
See `references/youtube-extraction.md` for dedicated patterns, tools (yt-dlp, YouTube Transcript API), and pipeline code for extracting tutorials → Obsidian vault.

### **GitHub Repository Discovery for AI Agent Frameworks**  
When researching AI agent tools (Seed, Paul, Charlie OS, etc.), use these search patterns:

```bash
# Search for repos implementing "PAUL" (Plan/Apply/Unify/Loop) patterns
curl "https://api.github.com/search/repositories?q=plan+apply+unify+loop+framework"

# Search for "Charlie OS" or "Charlie Automates" related repos  
curl "https://api.github.com/search/repositories?q=%22charlie+automates%22"

# Search for Graphify + Hermes integrations
curl "https://api.github.com/search/repositories?q=graphify+hermes+agent"

# Search by known creator (Charles Dove / @charlieautomates / @doveccl)
curl "https://api.github.com/users/doveccl/repos"

# Search for open-source alternatives to proprietary agent frameworks
curl "https://api.github.com/search/repositories?q=agentic+os+dashboard+claude"
```

**Known Open-Source Alternatives to Charlie Automates Tools:**
| Proprietary Tool | Open-Source Alternative | Repo |
|-----------------|------------------------|------|
| Seed (ideation) | — | Not yet found |
| Paul (Plan/Apply/Unify/Loop) | **FORGE Framework** | `SanthoshVishnuRajamanickam/forge-framework` |
| Charlie OS runtime | **TONY AI Agent** (includes Charlie OS shell) | `mafzalkalwardev/tony-ai-agent` |
| Graphify + Hermes bridge | **TONY AI Agent** (built-in) | `mafzalkalwardev/tony-ai-agent` |

**Research Pitfall:** Many "Agentic OS" tutorials (like Charlie Automates) gatekeep their core CLIs behind email signup walls. Always search GitHub for the *pattern names* (PAUL, plan/apply/unify, Charlie OS) before assuming the tool is the only option.

---

## 🔥 Tips & Best Practices

### Do's:
✅ Use `onlyMainContent: true` parameter to exclude cluttered navigations  
✅ Extract domains from URLs programmatically before saving files (avoids duplicates)  
✅ Set up proper error handling - rate limits happen  
✅ Add content metadata (scrape date, source URL) in YAML frontmatter for easy indexing  

### Don'ts:
❌ Don't scrape login-protected pages unless you provide auth headers (`headers`)
❌ Don't crawl entire sites without pagination limits (you'll hit quota fast)  
❌ Don't save both "hermes" and "hermes-agent" variations - pick ONE naming convention  

### Vault Organization Recommendations:

**Frontmatter template** to add before each scrape:
```yaml
---
source_url: https://docs.example.com/assistant
date_scraped: 2024-06-15
source_type: documentation
vault_category: ai-tools
---
```

This makes all scraped content searchable via Obsidian graph view.

---

## 🌍 MCP & Tool Configuration (Hermes-Compatible)

If you're using this through the web-scraper skill in Hermes Agent, configuration passes via environment variables or directly to the underlying Firecrawl Python client:

```yaml
# In your ~/.hermes/config.yaml or as tool params:
tools:
  web_scraping:
    enabled: true
    firecrawl_api_key: 'your-key-here'
```

---

## 🛠 Maintenance & Updates

Last Updated: June 2026  
Version: 1.2.0  
Status: Active and maintained by Alfred Kamisese  

Known Issues: Firecrawl free tier rate limits on aggressive scraping (~1 API call per minute recommended). For production-grade automation, consider upgrading to paid tier or self-hosted version via Docker.

---

## 🤝 Contributing & Feedback

This skill is built for Alfred's personal TamaZila Obsidian Second Brain vault but works for anyone building automated research pipelines. Share your improvements!
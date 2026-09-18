# Profile Templates — Ready-to-Use Configurations

Reference for `hermes-multi-agent-orchestration` skill.

---

## Forex Analyst Profile

```bash
hermes profile create forex-analyst --description "Forex technical analysis, macro indicators, automated alerts"
```

**Config overrides:**
```yaml
model:
  default: "openai/gpt-5.5"
  provider: "openrouter"
toolsets:
  - web
  - terminal
  - file
  - skills
  - memory
  - cronjob
auxiliary:
  web_extract:
    provider: "openrouter"
    model: "anthropic/claude-sonnet-4.6"
```

**Suggested skills to install:**
```bash
hermes -p forex-analyst skills install market-research
hermes -p forex-analyst skills install technical-analysis
hermes -p forex-analyst skills install risk-management
```

**Cron jobs:**
```bash
hermes -p forex-analyst cron add daily-digest "0 9 * * *" \
  --prompt "Summarize forex news, technical setups for EUR/USD, GBP/USD, USD/JPY, AUD/USD. Include macro calendar events and key levels."

hermes -p forex-analyst cron add session-open "0 17 * * 1-5" \
  --prompt "NY session open analysis: liquidity, spreads, news catalyst check for major pairs."
```

---

## Colorist Profile (DaVinci Resolve)

```bash
hermes profile create colorist --clone --description "DaVinci Resolve grading, node workflows, LUT design"
```

**Config overrides:**
```yaml
mcp_servers:
  davinci-resolve:
    enabled: true
toolsets:
  - web
  - terminal
  - file
  - skills
  - memory
```

**Suggested skills to install:**
```bash
hermes -p colorist skills install davinci-resolve-color-grading
hermes -p colorist skills install davinci-workflows
hermes -p colorist skills install color-science-guide
hermes -p colorist skills install lut-design
```

**Cron jobs:**
```bash
hermes -p colorist cron add weekly-technique "0 10 * * 1" \
  --prompt "Extract one DaVinci Resolve technique from recent Instagram reels and document as a reusable skill." \
  --skills davinci-resolve,instagram-reels-pipeline
```

---

## Web Developer Profile

```bash
hermes profile create web-dev --description "Next.js, React, TypeScript, Tailwind, Framer Motion"
```

**Config overrides:**
```yaml
model:
  default: "anthropic/claude-sonnet-4.6"
  provider: "openrouter"
toolsets:
  - web
  - terminal
  - file
  - code_execution
  - coding
  - skills
  - memory
```

**Suggested skills to install:**
```bash
hermes -p web-dev skills install nextjs-patterns
hermes -p web-dev skills install react-patterns
hermes -p web-dev skills install typescript-patterns
hermes -p web-dev skills install tailwind-patterns
hermes -p web-dev skills install framer-motion-patterns
```

---

## Creative Director Profile

```bash
hermes profile create creative-dir --clone --description "Storyboards, shot lists, camera theory, lighting design"
```

**Config overrides:**
```yaml
toolsets:
  - web
  - terminal
  - file
  - skills
  - memory
  - vision
  - image_gen
```

**Suggested skills to install:**
```bash
hermes -p creative-dir skills install videography
hermes -p creative-dir skills install photography
hermes -p creative-dir skills install storyboard-generation
hermes -p creative-dir skills install lighting-design
hermes -p creative-dir skills install camera-theory
```

---

## Researcher Profile

```bash
hermes profile create researcher --description "Deep research, paper analysis, market data"
```

**Config overrides:**
```yaml
model:
  default: "nvidia/nemotron-3-ultra-550b-a55b"
  provider: "nvidia"
toolsets:
  - web
  - terminal
  - file
  - skills
  - memory
  - browser
```

**Suggested skills to install:**
```bash
hermes -p researcher skills install deep-research
hermes -p researcher skills install arxiv-search
hermes -p researcher skills install paper-analysis
hermes -p researcher skills install market-data
```

---

## System Monitor Profile

```bash
hermes profile create system-monitor --description "System health, resource monitoring, alerting"
```

**Config overrides:**
```yaml
toolsets:
  - terminal
  - file
  - skills
  - memory
```

**No-agent cron script (`health_check.sh`):**
```bash
#!/bin/bash
# Save to ~/.hermes/scripts/health_check.sh
df -h / | tail -1
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
ollama ps
curl -s http://localhost:11434/api/tags | jq '.models[].name'
```

```bash
hermes -p system-monitor cron add health-check "0 * * * *" \
  --script "health_check.sh" \
  --no-agent true
```
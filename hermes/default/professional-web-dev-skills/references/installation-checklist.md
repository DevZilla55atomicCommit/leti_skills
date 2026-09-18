# Installation Checklist (Quick Reference)

## Prerequisites
1. **Python 3.x**: Install via `brew install python`
2. **Git**: Ensure `git` is installed and configured
3. **Claude Code**: Install and authenticate via `claude code login`

## Installation Steps
1. **Verify Claude Code Auth**
   ```bash
   claude code auth status
   ```
2. **Install Core Skills**
   ```bash
   claude code install https://github.com/addyosmani/agent-skills/tree/main/frontend-ui-engineering
   claude code install https://github.com/addyosmani/agent-skills/tree/main/spec-driven-development
   claude code install https://github.com/addyosmani/agent-skills/tree/main/test-driven-development
   claude code install https://github.com/addyosmani/agent-skills/tree/main/incremental-implementation
   claude code install https://github.com/addyosmani/agent-skills/tree/main/code-review-and-quality
   ```
3. **Install Design Skills**
   ```bash
   claude code install https://github.com/freshtechbro/claudedesignskills
   ```
4. **Install 3D Skills**
   ```bash
   claude code install https://github.com/freshtechbro/claudedesignskills/plugins/bundles/core-3d-animation/skills/threejs-webgl/SKILL.md
   claude code install https://github.com/freshtechbro/claudedesignskills/plugins/bundles/core-3d-animation/skills/react-three-fiber/SKILL.md
   claude code install https://github.com/freshtechbro/claudedesignskills/plugins/bundles/extended-3d-scroll/skills/lightweight-3d-effects/SKILL.md
   ```
5. **Verify Installations**
   ```bash
   claude code list
   ```

## Common Gotchas
- **Timeout on New Repos**: Run `git trust` in any new cloned repo to avoid HMAC timeout
- **Python Path Issues**: Some scripts may require `python3` explicitly
- **Model URL Conflicts**: When using NVIDIA API, ensure `base_url` is set to `https://integrate.api.nvidia.com/v1` (not local Ollama)
- **Trusted Workspace**: Always `git trust` new repos to prevent HMAC credential timeouts

## Verification Checklist
- ✅ All skills appear in `claude code list`
- ✅ No timeout errors during install
- ✅ Skills appear in `~/.claude/skills/` directory
- ✅ Reference files are accessible via `skill_view`
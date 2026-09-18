# Pipeline Lifecycle Reference

Cross-reference to the lifecycle skill: `instagram-davinci-pipeline-lifecycle`

## Key Integration Points

| Aspect | Covered By |
|--------|------------|
| File lifecycle & storage | `instagram-davinci-pipeline-lifecycle` |
| GIF/MP4 regeneration | `instagram-davinci-pipeline-lifecycle` |
| Rate limits & constraints | `instagram-davinci-pipeline-lifecycle` |
| Vision analysis protocol | `instagram-davinci-learning-pipeline` (this skill) |
| Skill/vault generation | `instagram-davinci-learning-pipeline` (this skill) |

## When to Use Each Skill

| Task | Use Skill |
|------|-----------|
| Process new Instagram URLs | `instagram-davinci-learning-pipeline` |
| Regenerate missing GIFs/MP4s | `instagram-davinci-pipeline-lifecycle` |
| Understand rate limits | `instagram-davinci-pipeline-lifecycle` |
| Debug storage issues | `instagram-davinci-pipeline-lifecycle` |
| Classify/route content | `instagram-davinci-learning-pipeline` |
| Generate vault notes/skills | `instagram-davinci-learning-pipeline` |
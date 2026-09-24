# Voice Playback Store — Desktop App Reference

Source: `apps/desktop/src/store/voice-playback.ts`

```typescript
import { atom } from 'nanostores'

export type VoicePlaybackSource = 'read-aloud' | 'voice-conversation'
export type VoicePlaybackStatus = 'idle' | 'preparing' | 'speaking'

export interface VoicePlaybackState {
  audioElement: HTMLAudioElement | null
  messageId: string | null
  sequence: number
  source: VoicePlaybackSource | null
  status: VoicePlaybackStatus
}

export const $voicePlayback = atom<VoicePlaybackState>({
  audioElement: null,
  messageId: null,
  sequence: 0,
  source: null,
  status: 'idle'
})

export function setVoicePlaybackState(next: VoicePlaybackState) {
  $voicePlayback.set(next)
}
```

## State Transitions

| Trigger | From | To | Notes |
|---------|------|-----|-------|
| TTS request sent (POST /api/audio/speak) | idle | preparing | Streaming WS not yet connected |
| Streaming WS `start` frame received | preparing | speaking | First audio chunk playing |
| TTS request sent (streaming) | idle | preparing | WS connecting |
| Streaming WS `start` frame | preparing | speaking | Audio playback began |
| Audio `ended` event | speaking | idle | Playback complete |
| `stopVoicePlayback()` called | any | idle | Barge-in / interruption |
| Streaming WS `fallback` frame | preparing | idle | No audio produced, fallback to POST |
| Streaming WS `error`/`close` (no audio yet) | preparing | idle | Fallback path |

## Accessing from Plugin

Plugins share the renderer process with the app, so the store is available on `window`:

```javascript
// In plugin useEffect
const interval = setInterval(() => {
  const pb = window.$voicePlayback?.get?.()
  if (pb) {
    // pb.status === 'idle' | 'preparing' | 'speaking'
    // pb.sequence increments on each new playback
    // pb.source === 'read-aloud' | 'voice-conversation'
  }
}, 100)
```

## Related Files

- `apps/desktop/src/lib/voice-playback.ts` — `playSpeechText()`, `startSpeechStream()`, `stopVoicePlayback()`
- `apps/desktop/src/app/chat/composer/hooks/use-auto-speak-replies.ts` — Auto-speak logic
- `apps/desktop/src/app/chat/composer/hooks/use-voice-conversation.ts` — Voice conversation loop
# Free video and voice tools

Free tiers, credits, quotas, regional availability, and commercial-use terms change. Check the official provider pages before publishing.

## AI script generation
- Groq API: low-latency model API; a free plan is available subject to model-specific limits. Requires an API key.
- Ollama: local models; performance depends on RAM/GPU.

## Voice
- Edge TTS: online neural voices via Python package; availability/terms may change.
- Piper and Kokoro: local TTS options; model setup, languages and hardware vary.
- Audacity: free audio cleanup.
- ElevenLabs: free tier quota and usage terms change.

## Video and editing
- FFmpeg: open-source video/audio rendering, subtitles and montage assembly.
- MoviePy: Python editing wrapper.
- CapCut, Canva, VN, Clipchamp: editing, templates and captions; free features vary.
- Pexels / Pixabay: stock clips and images; verify license, API and use restrictions.
- ComfyUI: local image/video workflows; hardware/model requirements can be significant.
- Hugging Face: models and demos; hosted spaces may sleep or have quotas.

## Baseline automated output
This repository's basic pipeline can produce narration plus stock footage (when a Pexels API key is configured) or a simple background/card montage. It does **not** generate AI video clips by default. Free AI-video credits are inconsistent, so generative video should remain an optional/manual step until a provider's free access is confirmed.

## Workflow
1. Generate an original script and scene descriptions.
2. Create narration audio.
3. Search optional stock footage for each scene.
4. Render a vertical MP4 with captions and audio using FFmpeg.
5. Review manually, check rights and facts, then publish.

No tool is guaranteed to remain free.

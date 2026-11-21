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

## Automated visual modes
- `ai-images`: attempts to generate a separate AI still for each scene through Hugging Face Inference. It animates those stills with FFmpeg zoom/pan motion (Ken Burns-style); this is **not true AI-generated video**. Requires the optional `HF_TOKEN` secret and provider/model availability; costs or credits may apply.
- `stock`: searches and uses Pexels clips if `PEXELS_API_KEY` is set.
- `cards`: uses simple background clips as the last fallback.

In `ai-images` mode, generation failures fall back to stock clips when Pexels is configured, then to cards. The pipeline still requires human review. Free AI-video credits are inconsistent, so true generated motion video remains optional/manual.

## Workflow
1. Generate an original script and scene descriptions.
2. Create narration audio.
3. Search optional stock footage for each scene.
4. Render a vertical MP4 with captions and audio using FFmpeg.
5. Review manually, check rights and facts, then publish.

No tool is guaranteed to remain free.

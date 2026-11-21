# Social Media AI Team

A manually triggered, low-cost AI content workflow for research, strategy, creative production and quality review.

## What this repository is intended to do

1. Research current trends and ideas with source links and dates.
2. Let a Social Media Manager role select ideas based on channel fit, originality, shareability, retention potential and production effort.
3. Let a Creative Developer turn selected ideas into scripts, shot lists, AI video prompts, voice-over, captions and editing instructions.
4. Let a Reviewer independently score the output, flag risks and request one revision.
5. Save a daily report and a history of ideas so the team avoids repeating itself.

## Channels

- **Dil Se Scroll (primary):** relatable Hindi/Hinglish, comedy, POV, friendship, love, middle-class life.
- **CodersAdda:** coding, AI tools, software testing, IT careers and interview preparation.
- **Divine Path:** devotional, spirituality, wisdom and life lessons.

Channels should be configurable. Do not produce content for future channels unless they are explicitly activated.


## Free / low-cost production toolkit

See **[docs/FREE_VIDEO_AND_VOICE_TOOLS.md](docs/FREE_VIDEO_AND_VOICE_TOOLS.md)** for options to create videos, generate voiceovers, edit, add captions and assemble content without paying upfront. Free allowances, watermarks, country availability and commercial-use rights change frequently; check each tool's official terms before publishing or monetizing.

## Suggested zero-budget production workflow

1. Generate an idea and script using this team's daily report.
2. Create still images with a free image generator or use your own footage.
3. Try free video generation credits for the key shots; do not assume every tool provides recurring free credits.
4. Create voice-over using a free TTS tool only after checking download and commercial-use terms.
5. Edit and add captions using a free editor such as VN, Clipchamp, Canva or CapCut (availability/features vary by region and plan).
6. Use original or platform-cleared music/sounds. Avoid reusing other creators' videos or voices without permission.
7. Publish separately to Shorts, Reels and Facebook Reels; track retention, shares, saves and follows.

## Daily run

The intended interface is GitHub Actions → **Daily Content Team** → choose channel(s) → Run workflow. The automation/workflow implementation is still being built; this README is not a claim that the workflow is already installed or functional.

## Key operating rules

- Research claims must include links and the date checked.
- Label trend evidence, evergreen ideas, and speculation separately.
- Never invent trending audio status, tool free-tier limits, analytics or account access.
- Reject generic, low-value, derivative or unverified ideas.
- A reviewer should have authority to reject or revise content.
- AI-generated content needs human checks for factual accuracy, visuals, voice rights, platform policy and brand fit.
- Keep outputs original and substantially transformed; avoid raw reposting.

## Report history

Daily reports should be saved under `reports/daily/YYYY-MM-DD/` when the workflow is implemented. Keep a lightweight index of idea IDs, dates, channels and statuses to reduce duplicate concepts.

## Important

This project is a content-planning assistant, not an auto-publishing system. Publishing should remain manual until the user has tested and approved quality and platform compliance.

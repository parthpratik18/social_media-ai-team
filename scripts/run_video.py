import os, json, re, random, subprocess, asyncio, requests
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
CFG=json.loads((ROOT/"config/channels.json").read_text(encoding="utf-8"))
W,H=1080,1920

def run_ffmpeg(args):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",*map(str,args)],check=True)

def safe_name(s):
    return re.sub(r"[^a-zA-Z0-9_-]+","-",s).strip("-")[:50] or "short"

def create_script(channel, topic):
    api=os.getenv("GROQ_API_KEY")
    if not api: raise RuntimeError("Missing GROQ_API_KEY secret. Add it in repo Settings > Secrets and variables > Actions.")
    ch=CFG[channel]
    prompt=f"""Make a unique 25-35 second short video for channel {ch['name']}.
Language: {ch['language']}. Style: {ch['style']}. Topic: {topic or 'pick a strong evergreen topic'}.
Return JSON with title, narration, scenes. scenes must be 4-6 objects each with narration, visual_search, on_screen_text.
Start with an attention-grabbing spoken hook, avoid filler, finish with a natural CTA.
Be truthful. For spirituality never invent scripture or attribute fabricated quotes. Avoid copyright characters, copied scripts or impersonation."""
    resp=requests.post("https://api.groq.com/openai/v1/chat/completions",
      headers={"Authorization":f"Bearer {api}","Content-Type":"application/json"},
      json={"model":os.getenv("GROQ_MODEL","openai/gpt-oss-120b"),"temperature":0.85,
        "response_format":{"type":"json_object"},
        "messages":[{"role":"system","content":"Return valid JSON only."},{"role":"user","content":prompt}]},timeout=90)
    resp.raise_for_status()
    return json.loads(resp.json()["choices"][0]["message"]["content"])

async def make_voice(text, voice, path):
    await edge_tts.Communicate(text,voice).save(str(path))

def pexels_search(query, key):
    if not key:return None
    try:
        r=requests.get("https://api.pexels.com/videos/search",headers={"Authorization":key},
          params={"query":query,"per_page":12,"orientation":"portrait"},timeout=30)
        r.raise_for_status()
        candidates=[]
        for video in r.json().get("videos",[]):
            for f in video.get("video_files",[]):
                if f.get("link") and f.get("width",0)>=480:
                    candidates.append(f)
        if candidates:
            candidates.sort(key=lambda f:(f.get("height",0),f.get("width",0)),reverse=True)
            return candidates[0]["link"]
    except Exception as e: print("Pexels lookup failed; using fallback cards:",e)
    return None

def download(url,path):
    try:
        with requests.get(url,stream=True,timeout=45) as r:
            r.raise_for_status()
            with open(path,"wb") as f:
                for c in r.iter_content(1024*512):
                    if c:f.write(c)
        return path.stat().st_size>20000
    except Exception as e:
        print("Footage download failed:",e)
        return False

def render_card(text,path,duration=5):
    # Scene label is encoded as SRT instead; background card remains text-free to avoid filter escaping.
    run_ffmpeg(["-f","lavfi","-i",f"color=c=0x17243D:s={W}x{H}:d={duration}",
      "-r","25","-pix_fmt","yuv420p","-c:v","libx264","-preset","veryfast","-t",str(duration),path])

def make_srt(scenes,duration):
    def tc(s):
        ms=int(s*1000); h=ms//3600000; m=(ms%3600000)//60000; sec=(ms%60000)//1000; milli=ms%1000
        return f"{h:02}:{m:02}:{sec:02},{milli:03}"
    total=max(1,len(scenes)); span=duration/total
    blocks=[]
    for i,scene in enumerate(scenes):
        text=(scene.get("on_screen_text") or scene.get("narration") or "").strip()
        if not text:continue
        text=text.replace("\n"," ").strip()
        blocks.append(f"{i+1}\n{tc(i*span)} --> {tc((i+1)*span)}\n{text}\n")
    return "\n".join(blocks)

def main():
    channel=os.getenv("CHANNEL","dil-se-scroll")
    topic=os.getenv("TOPIC","").strip()
    mode=os.getenv("VISUAL_MODE","cards")
    if channel not in CFG:raise ValueError(f"Unknown channel {channel}")
    data=create_script(channel,topic)
    scenes=data.get("scenes",[])[:6]
    if len(scenes)<4:raise RuntimeError("AI output needs 4 or more scenes. Re-run the workflow.")
    narration=(data.get("narration") or " ".join(s.get("narration","") for s in scenes)).strip()
    stem=safe_name(channel+"-"+data.get("title","daily-short"))
    base=OUT/stem
    (base.with_suffix(".json")).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    voice=base.with_suffix(".mp3")
    asyncio.run(make_voice(narration,CFG[channel]["voice"],voice))
    clips=[]
    for idx,scene in enumerate(scenes,1):
        clip=OUT/f"{stem}-scene{idx}.mp4"
        source=OUT/f"{stem}-source{idx}.mp4"
        url=pexels_search(scene.get("visual_search") or topic or data.get("title",""),os.getenv("PEXELS_API_KEY")) if mode=="stock" else None
        if url and download(url,source):
            vf=f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
            run_ffmpeg(["-stream_loop","-1","-i",source,"-t","5","-vf",vf,"-r","25","-pix_fmt","yuv420p","-c:v","libx264","-preset","veryfast",clip])
        else:
            render_card(scene.get("on_screen_text",""),clip)
        clips.append(clip)
    concat=OUT/f"{stem}-concat.txt"
    concat.write_text("".join(f"file '{c.resolve()}'\n" for c in clips),encoding="utf-8")
    silent=base.with_suffix(".silent.mp4")
    run_ffmpeg(["-f","concat","-safe","0","-i",concat,"-c","copy",silent])
    duration=len(scenes)*5
    subtitle=base.with_suffix(".srt")
    subtitle.write_text(make_srt(scenes,duration),encoding="utf-8")
    final=base.with_suffix(".mp4")
    srt_path=subtitle.resolve().as_posix().replace(":","\\:")
    vf=f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},subtitles='{srt_path}'"
    try:
        run_ffmpeg(["-i",silent,"-i",voice,"-vf",vf,"-c:v","libx264","-preset","veryfast","-c:a","aac","-shortest",final])
    except subprocess.CalledProcessError:
        print("Subtitle render failed; retrying without burned-in subtitles. SRT will still be included.")
        run_ffmpeg(["-i",silent,"-i",voice,"-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}","-c:v","libx264","-preset","veryfast","-c:a","aac","-shortest",final])
    report={"channel":channel,"topic":topic,"title":data.get("title"),"video":final.name,"script":base.with_suffix(".json").name,"voice":voice.name,"captions":subtitle.name,"visual_mode":mode,"review":"Human review required before posting."}
    (OUT/f"{stem}-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Rendered video:",final)

if __name__=="__main__":main()

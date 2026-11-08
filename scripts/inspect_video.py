#!/usr/bin/env python3
"""Inspect a reference video and export metadata, sampled frames and a contact sheet."""
import argparse, json, os, subprocess, math
from pathlib import Path
import cv2
from PIL import Image, ImageDraw

def probe(path):
    cmd=["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]
    data=json.loads(subprocess.check_output(cmd,text=True))
    v=next((s for s in data.get("streams",[]) if s.get("codec_type")=="video"),{})
    a=next((s for s in data.get("streams",[]) if s.get("codec_type")=="audio"),{})
    def rate(s):
        x=s.get("avg_frame_rate") or s.get("r_frame_rate") or "0/1"
        try:
            n,d=map(int,x.split("/")); return n/d if d else 0
        except Exception: return 0
    return {
        "path":str(path.resolve()),
        "duration_seconds":float(data.get("format",{}).get("duration",0) or 0),
        "format_name":data.get("format",{}).get("format_name"),
        "video":{"codec":v.get("codec_name"),"width":v.get("width"),"height":v.get("height"),
                 "fps":rate(v),"pixel_format":v.get("pix_fmt"),"frame_count":v.get("nb_frames")},
        "audio":{"present":bool(a),"codec":a.get("codec_name"),"sample_rate":a.get("sample_rate"),
                 "channels":a.get("channels"),"duration_seconds":float(a.get("duration",0) or 0) if a.get("duration") else None}
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out-dir",default="reference_inspection")
    ap.add_argument("--samples",type=int,default=9)
    args=ap.parse_args()
    src=Path(args.video); out=Path(args.out_dir); frames=out/"frame_samples"
    frames.mkdir(parents=True,exist_ok=True)
    meta=probe(src); (out/"metadata.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    cap=cv2.VideoCapture(str(src))
    fps=cap.get(cv2.CAP_PROP_FPS) or 30
    count=cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    duration=count/fps if count else meta["duration_seconds"]
    times=[0 if args.samples==1 else duration*i/(args.samples-1) for i in range(args.samples)]
    thumbs=[]
    for i,t in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
        ok,frame=cap.read()
        if not ok: continue
        h,w=frame.shape[:2]
        scale=min(360/w,640/h)
        frame=cv2.resize(frame,(int(w*scale),int(h*scale)))
        name=f"frame_{i+1:02d}_{t:07.2f}s.jpg"
        p=frames/name
        cv2.imwrite(str(p),frame,[int(cv2.IMWRITE_JPEG_QUALITY),92])
        im=Image.open(p).convert("RGB")
        thumbs.append((im,t))
    cap.release()
    if thumbs:
        tw,th=360,680
        sheet=Image.new("RGB",(tw*3,(th+34)*math.ceil(len(thumbs)/3)),(24,24,30))
        d=ImageDraw.Draw(sheet)
        for i,(im,t) in enumerate(thumbs):
            im.thumbnail((tw,th))
            x=(i%3)*tw+(tw-im.width)//2; y=(i//3)*(th+34)
            sheet.paste(im,(x,y+30)); d.text((i%3*tw+10,y+8),f"{t:.2f}s",fill="white")
        sheet.save(out/"contact_sheet.jpg",quality=92)
    print(json.dumps(meta,indent=2))
    print(f"Saved inspection to: {out.resolve()}")

if __name__=="__main__": main()

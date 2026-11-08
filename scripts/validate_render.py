#!/usr/bin/env python3
"""Validate a rendered Reel's technical properties and optional event timeline."""
import argparse, csv, json, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--timeline")
    ap.add_argument("--expected-width",type=int,default=1080)
    ap.add_argument("--expected-height",type=int,default=1920)
    ap.add_argument("--expected-fps",type=float,default=30)
    ap.add_argument("--fps-tolerance",type=float,default=0.05)
    args=ap.parse_args()
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",args.video],text=True))
    v=next((s for s in data.get("streams",[]) if s.get("codec_type")=="video"),None)
    a=next((s for s in data.get("streams",[]) if s.get("codec_type")=="audio"),None)
    if not v: print("FAIL: no video stream"); sys.exit(2)
    def fps(s):
        n,d=(s.get("avg_frame_rate") or s.get("r_frame_rate") or "0/1").split("/")
        return float(n)/float(d) if float(d) else 0
    actual_fps=fps(v); duration=float(data.get("format",{}).get("duration",0))
    checks={
        "resolution":(v.get("width")==args.expected_width and v.get("height")==args.expected_height,
                      f'{v.get("width")}x{v.get("height")} expected {args.expected_width}x{args.expected_height}'),
        "fps":(abs(actual_fps-args.expected_fps)<=args.fps_tolerance,
               f"{actual_fps:.3f} fps expected {args.expected_fps}"),
        "audio_present":(a is not None,"audio stream present" if a else "audio stream missing"),
        "h264":(v.get("codec_name")=="h264",f"video codec {v.get('codec_name')}"),
        "yuv420p":(v.get("pix_fmt")=="yuv420p",f"pixel format {v.get('pix_fmt')}")
    }
    for k,(ok,msg) in checks.items(): print(("PASS" if ok else "FAIL")+f" {k}: {msg}")
    timeline_info=None
    if args.timeline:
        with open(args.timeline,encoding="utf-8-sig",newline="") as f:
            reader=csv.DictReader(f); rows=list(reader); fields=reader.fieldnames or []
        required={"event_id","frame","time_seconds","phrase_id","event_type","malayalam_text","pitch_row"}
        missing=sorted(required-set(fields))
        sorted_ok=True
        try: sorted_ok=all(int(rows[i]["frame"])<=int(rows[i+1]["frame"]) for i in range(len(rows)-1))
        except Exception: sorted_ok=False
        print(("PASS" if not missing else "FAIL")+f" timeline columns: missing={missing}")
        print(("PASS" if sorted_ok else "FAIL")+f" timeline order: {len(rows)} events")
        timeline_info={"events":len(rows),"missing_columns":missing,"chronological":sorted_ok}
        checks["timeline_columns"]=(not missing,str(missing))
        checks["timeline_order"]=(sorted_ok,"chronological frames")
    report={"video":str(Path(args.video).resolve()),"duration_seconds":duration,
            "resolution":[v.get("width"),v.get("height")],"fps":actual_fps,
            "audio_codec":a.get("codec_name") if a else None,
            "timeline":timeline_info,
            "checks":{k:{"passed":ok,"detail":msg} for k,(ok,msg) in checks.items()},
            "all_passed":all(x[0] for x in checks.values())}
    Path("render_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    sys.exit(0 if report["all_passed"] else 1)

if __name__=="__main__": main()

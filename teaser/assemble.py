"""Stitch the TEMPO teaser: intro (Manim) + real-robot footage (wine pour at 2x) + results outro (Manim).

Usage:  python assemble.py [--pour-start 27.7] [--pour-speed 2.0]
Writes  tempo_teaser.mp4 (crf 18 master) and tempo_teaser_web.mp4 (crf 27, for the website).
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found: install it or `pip install imageio-ffmpeg`")


def find_render(scene_file, scene_name, fallback):
    cand = os.path.join(HERE, "media", "videos", scene_file, "1080p30", scene_name + ".mp4")
    if os.path.exists(cand):
        return cand
    fb = os.path.join(HERE, "renders", fallback)
    if os.path.exists(fb):
        return fb
    sys.exit(f"missing render for {scene_name}: looked in {cand} and {fb}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pour-start", type=float, default=27.7, help="footage time where Wine Pour begins (s)")
    ap.add_argument("--pour-speed", type=float, default=2.0, help="playback speed for the Wine Pour segment")
    ap.add_argument("--footage", default=os.path.join(HERE, "footage", "rollouts_4tasks.mp4"))
    ap.add_argument("--out", default=os.path.join(HERE, "tempo_teaser.mp4"))
    args = ap.parse_args()

    ff = ffmpeg_exe()
    intro = find_render("tempo_intro_timed", "IntroTimed", "intro_timed_30s.mp4")
    outro = find_render("tempo_combined", "Outro", "outro.mp4")
    norm = "format=yuv420p,fps=30,scale=1920:1080,setsar=1"
    fc = (
        f"[0:v]{norm}[a];"
        f"[1:v]trim=0:{args.pour_start},setpts=PTS-STARTPTS,{norm}[b1];"
        f"[1:v]trim=start={args.pour_start},setpts=(PTS-STARTPTS)/{args.pour_speed},{norm}[b2];"
        f"[2:v]{norm}[c];"
        f"[a][b1][b2][c]concat=n=4:v=1:a=0[v]"
    )
    subprocess.run([ff, "-v", "error", "-y", "-i", intro, "-i", args.footage, "-i", outro,
                    "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-movflags", "+faststart", args.out], check=True)
    web = os.path.splitext(args.out)[0] + "_web.mp4"
    subprocess.run([ff, "-v", "error", "-y", "-i", args.out, "-c:v", "libx264", "-crf", "27", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", web], check=True)
    print("wrote", args.out)
    print("wrote", web)


if __name__ == "__main__":
    main()

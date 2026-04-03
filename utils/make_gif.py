import asyncio
from playwright.async_api import async_playwright
import os
import glob
import subprocess
import imageio_ffmpeg

async def record_video():
    print("Launching browser to record signature...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': 600, 'height': 200},
            record_video_dir=".",
            record_video_size={"width": 600, "height": 200}
        )
        page = await context.new_page()
        html_path = os.path.abspath("index.html").replace(chr(92), "/")
        await page.goto(f"file:///{html_path}")
        
        await page.evaluate("document.getElementById('ctrlBtn')?.remove();")
        print("Recording 24 seconds of animation in ultra high quality...")
        await page.wait_for_timeout(24000)
        await context.close()
        await browser.close()
    
    videos = glob.glob("*.webm")
    if not videos: return
    webm_file = max(videos, key=os.path.getmtime)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    print("Generating color palette for flawless GIF quality...")
    subprocess.run([
        ffmpeg_exe, "-y", "-i", webm_file,
        "-vf", "fps=25,scale=600:-1:flags=lanczos,palettegen=stats_mode=diff",
        "palette.png"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Rendering final high-quality GIF...")
    subprocess.run([
        ffmpeg_exe, "-y", "-i", webm_file, "-i", "palette.png",
        "-filter_complex", "fps=25,scale=600:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5",
        "signature_hq.gif"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    os.remove(webm_file)
    os.remove("palette.png")
    print("Successfully created signature_hq.gif with maximum quality!")

if __name__ == "__main__":
    asyncio.run(record_video())

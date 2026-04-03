import asyncio
from playwright.async_api import async_playwright
import os
import glob
import subprocess
import imageio_ffmpeg

async def record_video():
    print("Launching browser to record video...")
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
    
    print("Converting to high quality MP4...")
    subprocess.run([
        ffmpeg_exe, "-y", "-i", webm_file,
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "signature.mp4"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    os.remove(webm_file)
    print("Successfully created signature.mp4!")

if __name__ == "__main__":
    asyncio.run(record_video())

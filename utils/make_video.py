import asyncio
from playwright.async_api import async_playwright
import os
import glob
import subprocess
import imageio_ffmpeg

async def record_video():
    print("Launching browser for ELITE 4K Ultra recording (2400x800)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': 600, 'height': 200},
            device_scale_factor=4, # Captures at 2400x800 for pro quality
            record_video_dir=".",
            record_video_size={"width": 2400, "height": 800}
        )
        page = await context.new_page()
        html_path = os.path.abspath("index.html").replace(chr(92), "/")
        await page.goto(f"file:///{html_path}")
        
        # Hide standard controls for professional look
        await page.evaluate("document.getElementById('ctrlBtn')?.remove();")
        
        print("Recording 24 seconds of animation in 4K resolution...")
        await page.wait_for_timeout(24000)
        await context.close()
        await browser.close()
    
    videos = glob.glob("*.webm")
    if not videos: return
    
    webm_file = max(videos, key=os.path.getmtime)
    print(f"Recorded 4K video: {webm_file}")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Render with "High Profile" H.264 for pro-grade color and sharpness
    print("Encoding to ultra-crisp pro-quality MP4 (signature_pro_4k.mp4)...")
    subprocess.run([
        ffmpeg_exe, "-y", "-i", webm_file,
        "-c:v", "libx264", "-profile:v", "high", "-crf", "12", "-pix_fmt", "yuv420p",
        "signature_pro_4k.mp4"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    os.remove(webm_file)
    print("SUCCESS! Captured signature in stunning 4K clarity!")
    print("Check your folder for: signature_pro_4k.mp4")

if __name__ == "__main__":
    asyncio.run(record_video())

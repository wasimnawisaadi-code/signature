import asyncio
from playwright.async_api import async_playwright
import os
import glob
import subprocess
import imageio_ffmpeg

async def record_video():
    print("Launching browser for ULTRA-HD recording (1200x400)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Scale everything up by 2x for Retina-level sharpness
        context = await browser.new_context(
            viewport={'width': 600, 'height': 200},
            device_scale_factor=2, # Captures at 1200x400
            record_video_dir=".",
            record_video_size={"width": 1200, "height": 400}
        )
        page = await context.new_page()
        html_path = os.path.abspath("index.html").replace(chr(92), "/")
        await page.goto(f"file:///{html_path}")
        
        # Remove pause button
        await page.evaluate("document.getElementById('ctrlBtn')?.remove();")
        
        print("Recording 24 seconds of animation in 2K HD...")
        await page.wait_for_timeout(24000)
        await context.close()
        await browser.close()
    
    videos = glob.glob("*.webm")
    if not videos:
        print("Error: No video output found.")
        return
    
    webm_file = max(videos, key=os.path.getmtime)
    print(f"Recorded HD video: {webm_file}")
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Pass 1: Generate ultra-precise 256-color palette
    # Using 'sierra2_4a' dither and 'max_colors=256' for the cleanest possible white background
    print("Building high-fidelity color palette...")
    subprocess.run([
        ffmpeg_exe, "-y", "-i", webm_file,
        "-vf", "fps=25,palettegen=stats_mode=diff:reserve_transparent=0",
        "palette.png"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Pass 2: Render final ULTRA-sharp GIF
    # We keep the 1200px width for extreme clarity
    print("Rendering final ULTRA-HD GIF (signature_ultra_hd.gif)...")
    subprocess.run([
        ffmpeg_exe, "-y", "-i", webm_file, "-i", "palette.png",
        "-filter_complex", "fps=25[x];[x][1:v]paletteuse=dither=sierra2_4a",
        "signature_ultra_hd.gif"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Cleanup
    os.remove(webm_file)
    os.remove("palette.png")
    print("FINISH! Signature generated in ultra high definition!")
    print("Check your folder for: signature_ultra_hd.gif")

if __name__ == "__main__":
    asyncio.run(record_video())

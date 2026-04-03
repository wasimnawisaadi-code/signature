from PIL import Image
import os

FOLDER = r"C:\Users\LENOVO\Downloads\signature final"
LOGOS  = [
    "logo_iata.png",
    "logo_dtcm.png",
    "logo_17th.png",
    "logo_uaf.png",
    "logo_iso.png",
    "logo_flydubai.png",
    "logo_assessment.png",
]

def remove_white_bg(path, threshold=230):
    img = Image.open(path).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # If pixel is very light/white → make transparent
            if r >= threshold and g >= threshold and b >= threshold:
                # Feather: how white is it beyond threshold?
                whiteness = min(r, g, b)
                fade = int(255 * (255 - whiteness) / (255 - threshold + 1))
                pixels[x, y] = (r, g, b, fade)
    img.save(path, "PNG")
    print(f"  OK  {os.path.basename(path)}")

print("Removing white backgrounds from logos...")
for logo in LOGOS:
    full = os.path.join(FOLDER, logo)
    if os.path.exists(full):
        try:
            remove_white_bg(full)
        except Exception as e:
            print(f"  ERR {logo}: {e}")
    else:
        print(f"  --  {logo} not found, skipping")

print("\nAll done!")

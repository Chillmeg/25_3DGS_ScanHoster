import requests, io
from PIL import Image

API_KEY = "AIzaSyAOO3xb40IdnBzC4YBFKXAllUvR3MECXuM"
lat, lon = 45.4374, 12.3348
fov = 85

# First: check if Street View exists here
meta = requests.get("https://maps.googleapis.com/maps/api/streetview/metadata",
    params={"location": f"{lat},{lon}", "key": API_KEY}).json()
print("Metadata:", meta)
if meta.get("status") != "OK":
    raise SystemExit(f"No Street View available: {meta}")

imgs = []
for h in range(0, 360, fov):
    r = requests.get("https://maps.googleapis.com/maps/api/streetview",
        params={"size":"640x640","location":f"{lat},{lon}",
                "heading":h,"fov":fov,"pitch":0,"key":API_KEY})
    print(f"heading={h}: status={r.status_code}, type={r.headers.get('content-type')}, bytes={len(r.content)}")
    if "image" not in r.headers.get("content-type", ""):
        print("Response body:", r.text[:300])
        raise SystemExit("Not an image — see error above")
    imgs.append(Image.open(io.BytesIO(r.content)))

strip = Image.new('RGB', (640*8, 640))
for i, img in enumerate(imgs): strip.paste(img, (i*640, 0))
strip.save("strip.png")
print("Saved strip.png")
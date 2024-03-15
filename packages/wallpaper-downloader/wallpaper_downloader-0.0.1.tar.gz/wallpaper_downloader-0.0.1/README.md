# Wallpaper Downloader
wallpaper-downloader is a simple Python module to easily download wallpaper images from websites that we supported.


# Installation
```bash
pip install wallpaper-downloader
```

# Usage
```python
from walldown import WallpaperFlare
from walldown import download_url


wf = WallpaperFlare("Space")
for img in wf.search(2):
    print("name: ", img.name)
    print("size: ", img.size)
    print("width: ", img.width)
    print("height: ", img.height)
    print("url: ", img.url)
    print("preview: ", img.preview)
    print("keywords: ", list(img.keywords))
    print("description: ", img.description)
    print("px_resolution: ", img.px_resolution)
    print("=" * 30)

    # To download image uncomment this line
    # download_url(img.url)
```
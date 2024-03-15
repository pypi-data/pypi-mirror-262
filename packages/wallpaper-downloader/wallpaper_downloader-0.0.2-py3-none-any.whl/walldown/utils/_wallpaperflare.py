#!/usr/bin/python3

from ..progress_bar import download_url
from typing import Generator
from bs4 import BeautifulSoup
from lxml import html
import requests



class WallpaperFlare:
    """Wallpaper Flare automation image downloader

    Usage:
    ```python
        wf = WallpaperFlare("Space")
        for img in wf.search(count=3):
            print(img.name, img.size)
    ```
    """

    URL: str = "https://www.wallpaperflare.com"


    class Image:
        def __init__(self, image_link: str) -> str:
            self._image_data = WallpaperFlare._bs4(WallpaperFlare._join_url(image_link.get("href"), "download"))
            self._image_html = html.fromstring(self._image_data.encode())

        @property
        def size(self) -> int:
            return requests.head(self.url).headers.get("content-length")

        @property
        def url(self) -> str:
            return self._image_data.find("img", id="show_img").get("src")

        @property
        def name(self) -> str:
            return self._image_data.find("figcaption", attrs={"itemprop": "caption"}).text
        
        @property
        def width(self) -> int:
            return int(self._image_html.xpath('//div[@class="dld_info"]//span[@itemprop="width"]//span[@itemprop="value"]')[0].text.strip())

        @property
        def height(self) -> str:
            return int(self._image_html.xpath('//div[@class="dld_info"]//span[@itemprop="height"]//span[@itemprop="value"]')[0].text.strip())
        
        @property
        def px_resolution(self) -> str:
            return self._image_data.find("div", class_="dld_info").text.split(":")[-1].strip()
        
        @property
        def preview(self) -> str:
            return self._image_data.find("img", id="dld_thumb", attrs={"itemprop": "thumbnail"}).get("src")
        
        @property
        def keywords(self) -> Generator:
            return map(lambda x: x.strip(), self._image_data.find("meta", attrs={"itemprop": "keywords"}).get("content").split(","))
        
        @property
        def description(self) -> str:
            return self._image_data.find("meta", attrs={"itemprop": "description"}).get("content")

        def download(self, path: str = None, fname: str = None) -> None:
            download_url(self.url, path, fname)

    def __init__(self, 
                 query: str, 
                 page: int = 0,
                 width: str | int = None, 
                 height: str | int = None, 
                 is_mobile: bool = False):

        self.query = query.strip()
        self.page = page
        self.width = width
        self.height = height
        self.is_mobile = is_mobile

    @property
    def _search_url(self) -> str:
        return (self._join_url(self.URL, "search?")
                + f"wallpaper={self.query}"
                + f"&page={self.page}" if self.page >= 0 else ""
                + f"&width={self.width}" if self.width is not None else ""
                + f"&height={self.height}" if self.height is not None else ""
                + "&mobile=ok" if self.is_mobile else ""
            )

    @classmethod
    def _join_url(cls, *args) -> str:
        return "/".join(args)
    
    @classmethod
    def _bs4(cls, url: str, **kwargs) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url, stream=True, **kwargs).content, 'lxml')

    def search(self, count: int = -1) -> Generator:
        return map(WallpaperFlare.Image, self._bs4(self._search_url).find_all("a", attrs={"itemprop": "url"})[:count])


if __name__ == "__main__":
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
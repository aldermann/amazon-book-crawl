import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from tqdm import tqdm

first_selector = ".s-access-detail-page"
other_selector = ".s-result-list.s-search-results.sg-row h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 > a"

first_url = "https://www.amazon.com/b/?node=15762881&ref_=Oct_CateC_173508_0&pf_rd_p=07d7dc4a-b93c-5561-8d0b-4968d722a9a4&pf_rd_s=merchandised-search-3&pf_rd_t=101&pf_rd_i=173508&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6GD8TJTBJJJXF8B9QSHA&pf_rd_r=6GD8TJTBJJJXF8B9QSHA&pf_rd_p=07d7dc4a-b93c-5561-8d0b-4968d722a9a4"

first_page_next_selector = "#pagnNextLink"
other_page_next_selector = ".a-pagination>.a-last>a"

sess = requests.Session()
sess.headers.update({
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7,vi;q=0.6",
    "cache-control": "max-age=0",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": 'session-id=138-3466000-2647616; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:VN"; ubid-main=135-8207411-0396738; x-wl-uid=1OvcQf/7hLtwNFXf/2fURGcifuyJ3Q8bHLwVydm67W6Xfkb0CbvPhh3bX3E0d0dyTZOaIDuPcLR8=; session-token=BmTgGqj3fHijkAZHHlqbNKu+JJsMArRvjOlaU8l/sMhtoC45ZdBl6UUGgk4X+h+DPL2Tj3qyuh9kmX021ntQIcbB1WixAmHIZNd2/nHXVl2UX74XszVQmAAwZeofuaDgziB7TAPxdOzg4sgag28C6uydsE7WIam7Hf7tj9nzIaLPovihi/PbVfKhlJXpWWIk5o2UJFhpTcrGWlnrKS/s3uBaj/eg/3zNbvJ3mrWmS6ygrU4fENizMOdP5FLgRnpw; csm-hit=tb:s-CSZGBY2QFHYYKFXEVDVF|1567338953279&t:1567338956868&adb:adblk_yes'
})


def get_book_links(url, sel, next_sel):
    resp = None
    nextPageLink = None
    for _ in range(1, 100):
        resp = sess.get(url)
        if resp.status_code == 200:
            break
    if resp.status_code != 200:
        return ([], nextPageLink)
    html = BS(resp.text, "html.parser")

    anchors = html.select(sel)
    res = []
    for a in anchors:
        h = a["href"]
        if "amazon" not in h:
            h = urljoin("https://www.amazon.com", h)
        res.append(h)
    if (len(html.select(next_sel)) == 0):
        return res, None
    nextPageLink = html.select(next_sel)[0]["href"]
    if "amazon" not in nextPageLink:
        nextPageLink = urljoin("https://www.amazon.com", nextPageLink)
    return (res, nextPageLink)

all_book_links = []
f = open("links.txt", "w")
def crawl_page(url, it):
    nextPageLink = None
    if it == 1:
        book_links, nextPageLink = get_book_links(
            url, first_selector, first_page_next_selector)
    else:
        book_links, nextPageLink = get_book_links(
            url, other_selector, other_page_next_selector)
    all_book_links.extend(book_links)
    tqdm.write(f"Found {len(book_links)} links in page {it}")
    for link in book_links:
        f.write(link)
        f.write("\n")
    return nextPageLink


url = first_url
for it in tqdm(range(1, 76), desc="Get books links progress"):
    nextPage = crawl_page(url, it)
    if nextPage is None:
        break
    url = nextPage

f.close()

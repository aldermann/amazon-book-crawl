import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
import scrap_detail
import upload_detail
from tqdm import tqdm

first_selector = ".s-access-detail-page"
other_selector = ".s-result-list.s-search-results.sg-row h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 > a"

first_url = "https://www.amazon.com/b/?node=15762881&ref_=Oct_CateC_173508_0&pf_rd_p=07d7dc4a-b93c-5561-8d0b-4968d722a9a4&pf_rd_s=merchandised-search-3&pf_rd_t=101&pf_rd_i=173508&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6GD8TJTBJJJXF8B9QSHA&pf_rd_r=6GD8TJTBJJJXF8B9QSHA&pf_rd_p=07d7dc4a-b93c-5561-8d0b-4968d722a9a4"
other_url_tmpl = "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A1000%2Cn%3A1%2Cn%3A173508%2Cn%3A15762881&page={page}&qid=1567152919&ref=sr_pg_3"


sess = requests.Session()
sess.headers.update({
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7,vi;q=0.6",
    "cache-control": "max-age=0",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": 'session-id=147-9226649-5809203; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9: VN"; x-wl-uid=1NoJiLkWZ7msmSPkxSqpHvND/J3lRDcuIvt1mWW7rgjMZZmxYdP1svQ4IVwnrfASdgZa2nhCaq8I=; ubid-main=134-3518144-0922607; session-token=xREIcuVlcwQom5JQn275fFD4HvlejehRt8SohNSE3+HisElCZkHMioSc0IqvlD8IWIeDMr0QR5L+MTYLiqhdXI6ZTFXT4SW78aNEG4bUBJVkkRRzHZuSgZQ4bTgWv+BLMF6MdbKvrZfvJ4VcueZy7C24gcaMiv3KtmluSo+MwzS8vRSZnunXKRNjhJdO1oAs; csm-hit=tb:MF3M8H0DE73K3T2BEMTS+s-MF3M8H0DE73K3T2BEMTS|1567236278567&t:1567236278567&adb:adblk_yes'
})

# sess.proxies = {
#     "https": "https://115.68.14.247:3128"
# }


def get_book_links(url, sel):
    resp = None
    while True:
        resp = sess.get(url)
        if resp.status_code == 200:
            break
    html = BS(resp.text, "html.parser")

    anchors = html.select(sel)
    res = []
    for a in anchors:
        h = a["href"]
        if "amazon" not in h:
            h = urljoin("https://www.amazon.com", h)
        res.append(h)
    return res


left_over_links = []


def crawl_page(it):
    book_links = []
    if it == 1:
        book_links = get_book_links(first_url, first_selector)
    else:
        book_links = get_book_links(
            other_url_tmpl.format(page=it), other_selector)
    details = []
    for link in tqdm(book_links, desc=f"Scraping progress in page {it}"):
        detail = scrap_detail.scrap_book_detail(link, sess, random_cookie=True)
        if isinstance(detail, int):
            tqdm.write(
                f"Error fetching page: {link} with error code: {detail}. Putting in leftover links")
            left_over_links.append(link)
            continue
        detail = {**detail, "_index": "amazon_books",
                  "_type": "books", "URL": link}
        details.append(detail)

    tqdm.write(f"Uploading page {it} to Elasticsearch")
    upload_detail.upload_detail_bunk(details)


for it in tqdm(range(21, 31), desc="Page progress"):
    crawl_page(it)

for it in range(5):
    details = []
    curr_leftover = []
    for link in tqdm(left_over_links, desc=f"Scraping progress in left over links"):
        detail = scrap_detail.scrap_book_detail(link, sess, random_cookie=True)
        if isinstance(detail, int):
            tqdm.write(
                f"Error fetching page: {link} with error code: {detail}")
            curr_leftover.append(link)
            continue
        detail = {**detail, "_index": "amazon_books",
                  "_type": "books", "URL": link}
        details.append(detail)
    tqdm.write(f"Uploading left over links to Elasticsearch")
    upload_detail.upload_detail_bunk(details)
    if len(curr_leftover) == 0:
        break
    else:
        left_over_links = curr_leftover

from tqdm import tqdm
import scrap_detail
import upload_detail
import requests

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

f = open("links.txt", "r")
all_book_links = []
line = f.readline()
while line:
    all_book_links.append(line)
    line = f.readline()

for it in range(200):
    details = []
    left_over = []
    for link in tqdm(all_book_links, desc="Scraping books data progress"):
        detail = scrap_detail.scrap_book_detail(link, sess, random_cookie=True)
        if isinstance(detail, int):
            left_over.append(link)
            continue
        tqdm.write("Fetched")
        detail = {**detail, "_index": "amazon_books",
                "_type": "books", "URL": link}
        details.append(detail)
    tqdm.write("Uploading {} links to Elasticsearch".format(len(details)))
    try:
        upload_detail.upload_detail_bunk(details)
    except:
        print("Error")

    if len(left_over) == 0:
        break
    else:
        all_book_links = left_over

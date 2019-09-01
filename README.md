# Book crawl from Amazon.

-   Crawl from this [starting link](https://www.amazon.com/b/?node=15762881&ref_=Oct_CateC_173508_0&pf_rd_p=07d7dc4a-b93c-5561-8d0b-4968d722a9a4&pf_rd_s=merchandised-search-3&pf_rd_t=101&pf_rd_i=173508&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=6GD8TJTBJJJXF8B9QSHA&pf_rd_r=6GD8TJTBJJJXF8B9QSHA&pf_rd_p=07d7dc4a-b93c-5561-8d0b-4968d722a9a4)
-   Every page is scraped for books pages link. These links are revisited seperately, and products data is fetched from this page.
-   Links that is blocked by Captcha is put into a leftover links list. The list is sieved for 20 times or until no leftover links are not visited.
-   After scraping every books in a page, we index the result to Elasticsearch.

## Indexed result:
Elasticsearch url: [https://fz98j6ogqz:qez1c4u6k6@book-crawl-amazon-632909585.ap-southeast-2.bonsaisearch.net:443](https://fz98j6ogqz:qez1c4u6k6@book-crawl-amazon-632909585.ap-southeast-2.bonsaisearch.net:443)

Index name is: /amazon_books

## How to use?:
-   `pip3 install requests beautifulsoup4 tqdm elasticsearch`
-   `python3 crawl.py`
-   `python3 crawl_book.py`

## Shortcoming:
- Because of captcha, I could only scrape 438 in 1196 books.

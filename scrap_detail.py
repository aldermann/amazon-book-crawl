import requests
from bs4 import BeautifulSoup as BS
import re




def scrap_book_detail(url, sess, random_cookie=False):
    try:
        resp = sess.get(url)
        if resp.status_code != 200:
            return resp.status_code
        html = BS(resp.text, "html.parser")
        res = ""
        detail = html.select(".bucket > .content > ul > li")
        for d in detail:
            for st in d.find_all("style"):
                st.decompose()
            for sc in d.find_all("script"):
                sc.decompose()
            for a in d.find_all("script"):
                sc.decompose()
            s = d.get_text().strip()
            s = re.sub("(?!\n)\s+", " ", s)
            s = re.sub("\n{2,}", " ", s)
            s = s.replace("(View shipping rates and policies)", "")
            s = s.replace("(See Top 100 in Books)", "")
            res += s + '\n'
        key = None
        last_string = ""
        data = {}
        title = html.find("h1", id="title").get_text().replace("\n", " ").strip()
        data["Title"] = title
        for line in res.split('\n'):
            if ":" in line:
                if key is not None:
                    last_string = re.sub("(#([0-9],)+)", "\n\\1", last_string)
                    data[key] = last_string
                part = line.split(":", 1)
                key, last_string = part
            else:
                last_string += line + ' '
        last_string = re.sub("(#([0-9]|,)+)", "\n\\1", last_string)
        data[key] = last_string
        return data
    except AttributeError as err:
        print(url)
        raise err

import requests_html
from assets.page_builder import PageBuilder
from bs4 import BeautifulSoup as bs

import config

class Parser:
    def __init__(self, url):
        self.url = url
        self.session = requests_html.HTMLSession()
        self.articles = []

    def parse_articles(self):
        inc = 1
        while True:
            r = self.session.get(self.url + "/page/" + str(inc))
            soup = bs(r.content, "html.parser")

            if soup.find("h1").text == "No Posts Found":
                break

            for article in soup.select("article.article.excerpt"):
                link = article.select_one("a.excerpt-link").get("href")
                content_art = self.session.get(link)
                soup_art = bs(content_art.content, "html.parser")
                content = soup_art.select("h2, p")
                temp = ""
                for i in content:
                    temp += str(i)

                temp = bs(temp, "html.parser")

                h2s = temp.select("h2:not(.screen-reader-text)")
                tmp = temp.select("h2:not(.screen-reader-text) + p")

                image = article.select_one(".post-thumbnail img").get("src")
                desc = article.select_one("div.excerpt-excerpt").text.replace("\n", "")

                for idx, i in enumerate(tmp):
                    if i in temp.select("h2:not(.screen-reader-text) ~ p"):
                        stories = []
                        title = h2s[idx].text

                        from_ = temp.select("h2:not(.screen-reader-text) ~ p").index(tmp[idx])
                        try:
                            to_ = temp.select("h2:not(.screen-reader-text) ~ p").index(tmp[idx + 1])
                            itms = temp.select("h2:not(.screen-reader-text) ~ p")[from_:to_]
                        except:
                            itms = temp.select("h2:not(.screen-reader-text) ~ p")[from_:]

                        for itm in itms:
                            try:
                                if type(int(itm.text[0])) == int:
                                    if itm.text[1] == "." or itm.text[2] == ".":
                                        stories.append(itm.text.replace("\n", ""))
                            except:
                                pass

                        self.articles.append(
                            {
                                "url": link,
                                "title": title,
                                "image": image,
                                "desc": desc,
                                "stories": stories
                            }
                        )

            print("Page", inc)
            inc += 1

    def build(self):
        print(len(self.articles))

        for article in self.articles:
            builder = PageBuilder()
            builder.set_page_poster_path("https://images.pexels.com/photos/1166990/pexels-photo-1166990.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")
            builder.set_page_title(article["title"])
            builder.set_page_link(article["url"])
            builder.build_start_page()
            builder.build_page_head()
            builder.build_story_start(config.publisher, config.publisher_logo)
            builder.build_story(article["title"], "first_story")

            for story in article["stories"]:
                builder.build_story(story)

            builder.build_end_page()
            builder.build_page("stories/" + article["title"].replace(" ", "_").replace("’", "").replace("‘", "").replace("​", ""))
            #print(article, '\n')
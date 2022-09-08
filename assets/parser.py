import requests_html
from bs4 import BeautifulSoup as bs

session = requests_html.HTMLSession()

articles = []

inc = 1
while True:
    r = session.get("https://findyourmomtribe.com/category/parenting/quotes/page/" + str(inc))
    soup = bs(r.content, "html.parser")

    if soup.find("h1").text == "No Posts Found":
        break

    for article in soup.select("article.article.excerpt"):
        articles.append(article)

    print("Page", inc)
    inc += 1

print(len(articles))

for article in articles:
    #print(article.prettify())
    link = article.select_one("a.excerpt-link").get("href")
    title = article.select_one("h2.excerpt-title").text
    description = article.select_one("div.excerpt-excerpt").text
    print(title, description, link)
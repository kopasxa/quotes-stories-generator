import re
import config

class PageBuilder:
    def __init__(self):
        self.page = ""
        self.page_title = ""
        self.page_poster_path = 'https://images.pexels.com/photos/8162662/pexels-photo-8162662.jpeg'
        self.style = config.style_for_page 
        self.story_pages = []
        self.page_link = "" 

    def set_page_title(self, title):
        self.page_title = title

    def set_page_link(self, link):
        self.page_link = link

    def set_page_story(self, story_title, story_link, story_path):
        self.story_pages.append({
            "title": story_title,
            "link": story_link,
            "path_to_image": story_path
        })

    def build_start_page(self):
        self.page += f"""
<!doctype html>
<html ⚡>"""
        return

    def build_page_head(self):
        reg = re.compile('[^0-9\s^a-zA-Z]')
        title = reg.sub('', self.page_title)
        path = f'{config.path_to_stories}/{"_".join(title.split(" ")).split(".")[0]}/index'
        self.page += f"""
    <head>
        <meta charset="utf-8">
        <title>{self.page_title}</title>
        <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
        <link rel="canonical" href="{config.my_domain}{path.split(config.path_root)[1]}.html">
        {self.style}
    </head>
        """
        return

    def build_story(self, title="", story_type="story"):
        if story_type == "first_story":
            self.page += f"""
            <amp-story-page id="cover">
                <amp-story-grid-layer template="fill">
                    <amp-img src="{self.page_poster_path}" width="720" height="1280" layout="responsive">
                    </amp-img>
                </amp-story-grid-layer>
                <amp-story-grid-layer template="vertical">
                    <h1>{self.page_title}</h1>
                </amp-story-grid-layer>
                
            </amp-story-page>
            """
            #<amp-story-page-outlink layout="nodisplay" theme="dark">
            #    <a href="{self.page_link}" title="Read More"></a>
            #</amp-story-page-outlink>
        elif story_type == "story":
            self.page += f"""
            <amp-story-page id="page1">
                <amp-story-grid-layer template="fill">
                    <amp-img src="{self.page_poster_path}" width="720" height="1280" layout="responsive">
                    </amp-img>
                </amp-story-grid-layer>
                <amp-story-grid-layer template="vertical" class="bottom">
                    <h4>{title}</h4>
                </amp-story-grid-layer>
            </amp-story-page>
            """
        return

    def build_story_start(self, publisher, publisher_logo):
        script = '{"ad-attributes": {"type": "adsense","data-ad-client": "ca-pub-5893452305550881","data-ad-slot": "7525101101"}}'
        self.page += f"""
    <body>
        <amp-story standalone title="{self.page_title} | Amerikanki" publisher="{publisher}"
            publisher-logo-src="{publisher_logo}" poster-portrait-src="{self.page_poster_path}">

            <amp-ad width="100vw" height="320"
                type="adsense"
                data-ad-client="ca-pub-8064390991973365"
                data-ad-slot="1224845979"
                data-auto-format="rspv"
                data-full-width="">
                <div overflow=""></div>
            </amp-ad>"""
        return

    def build_end_page(self):
        self.page += """
        </amp-story>
    </body>
</html>"""
        return

    def build_page(self, filename):
        try:
            with open(f"{filename}.html", "w", encoding="utf-8") as page:
                page.write(self.page)
            return 
        except:
            return None
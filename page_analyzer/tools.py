from bs4 import BeautifulSoup


class HTMLParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_title(self):
        title = self.soup.title.string
        if title:
            return title
        return

    def get_h1(self):
        h1 = self.soup.h1
        if h1:
            return h1.string
        return

    def get_content(self):
        for meta in self.soup.find_all('meta'):
            if meta.get('name') == 'description':
                content = meta.get('content')
                return content[:255]
        return

    def check(self):
        result = dict()
        result['title'] = self.get_title()
        result['h1'] = self.get_h1()
        result['content'] = self.get_content()
        return result

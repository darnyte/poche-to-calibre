import string, re
from calibre import strftime
from calibre.web.feeds.recipes import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup

class NYTimes(BasicNewsRecipe):

    title       = 'Poche'
    __author__  = 'Xavier Detant'
    description = 'Ma poche'
    needs_subscription = True
    remove_tags_before = dict(id='article')
    remove_tags_after  = dict(id='article')

    def get_browser(self):
        br = BasicNewsRecipe.get_browser()
        if self.username is not None and self.password is not None:
            br.open('http://app.inthepoche.com/u/FaustXVI/')
            br.select_form(name='loginform')
            br['login']   = self.username
            br['password'] = self.password
            br.submit()
        return br

    def parse_index(self):
        baseURL = 'http://app.inthepoche.com/u/'+self.username+'/'
        soup = self.index_to_soup(baseURL+'index.php')
        articles = {}
        key = None
        ans = []

        for div in soup.findAll(True,attrs={'class':['entrie']}):

                 a = div.find('a', href=True)
                 if not a:
                     continue
                 key = self.tag_to_string(div.find('a',attrs={'class':['reading-time']}))
                 url = baseURL + a['href']
                 title = self.tag_to_string(a, use_alt=False)
                 description = ''
                 pubdate = strftime('%a, %d %b')
                 summary = div.find('p')
                 if summary:
                     description = self.tag_to_string(summary, use_alt=False)

                 feed = key if key is not None else 'Uncategorized'
                 if not articles.has_key(feed):
                     articles[feed] = []
                 articles[feed].append(dict(title=title, url=url, date=pubdate,description=description,content=''))
        ans = [(key, articles[key]) for key in articles.keys()]
        return ans
import requests
import lxml.html as lxmlhtml

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

def get_html(url):
    r = requests.get (url, headers=headers)
    return r.text

def get_pages(html):
    htmlToLXML = lxmlhtml.fromstring(html)
    pages = htmlToLXML.xpath('.//div[@class = "navi"]/span[@class = "navigation"]/a/text()')
    return int (pages[-1])

def get_titles(htmlData):
    htmlToLXML = lxmlhtml.fromstring(htmlData)
    title = htmlToLXML.xpath('.//div[@class = "title"]/a/text()')
    titleScore = htmlToLXML.xpath('.//b[@itemprop = "ratingValue"]/text()')
    titleResult = dict(list(zip(title, titleScore)))
    return titleResult

def main():
    url = 'https://online.anidub.com/anime_movie/'
    htmlData = get_html(url)
    # titlesList = get_titles(htmlData)
    all_pages = get_pages(htmlData)
    for i in range(1, all_pages + 1):
        nextPage = get_html('https://online.anidub.com/anime_movie/page/'+str(i)+'/')
        titlesList = get_titles(nextPage)
        for x in titlesList:
            print(x + ' ' + titlesList[x] + ' parsed')
    


if __name__ == '__main__':
    main ()

import aiohttp
import asyncio
import async_timeout
import lxml.html as lxmlhtml

HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'),
}

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

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://online.anidub.com/anime_movie/')
        all_pages = get_pages(html)
        for i in range(1, all_pages + 1):
            # nextPage = get_html('https://online.anidub.com/anime_movie/page/'+str(i)+'/')
            nextPage = await fetch(session, 'https://online.anidub.com/anime_movie/page/'+str(i)+'/')
            titlesList = get_titles(nextPage)
            for x in titlesList:
                print(x + ' ' + titlesList[x] + ' parsed')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
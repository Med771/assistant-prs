import asyncio
from typing import Optional

from aiohttp import ClientSession
from aiohttp.http_exceptions import HttpProcessingError

from bs4 import BeautifulSoup, Tag

from parse.cap.config import CapConfig

from tools import ParseDecorator


class CapParser:
    @staticmethod
    @ParseDecorator.log_call(prefix="fetch_page")
    async def fetch_page(session, url):
        async with session.get(url) as response:
            if response.status != 200:
                raise HttpProcessingError()

            return await response.text()

    @staticmethod
    @ParseDecorator.log_call(prefix="refactor_page")
    async def refactor_page(session: ClientSession, base_url: str, page: int) -> list:
        links = []
        url = base_url + CapConfig.NEWS_PATH.format(page)

        html = await CapParser.fetch_page(session, url)

        if not html: return links

        soup = BeautifulSoup(html, 'html.parser')
        news_list = soup.find('div', class_='news_list')

        if not news_list: return links

        items = news_list.find_all('div', class_='item_news')

        if not items: return links

        links.extend(await CapParser.get_urls(base_url, items))

        return links

    @staticmethod
    @ParseDecorator.log_call(prefix="get_urls")
    async def get_urls(base_url: str, items: list) -> list:
        news = []

        for item in items:
            link_tag = item.find('a', class_='news-list_title')

            if link_tag:
                href = link_tag['href']
                full_link = base_url + href

                news.append(full_link)

        return news

    @staticmethod
    async def parse_news_page(base_url: str) -> list:
        page = 1
        news = []

        async with ClientSession() as session:
            while True:
                links = await CapParser.refactor_page(session, base_url, page)

                if not links: break

                news.extend(links)

                page += 1

                await asyncio.sleep(0.1)

        return news

    @staticmethod
    async def parse_article_page(url: str) -> Optional[str]:
        async with ClientSession() as session:
            html = await CapParser.fetch_page(session, url)

            if html is None: return None

            soup = BeautifulSoup(html, 'html.parser')

            text_block: Tag = soup.find('div', class_='news_text')

            if text_block is None: return None

            return text_block.get_text(separator=" ", strip=True)
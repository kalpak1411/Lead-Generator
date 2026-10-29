import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebsiteScraper:
    """
    Fetches and extracts clean textual content, titles, meta descriptions,
    headings, and navigational offerings from public company websites.
    """

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    @classmethod
    def fetch_company_info(cls, url, timeout=8):
        """
        Fetches web page content safely. Returns structured extracted metadata.
        Falls back gracefully if live fetch encounters network timeouts or blocks.
        """
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        result = {
            'url': url,
            'title': '',
            'meta_description': '',
            'headings': [],
            'paragraphs': [],
            'raw_text': '',
            'success': False,
            'error': None
        }

        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=timeout, allow_redirects=True)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')

                # Strip scripts and styles
                for element in soup(['script', 'style', 'noscript', 'header', 'footer', 'nav', 'svg']):
                    element.extract()

                # Extract title
                title_tag = soup.find('title')
                result['title'] = title_tag.get_text().strip() if title_tag else ''

                # Extract meta description
                meta_desc = soup.find('meta', attrs={'name': re.compile(r'description', re.I)}) or \
                            soup.find('meta', attrs={'property': 'og:description'})
                if meta_desc and meta_desc.get('content'):
                    result['meta_description'] = meta_desc['content'].strip()

                # Extract H1, H2 headings
                headings = []
                for h in soup.find_all(['h1', 'h2', 'h3'])[:8]:
                    h_text = h.get_text().strip()
                    if h_text and len(h_text) > 5 and len(h_text) < 120:
                        headings.append(h_text)
                result['headings'] = headings

                # Extract paragraphs
                paragraphs = []
                for p in soup.find_all('p'):
                    p_text = re.sub(r'\s+', ' ', p.get_text()).strip()
                    if len(p_text) > 30 and len(p_text) < 400:
                        paragraphs.append(p_text)
                result['paragraphs'] = paragraphs[:15]

                # Combined text
                all_text = ' '.join([result['title'], result['meta_description']] + headings + paragraphs)
                result['raw_text'] = re.sub(r'\s+', ' ', all_text).strip()
                result['success'] = True
            else:
                result['error'] = f"HTTP {resp.status_code}"
        except Exception as e:
            result['error'] = str(e)

        return result


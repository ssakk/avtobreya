import requests
import re
from selectolax.parser import HTMLParser
import json


lex = ['рука', 'база', 'голова', 'круг', 'повод']
cookies = {
    # 'PHPSESSID': '435ij5n3llpgur4blmfstojv4e',
    '_ym_uid': '1701800515689053827',
    '_ym_d': '1701800515',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_gid': 'GA1.2.1259315513.1701800516',
    'cf_clearance': 'gxv6Tgu6GWBzKWvmDw4s.XzxEkL3pFGUyTVYXXgrzbM-1701800516-0-1-89f9d8e4.800f9795.def88704-0.2.1701800516',
    '_ga_0ZV2QQ24QD': 'GS1.1.1701800515.1.1.1701800589.0.0.0',
    '_ga': 'GA1.2.1357408295.1701800515',
}

headers = {
    'authority': 'lexicography.online',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PHPSESSID=435ij5n3llpgur4blmfstojv4e; _ym_uid=1701800515689053827; _ym_d=1701800515; _ym_isad=1; _ym_visorc=w; _gid=GA1.2.1259315513.1701800516; cf_clearance=gxv6Tgu6GWBzKWvmDw4s.XzxEkL3pFGUyTVYXXgrzbM-1701800516-0-1-89f9d8e4.800f9795.def88704-0.2.1701800516; _ga_0ZV2QQ24QD=GS1.1.1701800515.1.1.1701800589.0.0.0; _ga=GA1.2.1357408295.1701800515',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def get_page_parser(word):
    response = requests.get(f'https://lexicography.online/explanatory/mas/{word[0]}/{word}', cookies=cookies, headers=headers)

    return HTMLParser(response.content)


def get_meanings(lexems):
    res = {}
    for word in lexems:
        text = get_page_parser(word).css_first("p").html
        pattern = re.compile(r'<b>\d+</b>\. (<i>[^<]+</i>)?[^<]*([А-ЯёЁ][^<]+)<')
        matches = pattern.findall(text)
        res[word] = matches

    return res


meanings = get_meanings(lex)
with open('meanings.json', 'w', encoding='utf-8') as f:
    json.dump(meanings, f, ensure_ascii=False)

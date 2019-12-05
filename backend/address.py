import aiohttp
import re

from sqlalchemy.sql import text, select, func, literal_column

import db
import utils


class Address:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn

    async def list(self, search_text):
        if search_text is None:
            return None

        pattern = re.compile('[a-z]')
        search_text = self.detransliterate(search_text) \
                if len(pattern.findall(search_text)) > 0 else search_text
        url = 'https://suggestions.dadata.ru/suggestions/api/' + \
                '4_1/rs/suggest/address'
        token = '879a23c709950474156f0782498fb9dfb7496b88'
        payload = {
                'query':'санкт-петербург %s'%search_text,
                'count':10,
                #'locations': [{
                    #'kladr_id': '78'
                    #'kladr_id': '47'
                    #'city_fias_id': 'c2deb16a-0330-4f05-821f-1d09c93331e6'
                #}],
                }
        headers = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'Authorization':'Token %s'%token,}

        json_data = None
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                        url,
                        params=payload,
                        headers=headers) as resp:
                json_data = await resp.json()

        return [item for item in json_data["suggestions"] if \
                item["data"]["street"] is not None]

    def detransliterate(self, text):
        ru_text = ''
        letters = {
           'a' : 'а',
           'b' : 'б',
           'v' : 'в',
           'g' : 'г',
           'd' : 'д',
           'e' : 'е',
           'z' : 'з',
           'i' : 'и',
           'y' : 'й',
           'j' : 'й',
           'k' : 'к',
           'l' : 'л',
           'm' : 'м',
           'n' : 'н',
           'o' : 'о',
           'p' : 'п',
           'r' : 'р',
           's' : 'с',
           't' : 'т',
           'u' : 'у',
           'f' : 'ф',
           'h' : 'х',
           '\'' : 'ь',
           'e' : 'э',}

        multiple_letters = {
           'zh' : 'ж',
           'ts' : 'ц',
           'ch' : 'ч',
           'sh' : 'ш',
           'sch' : 'щ',
           'yu' : 'ю',
           'ya' : 'я',
           'ju' : 'ю',
           'ja' : 'я',}

        ru_text = text.lower()
        for letter_translit, letter in multiple_letters.items():
            ru_text = re.sub(letter_translit, letter, ru_text)

        for letter_translit, letter in letters.items():
            ru_text = re.sub(letter_translit, letter, ru_text)

        return ru_text


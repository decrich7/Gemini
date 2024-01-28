# -*- coding: utf-8 -*-
import asyncio
import re
import random
import logging
from aiogram.utils.markdown import quote_html

import markdown
from sulguk import transform_html

from tgbot.services.Gemini import BaseAioRequests
from tgbot.services.db_api import db
from tgbot.services.db_api.schemas.data import Token, Proxy


class TextInput(BaseAioRequests):
    def __init__(self, key: str, proxy: dict, base_url='https://generativelanguage.googleapis.com/v1beta/models',
                 model='gemini-pro',
                 func='generateContent', headers={'Content-Type': 'application/json'}):
        BaseAioRequests.__init__(self, key, proxy, base_url, model, func, headers)

    def make_json(self, msg: str, params=None) -> dict:
        if params:

            return {
                "contents": [{
                    "parts": [
                        {"text": msg}
                    ]
                }],
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": params.get("HARM_CATEGORY_SEXUALLY_EXPLICIT") if params.get(
                            "HARM_CATEGORY_SEXUALLY_EXPLICIT") else "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": params.get("HARM_CATEGORY_HATE_SPEECH") if params.get(
                            "HARM_CATEGORY_HATE_SPEECH") else "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": params.get("HARM_CATEGORY_HARASSMENT") if params.get(
                            "HARM_CATEGORY_HARASSMENT") else "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": params.get("HARM_CATEGORY_DANGEROUS_CONTENT") if params.get(
                            "HARM_CATEGORY_DANGEROUS_CONTENT") else "BLOCK_ONLY_HIGH"
                    }
                ],
                "generationConfig": {
                    "temperature": params.get('temperature') if params.get('temperature') else 0.5,
                    "maxOutputTokens": params.get('maxOutputTokens') if params.get('maxOutputTokens') else 2000
                    # "topP": params.get('topP'),
                    # "topK": params.get('topK') if params.get('topK') else 40
                }
            }
        else:
            return {
                "contents": [
                    {"parts": [{"text": msg}]}
                ]
            }

    async def get_answer(self, msg, params=None) -> str:
        response = await self.get_response(msg, params)

        if response.get('candidates'):

            finish_reason = response.get('candidates')[0].get('content').get('finishReason')
            if finish_reason:
                if finish_reason == 'SAFETY':
                    logging.exception(f'Error TextInput: {finish_reason}')

                    return ' Генерация контента была отменена по соображениям безопасности(нарушение политики безопасности)'
                elif finish_reason == 'MAX_TOKENS':
                    logging.exception(f'Error TextInput: {finish_reason}')

                    return ' Достигнуто максимальное количество токенов, попробуйте другой запрос '

                elif finish_reason == 'RECITATION':
                    logging.exception(f'Error TextInput: {finish_reason}')

                    return '  Генерация контента была отменена по причине "Цитирования"  '

                elif finish_reason == 'OTHER':
                    logging.exception(f'Error TextInput: {finish_reason}')

                    return ' Кажется возникла неизвестная ошибка, попробуйте позже '

                else:
                    logging.exception(f'Error TextInput: блок else ')

                    return ' Кажется возникла ошибка, попробуйте позже '



            try:
                string = response['candidates'][0]['content']['parts'][0]['text']

                def replace_text(string):

                    string_rep = quote_html(string)

                    # print('------------------------------------------------------------')
                    # pattern_lang = r"```(.*?)\n"
                    # pattern_tag = r"```.+\n"
                    #
                    # match = re.search(pattern_lang, string)
                    # if match:
                    #     result = match.group(1)
                    #     new_string = re.sub(pattern_tag, f'<pre language="{result}">\n', string)
                    #     # print(new_string.replace('```', '</pre>'))
                    #     return new_string.replace('```', '</pre>')
                    # else:
                    #     return string
                    return re.sub(r"```(\w+)", r"<pre>", string_rep).replace('```', '</pre>')

                return replace_text(
                    transform_html(markdown.markdown(string)).text)
            except Exception as e:
                logging.exception(f'Error TextInput: {e}')

                return ' Кажется возникла ошибка, попробуйте позже '
        elif response.get('error'):
            logging.exception(f'Error TextInput: {response.get("error")["message"]}')

            return ' Кажется возникла ошибка, попробуйте позже '








        elif response.get('promptFeedback'):
            logging.exception(f'Нарушение политики безопасности')

            return ' Нарушение политики безопасности, попробуйте другой запрос'

        else:
            logging.exception(f'Ошибка TextInput')

            return ' Кажется возникла ошибка, попробуйте позже '

        # try:
        #     # return response['candidates'][0]['content']['parts'][0]['text']
        #     string = response['candidates'][0]['content']['parts'][0]['text']
        #
        #     def replace_text(string):
        #         # print(string)
        #         # print('------------------------------------------------------------')
        #         pattern_lang = r"```(.*?)\n"
        #         pattern_tag = r"```.+\n"
        #
        #         match = re.search(pattern_lang, string)
        #         if match:
        #             result = match.group(1)
        #             new_string = re.sub(pattern_tag, f'<pre language="{result}">\n', string)
        #             # print(new_string.replace('```', '</pre>'))
        #             return new_string.replace('```', '</pre>')
        #         else:
        #             return string
        #
        #     return replace_text(
        #         transform_html(markdown.markdown(string)).text)
        #
        # except KeyError:
        #     high_probability_items = [rating for rating in response['promptFeedback']['safetyRatings']]
        #     dict_trans_filters = {'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'Сексуально откровенно',
        #                           'HARM_CATEGORY_HATE_SPEECH': 'Разжигание ненависти',
        #                           'HARM_CATEGORY_HARASSMENT': 'Домогательство',
        #                           'HARM_CATEGORY_DANGEROUS_CONTENT': 'Опасный'}
        #
        #     stage_danger = {'NEGLIGIBLE': 'НЕЗНАЧИТЕЛЬНЫЙ',
        #                     'LOW': 'НИЗКИЙ',
        #                     'MEDIUM': 'СРЕДНИЙ',
        #                     'HIGH': 'ВЫСОКИЙ'}
        #
        #     return '\n\n'.join([
        #         f'{dict_trans_filters[category.get("category")]}:  Уровень  - {stage_danger[category.get("probability")]} '
        #         for category in high_probability_items])
        #
        # except Exception:
        #     print(2342)
        #     return response

        # finally:
        #     return f'Возникла непредвиденная ошибка - '


async def main_text_input(msg: str, params: dict = None):
    # await db.set_bind('postgresql://postgres:24651asd@127.0.0.1/gemini_bot')
    # await db.gino.drop_all()
    # await db.gino.create_all()
    # await Proxy.add_proxy("http://45.4.197.124:8000", "8K58YN", '6km5bA')
    # await Token.add_token('AIzaSyAMpQKMwsGXW_u03oPijFoaPQeIv4K_uKE', "pavel.boy4enko900@gmai.com")

    token = await Token.select_random_token()
    proxy = await Proxy.select_random_proxy()
    a = TextInput(key=token[0], proxy=proxy)

    # return await a.get_answer(msg)
    if params:
        return await a.get_answer(msg, params=params)
    return await a.get_answer(msg)


# asyncio.run(main_text_input('Сгенерируй стартап '))

# params = {
#         'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
#         'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
#         'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
#         'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
#         'temperature': 0.3
#
#     }
# import requests
#
# proxies = {
#     'https': 'http://45.145.57.222:11809'
# }
#
# print(requests.get('https://ipinfo.io', proxies=proxies).json())

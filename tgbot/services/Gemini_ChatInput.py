# -*- coding: utf-8 -*-
import asyncio
import re

import markdown
from aiogram.utils.markdown import quote_html
from sulguk import transform_html
from typing import List
import logging
from tgbot.services.Gemini import BaseAioRequests
from tgbot.services.db_api import db
from tgbot.services.db_api.schemas.data import Token, Proxy


class ChatInput(BaseAioRequests):
    def __init__(self, key: str, proxy: dict, base_url='https://generativelanguage.googleapis.com/v1beta/models', model='gemini-pro',
                 func='generateContent', headers={'Content-Type': 'application/json'}):
        BaseAioRequests.__init__(self, key, proxy, base_url, model, func, headers)

    def make_json(self, msg: List[dict], params=None) -> dict:
        chat_msg = [{"role": list(i.keys())[0], "parts": [{"text": list(i.values())[0]}]} for i in msg]

        if params:

            return {
                "contents": chat_msg,
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
                "contents": chat_msg
            }

    async def get_answer(self, msg: List[dict], params=None) -> str:
        response = await self.get_response(msg, params)



        if response.get('candidates'):
            try:
                string = response['candidates'][0]['content']['parts'][0]['text']

                def replace_text(string):

                    string_rep = quote_html(string)
                    return re.sub(r"```(\w+)", r"<pre>", string_rep).replace('```', '</pre>')



                    
                    # print(string)
                    # print('------------------------------------------------------------')
                    # pattern_lang = r"```(.*?)\n"
                    # pattern_tag = r"```.+\n"
                    #
                    # match = re.search(pattern_lang, string)
                    # if match:
                    #     result = match.group(1)
                    #     new_string = re.sub(pattern_tag, f'<pre>\n', string)
                    #     # print(new_string.replace('```', '</pre>'))
                    #     return new_string.replace('```', '</pre>')
                    # else:


                return replace_text(
                    transform_html(markdown.markdown(string)).text)
            except Exception as e:
                logging.exception(f'Error ChatInput: {e}')

                return ' Кажется возникла ошибка, попробуйте позже или завершите чат'
        elif response.get('error'):
            logging.exception(f'Error ChatInput: {response.get("error")["message"]}')

            return ' Кажется возникла ошибка, попробуйте позже или завершите чат'

        elif response.get('promptFeedback'):
            logging.exception(f'Нарушение политики безопасности')

            return ' Нарушение политики безопасности, попробуйте другой запрос'

        else:
            logging.exception(f'Ошибка ChatInput')

            return ' Кажется возникла ошибка, попробуйте позже  или завершите чат'




        # try:
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
        #         transform_html(markdown.markdown(response['candidates'][0]['content']['parts'][0]['text'])).text)
        #
        #
        #     return response['candidates'][0]['content']['parts'][0]['text']
        # except Exception:
        #     print(response)
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
        #         f'* ** {dict_trans_filters[category.get("category")]} **: ** Уровень ** - {stage_danger[category.get("probability")]} '
        #         for category in high_probability_items])
        #
        # except Exception as e:
        #     return f'Возникла непредвиденная ошибка - {e}'


async def main_chat_input(msg: List[dict], params: dict = None):

    # await db.set_bind('postgresql://postgres:24651asd@127.0.0.1/gemini_bot')
    # await db.gino.drop_all()
    # await db.gino.create_all()
    # await Proxy.add_proxy("http://45.4.197.124:8000", "8K58YN", '6km5bA')
    # await Token.add_token('AIzaSyAMpQKMwsGXW_u03oPijFoaPQeIv4K_uKE', "pavel.boy4enko900@gmai.com")

    token = await Token.select_random_token()
    proxy = await Proxy.select_random_proxy()
    a = ChatInput(key=token[0], proxy=proxy)


    # return await a.get_answer(msg)
    if params:
        return await a.get_answer(msg, params=params)
    return await a.get_answer(msg)


# asyncio.run(main_chat_input([{'user': 'привет'}]))
# params = {
#         'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
#         'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
#         'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
#         'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
#         'temperature': 0.3
#
#     }

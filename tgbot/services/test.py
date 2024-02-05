# -*- coding: utf-8 -*-
import re

import requests
import aiohttp
import asyncio
import markdown


# proxies = {
#     'https': 'http://45.4.197.124:8000/'
# }
#
# print(requests.get('https://ipinfo.io/', proxies=proxies).json())

def asd(**kwargs):
    a = 'Режим чата в ChatGPT - это функция, которая позволяет пользователям общаться с искусственным интеллектом (ИИ) в режиме реального времени. Пользователи могут задавать вопросы, делать запросы и получать ответы от ИИ в виде текста. Режим чата предназначен для того, чтобы сделать взаимодействие с ИИ более естественным и интерактивным.\n\nВот некоторые ключевые особенности режима чата в ChatGPT:\n\n* **Естественный язык:** ИИ в режиме чата понимает и отвечает на вопросы, используя естественный язык. Это означает, что вы можете общаться с ИИ так же, как вы общаетесь с другим человеком.\n* **Интерактивность:** Режим чата позволяет пользователям вести диалог с ИИ. Вы можете задавать дополнительные вопросы, уточнять информацию или менять тему разговора.\n* **Широкий спектр знаний:** ИИ в режиме чата имеет доступ к огромному количеству информации из различных источников. Это позволяет ему отвечать на широкий спектр вопросов, от простых до сложных.\n* **Быстрые ответы:** ИИ в режиме чата обычно отвечает на вопросы очень быстро. Это делает его удобным инструментом для получения быстрых ответов на ваши вопросы.\n\nРежим чата в ChatGPT может быть полезен для различных целей, например:\n\n* **Получение информации:** Вы можете использовать режим чата, чтобы получить информацию по различным темам, таким как история, наука, культура и т.д.\n* **Решение проблем:** Режим чата может помочь вам решить проблемы, связанные с работой, учебой или повседневной жизнью.\n* **Генерация идей:** Режим чата может помочь вам генерировать идеи для творческих проектов, таких как написание рассказов, сочинение музыки или создание произведений искусства.\n* **Обучение:** Режим чата может быть использован для обучения новым языкам, навыкам и знаниям.\n\nРежим чата в ChatGPT - это мощный инструмент, который может быть полезен для различных целей. Он позволяет пользователям общаться с ИИ в естественном и интерактивном режиме, получать быстрые ответы на вопросы и решать различные задачи.'

    # md_text = '[TOC]\n# Title\n**text**'
    html = markdown.markdown(a)
    print(a)
    from sulguk import transform_html

    print(transform_html(html).text)
    print(*kwargs)


# asd(email='werwer', id='234234')

def replace_text(string):
    print(string)
    print('------------------------------------------------------------')
    pattern_lang = r"```(.*?)\n"
    pattern_tag = r"```.+\n"

    match = re.search(pattern_lang, string)
    if match:
        result = match.group(1)
        new_string = re.sub(pattern_tag, f'<pre language="{result}">\n', string)
        print(new_string.replace('```', '</pre>'))
        return new_string.replace('```', '</pre>')
    else:
        return string

        # pattern = r"```.*\n"
        # replacement = "<pre>\n"
        #
        # new_string = re.sub(pattern, replacement, string)
        # return new_string

        # from pathlib import Path
        #
        # directory = Path('/home/lorehunt/PycharmProjects/Gemini/tgbot')
        # print(directory)
        # line_count = 0
        #
        # for f in directory.rglob('*.py'):
        #     if not f.is_file() or not f.exists():
        #         continue
        #
        #     local_count = 0
        #     for line in f.read_text(encoding='utf-8').splitlines():
        #         line = line.strip()
        #         if not line or line.startswith(('#', '"', "'")):
        #             continue
        #         local_count += 1
        #
        #     print(f'{f} - {local_count} ст')
        #     line_count += local_count
        #
        # print("=====================================")
        # print(f"all - {line_count}")
response = {'candidates': [{'content': {'parts': [{'text': '**Доказательство:**\n\n**Шаг 1:**\n\nНачнем с исходного уравнения:\n\n2cos² - 1 = cos² -sin²\n\n**Шаг 2:**\n\nПеренесем все члены в одну сторону уравнения, чтобы получить:\n\n2cos² - cos² = sin² + 1\n\n**Шаг 3:**\n\nУпростим левую часть уравнения:\n\ncos² = sin² + 1\n\n**Шаг 4:**\n\nЗаметим, что sin² + cos² = 1, что является тригонометрическим тождеством. Подставим это тождество в уравнение:\n\ncos² = 1 - cos²\n\n**Шаг 5:**\n\nПеренесем cos² в левую часть уравнения:\n\n2cos² = 1\n\n**Шаг 6:**\n\nРазделим обе части уравнения на 2:\n\ncos² = 1/2\n\n**Шаг 7:**\n\nВозьмем квадратный корень из обеих частей уравнения:\n\ncos = ±√(1/2)\n\n**Шаг 8:**\n\nУпростим выражение под квадратным корнем:\n\ncos = ±√(1/2) = ±(1/√2)\n\n**Шаг 9:**\n\nСгруппируем выражения:\n\ncos = ±(1/√2) = ±(√2/2)\n\n**Шаг 10:**\n\nСледовательно,\n\ncos = √2/2 или cos = -√2/2\n\n**Шаг 11:**\n\nОднако это противоречит исходному уравнению, так как cos не может быть равен как √2/2, так и -√2/2 одновременно.\n\n**Вывод:**\n\nИсходное уравнение 2cos² - 1 = cos² -sin² не имеет действительных решений, следовательно, оно является ложным.'}], 'role': 'model'}, 'finishReason': 'STOP', 'index': 0, 'safetyRatings': [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE'}]}], 'promptFeedback': {'safetyRatings': [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE'}]}}

if response.get('candidates'):

    finish_reason = response.get('candidates')[0].get('finishReason')
    print(finish_reason)
    if finish_reason != 'STOP':
        if finish_reason == 'SAFETY':

            print(' Генерация контента была отменена по соображениям безопасности(нарушение политики безопасности)')
        elif finish_reason == 'MAX_TOKENS':

            print(' Достигнуто максимальное количество токенов, попробуйте другой запрос ')

        elif finish_reason == 'RECITATION':

            print('  Генерация контента была отменена по причине "Цитирования"  ')

        elif finish_reason == 'OTHER':

            print(' Кажется возникла неизвестная ошибка, попробуйте позже ')

        else:

            print(' Кажется возникла ошибка, попробуйте позже ')

    try:
        string = response['candidates'][0]['content']['parts'][0]['text']
        print(432543534)
    except Exception as e:

        print(' Кажется возникла ошибка, попробуйте позже 3534534')

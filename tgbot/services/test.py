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


# text = '''О, это здорово! Python — отличный язык для программирования. Он очень универсален и прост в изучении. Что ты делаешь на Python?```lalala\ndef sort_array(array):\n  """\n  Сортирует массив по возрастанию.\n\n  Args:\n    array: Массив, который нужно отсортировать.\n\n  Returns:\n    Отсортированный массив.\n  """\n\n  # Проверяем, является ли массив пустым или содержит ли он только один элемент.\n  if len(array) <= 1:\n    return array\n\n  # Выбираем опорный элемент.\n  pivot = array[0]\n\n  # Создаем два пустых списка: один для элементов, меньших опорного, а другой для элементов, больших опорного.\n  left = []\n  right = []\n\n  # Перебираем все элементы массива, начиная со второго.\n  for i in range(1, len(array)):\n    # Если элемент меньше опорного, добавляем его в список меньших элементов.\n    if array[i] < pivot:\n      left.append(array[i])\n    # Иначе добавляем его в список больших элементов.\n    else:\n      right.append(array[i])\n\n  # Рекурсивно сортируем оба списка.\n  left = sort_array(left)\n  right = sort_array(right)\n\n  # Возвращаем отсортированный массив, объединив отсортированные списки меньших и больших элементов и добавив опорный элемент в середину.\n  return left + [pivot] + right\n```'''
# new_text = replace_text(text)
# print(new_text)
from pathlib import Path

directory = Path(r'C:\Users\PAJILOY PAVUK\PycharmProjects\GeminiAiBot\tgbot')
line_count = 0

for f in directory.rglob('*.py'):
    if not f.is_file() or not f.exists():
        continue

    local_count = 0
    for line in f.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        # if not line or line.startswith(('#', '"', "'")):
        #     continue
        local_count += 1

    print(f'{f} - {local_count} ст')
    line_count += local_count

print("=====================================")
print(f"all - {line_count}")
# async def main():
#     async with aiohttp.ClientSession() as session:
#         # proxy_auth = aiohttp.BasicAuth('rb3V6g7j', 'Qw9dYird')
#         async with session.post('https://ipinfo.io', proxy="http://45.147.103.212:8000") as resp:
#             # f = open('d.txt', 'w')
#             # f.write(await resp.text())
#             a = await resp.text()
#             print(a[:900])
#
# asyncio.run(main())

# -*- coding: utf-8 -*-

# print("```python\ndef calculate_income_tax(gross_income, tax_bracket):\n  \"\"\"Calculates the income tax for a given gross income and tax bracket.\n\n  Args:\n    gross_income: The gross income of the taxpayer.\n    tax_bracket: The tax bracket of the taxpayer.\n\n  Returns:\n    The income tax owed by the taxpayer.\n  \"\"\"\n\n  # Check if the gross income is valid.\n  if gross_income \u003c 0:\n    raise ValueError(\"Gross income cannot be negative.\")\n\n  # Check if the tax bracket is valid.\n  if tax_bracket not in [1, 2, 3, 4, 5]:\n    raise ValueError(\"Invalid tax bracket.\")\n\n  # Calculate the taxable income.\n  taxable_income = gross_income\n\n  # Calculate the income tax.\n  if tax_bracket == 1:\n    income_tax = taxable_income * 0.10\n  elif tax_bracket == 2:\n    income_tax = taxable_income * 0.12\n  elif tax_bracket == 3:\n    income_tax = taxable_income * 0.22\n  elif tax_bracket == 4:\n    income_tax = taxable_income * 0.24\n  elif tax_bracket == 5:\n    income_tax = taxable_income * 0.32\n\n  # Return the income tax.\n  return income_tax\n\n\ndef main():\n  \"\"\"Gets the gross income and tax bracket from the user and calculates the income tax.\"\"\"\n\n  # Get the gross income from the user.\n  gross_income = float(input(\"Enter your gross income: \"))\n\n  # Get the tax bracket from the user.\n  tax_bracket = int(input(\"Enter your tax bracket (1-5): \"))\n\n  # Calculate the income tax.\n  income_tax = calculate_income_tax(gross_income, tax_bracket)\n\n  # Print the income tax.\n  print(f\"Your income tax is {income_tax}\")\n\n\nif __name__ == \"__main__\":\n  main()\n```")
from typing import List

import aiohttp
import asyncio


# import nest_asyncio
# nest_asyncio.apply()


class BaseAioRequests(object):
    def __init__(self, key: str, proxy: dict, base_url='https://generativelanguage.googleapis.com/v1beta/models',
                 model='gemini-pro', func='generateContent', headers={'Content-Type': 'application/json'}):
        self.base_url = base_url
        self.proxy = proxy
        self.model = model
        self.func = func
        self.headers = headers
        self.key = key

    def make_json(self, msg: str, is_chat=False, params=None) -> dict:
        if is_chat:
            pass
        else:
            return {
                "contents": [
                    {"parts": [{"text": msg}]}
                ]
            }

    def make_url(self) -> str:
        return f'{self.base_url}/{self.model}:{self.func}?key={self.key}'

    async def get_response(self, msg: str, params=None) -> dict:
        json = self.make_json(msg, params)
        url = self.make_url()
        async with aiohttp.ClientSession() as session:
            proxy_auth = aiohttp.BasicAuth(self.proxy.get('login'), self.proxy.get('password'))
            async with session.post(url, headers=self.headers, json=json, proxy=self.proxy.get('proxy'),
                                    proxy_auth=proxy_auth) as resp:
                return await resp.json()
#
#

# async def main():
#     async with aiohttp.ClientSession() as session:
#         # proxy_auth = aiohttp.BasicAuth('7MaZfy', 'tHSbnG')
#         async with session.post('https://ipinfo.io', proxy="https://45.147.103.212:8000") as resp:
#             print(await resp.json())
#
# asyncio.run(main())

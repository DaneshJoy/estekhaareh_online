import random
import requests as req
from bs4 import BeautifulSoup

odd_page_numbers = range(1, 604, 2)
page_number = random.choice(odd_page_numbers)

url = f'https://www.aviny.com/%D8%A7%D8%B3%D8%AA%D8%AE%D8%A7%D8%B1%D9%87/{page_number}'
page = req.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

fields = soup.find_all('div', class_='field')

results = []
for field in fields:
    content = None
    field_label = field.find('div', class_='field__label')
    field_item = field.find('div', class_='field__item')
    field_number = field.find('input', {"id": "goestekhare-page"})
    if field_number:
        content = f"{field_label.text.strip()}: {field_number.get('value')}"
    elif field_label:
        if 'سوره' in field_label.text:
            sooreh = field_item.text.split('(')[1].split(')')[0]
        if 'آیه' in field_label.text:
            ayeh = field_item.text.strip()
        content = f"{field_label.text.replace(':', '').strip()}: {field_item.text.strip()}"
    if content:
        print(content)
        results.append(content)


translate_url = f"https://www.aviny.com/soore/{sooreh}?ayeh={ayeh}"
translate_page = req.get(translate_url)
translate_soup = BeautifulSoup(translate_page.text, 'html.parser')
translates = translate_soup.find('div', class_='field-content')
translate_selected = 'ترجمه: ' + translates.find_all('p')[int(ayeh)].text.strip()
results.append(translate_selected)
print(translate_selected)

import tkinter as tk
from tkinter import messagebox

#%%
import webbrowser
import os

# HTML content
html_results = ''
for item in results:
    html_results += f"        <p>{item}</p>\n"
    
html_content = f"""
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پیام</title>
    <style>
        body {{
            direction: rtl;
            text-align: right;
            font-family: Tahoma, Arial, sans-serif;
        }}
        .message-box {{
            border: 1px solid #ccc;
            padding: 20px;
            margin: 20px auto;
            max-width: 400px;
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="message-box">
        {html_results}
    </div>
</body>
</html>
"""

# Save the HTML content to a temporary file
file_path = os.path.join(os.getcwd(), "result.html")
with open(file_path, "w", encoding="utf-8") as file:
    file.write(html_content)

# Open the HTML file in the default web browser
webbrowser.open(f"file://{file_path}")


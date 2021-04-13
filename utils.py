from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests


def get_html(url: str) -> str:
    "Функция, которая идет по URL и забирает оттуда html-страничку"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_urls(url: str) -> tuple:
    urls = {}
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    companies = soup.find('body').find('div', class_='container')


def parse_html(html: str) -> 'DataFrame':
    if not html:
        return False
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table table-hover').find('tbody').findAll('tr')

    table_list = []
    for row in table:
        row_list = []
        for elem in row.findAll('td')[1:]:
            row_list.append(elem.text)
        table_list.append(row_list)
    
    dividents_data = pd.DataFrame(
        np.array(table_list, dtype=object), 
        columns=['Купить до', 'Реестр', 'Дата выплаты', 'Период', 'Дивиденд, руб', 'Доходность, %', 'Цена на закрытии, руб']
    )
    return dividents_data


def write_dividents_data_to_excel(dividents_data: 'DataFrame', file_name: str, sheetname: str):
    dividents_data.to_excel(file_name, sheetname=sheetname)


def edit_dividents_data(dividents_data):
    for idx in range(len(dividents_data)):
        dividents_data['Дивиденд, руб'][idx] = dividents_data['Дивиденд, руб'][idx].replace(',', '.')
        dividents_data['Доходность, %'][idx] = dividents_data['Доходность, %'][idx].replace(',', '.')
        dividents_data['Цена на закрытии, руб'][idx] = dividents_data['Цена на закрытии, руб'][idx].replace(',', '.')
        try:
            dividents_data['Период'][idx] = int(dividents_data['Период'][idx].split()[-1])
            dividents_data['Дивиденд, руб'][idx] = float(dividents_data['Дивиденд, руб'][idx].split()[0])
            dividents_data['Доходность, %'][idx] = float(dividents_data['Доходность, %'][idx][:-1])
            dividents_data['Цена на закрытии, руб'][idx] = float(dividents_data['Цена на закрытии, руб'][idx].split()[0])
        except IndexError:
            pass
    return dividents_data

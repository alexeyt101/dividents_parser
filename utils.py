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


def get_companies_urls(url: str) -> tuple:
    companies_urls = {}
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        companies = soup.find('body').findAll('div', class_='container')[1].findAll('tr', class_='filtered')
        for company in companies:
            company_name = company.find('td')['data-order']
            company_url = company.find('a', class_='d-flex align-items-center')['href']
            companies_urls[company_name] = company_url
        return companies_urls
    return False


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


def save_result_data(writer: 'XlsxWriter object', sheet_name: str, dividents_data: 'DataFrame'):
    '''Функция, которая сохраняет обработанные данные в exel-файл'''
    dividents_data.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    header_format = workbook.add_format({
                                        'bold': True,
                                        'text_wrap': True,
                                        'valign': 'top',
                                        'fg_color': '#D7E4BC',
                                        'border': 1
                                        })
    header_format.set_align('center')
    header_format.set_align('vcenter')
    worksheet.set_column('A:P', 13)
    for col_num, value in enumerate(dividents_data.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)


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
        except (IndexError, ValueError):
            pass
    return dividents_data

import pandas as pd

from utils import edit_dividents_data, get_companies_urls, get_html, parse_html, save_result_data
from config import BASE_URL


def main_func():
    count = 0
    companies_urls = get_companies_urls(BASE_URL)
    try:
        writer = pd.ExcelWriter('test_output_file.xlsx', engine='xlsxwriter')
    except PermissionError:
        print('Закройте файл результатов')
    for company_name, url in companies_urls.items():
        if count > 2: # Ограничение по количеству запросов (потом убрать)
            break
        html = get_html(url)
        dividents_data = parse_html(html)
        dividents_data = edit_dividents_data(dividents_data)
        dividents_data.to_excel(writer, sheet_name=company_name)
        count += 1
    writer.close()


if __name__ == '__main__':
    main_func()

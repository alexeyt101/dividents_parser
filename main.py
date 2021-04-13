from utils import get_html, parse_html, write_dividents_data_to_excel
from config import BASE_URL


def main_func():
    html = get_html(BASE_URL)
    dividents_data = parse_html(html)
    print(dividents_data)
    write_dividents_data_to_excel(dividents_data, 'test_output_file.xlsx')


if __name__ == '__main__':
    main_func()
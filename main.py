from gspread import Spreadsheet
from core import client_init_json, get_table_by_url, get_worksheet_info
from config import settings
from typing import List, Dict
from collections import defaultdict
from pprint import pprint
import interface as ui


def extract_data_from_sheet(table: Spreadsheet, sheet_name: str) -> List[Dict]:
    """
    Извлекает данные из указанного листа таблицы Google Sheets и возвращает список словарей.

    :param table: Объект таблицы Google Sheets (Spreadsheet).
    :param sheet_name: Название листа в таблице.
    :return: Список словарей, представляющих данные из таблицы.
    """
    worksheet = table.worksheet(sheet_name)
    rows = worksheet.get_all_records()
    rating = {}
    for row in rows:
        jury = row['Кто вы?']
        for key, value in row.items():
            if not '|' in key:
                continue

            criterion, film_name = key.split(' | ')

            rating[film_name] = rating.get(film_name, defaultdict(list))
            rating[film_name][criterion] += [{'jury': jury, 'value': value}]
            
    return rating


def main():
    # Создаем клиента и открываем таблицу
    client = client_init_json(settings.credentials_path)
    table = get_table_by_url(client, settings.table_url)
    
    # Извлекаем данные из листа
    data = extract_data_from_sheet(table, settings.worksheet_name)
    pprint(data)

    ui.plot_average_scores(data)
    ui.plot_radar_chart(data)
    ui.plot_overall_average_scores(data)
    ui.plot_pie_charts_comparison(data)

    ui.generate_md_report_with_graphs()



if __name__ == '__main__':
    main()
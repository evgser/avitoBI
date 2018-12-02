import pandas as pd
import avito_handler as ah
from datetime import datetime

import csv

if __name__ == '__main__':

    # Выводим время начала работы программы
    print(datetime.now())

    users_file_1 = 'csv_db/part 3 new 1.csv'
    users_file_2 = 'csv_db/part 3 new 2.csv'

    # Задаём файлы для обработки
    #users_file = 'csv_db/part 3 new.csv'
    support_file = 'csv_db/part 2.1 new.csv'

    # Создаём DataFrame по каждому файлу
    #users_df = pd.read_csv(users_file)
    support_df = pd.read_csv(support_file)

    # Задаём среднюю дельта-средних пользователей при положительных оценках поддержки
    g_delta_met = 0.678469

    # Создаём DataFrame пользователей часть 1
    users_df_1 = pd.read_csv(users_file_1)

    # Создаём обработчик пользователей часть 1
    met = ah.HandlerOfUsersBigData(users_df_1, support_df)

    # Получаем метрики пользователей часть 1
    user_count, except_value_count, lost_items, lost_users = met.handler_user_df(g_delta_met)

    del met
    del users_df_1

    # Создаём DataFrame пользователей часть 2
    users_df_2 = pd.read_csv(users_file_2)

    # Создаём обработчик пользователей часть 2
    met_2 = ah.HandlerOfUsersBigData(users_df_2, support_df)

    # Получаем метрики пользователей часть 2
    user_count_2, except_value_count_2, lost_items_2, lost_users_2 = met_2.handler_user_df(g_delta_met)

    user_count += user_count_2
    except_value_count += except_value_count_2
    lost_items += lost_items_2
    lost_users += lost_users_2

    print('Все пользователи: ', user_count)
    print('Количество пользователей с обращениями больше 1: ', except_value_count)
    print('Процент обработанных записей: ', 1 - (except_value_count / user_count))

    print('Количество потерянных пользователей: ', lost_users)
    print('Количество потерянных объявлений: ', lost_items)

    # Выводим время завершения программы
    print(datetime.now())

import pandas as pd
import numpy as np
from multiprocessing import Pool


class HandlerOfUsers:

    def __init__(self, item_df, support_df):
        self.item_df = item_df
        self.support_df = support_df

    def handler_specific_interval(self):
        """Здесь будет обработчик особых случаев обращения в поддержку"""
        pass

    def get_support_time(self, user_id):
        """Выделяем время обращения в поддержку"""

        # Сортируем время обращения пользователя в поддержку
        sdf_for_user = self.support_df[self.support_df.user_id == user_id].sort_values(by='activity_start_dt')

        # Инициализируем список для записи времени обращения в поддержку
        support_time_list = []

        # Заполняем список временем обращения в поддержку
        for i in range(sdf_for_user['activity_start_dt'].count()):
            support_time_list.append(sdf_for_user.iloc[i][2])

        return support_time_list

    def item_counter(self, user_id):
        """Считаем количество объявлений пользователя в месяц по периодам"""

        # Инициализируем словарь для подсчёта количество объявлений пользователя в месяц
        count_month_dict = {}

        # Заполняем словарь
        for item_date in self.item_df[self.item_df.user_id == user_id]['item_starttime']:
            year, month, remainder = item_date.split('-')
            title = year + '-' + month
            if title in count_month_dict.keys():
                count_month_dict.update({title: count_month_dict[title] + 1})
            else:
                count_month_dict.update({title: 1})

        return count_month_dict

    def convert_to_ts(self, count_month_dict):
        """Функция преобразует количество объявлений пользователя за месяц в временной ряд"""

        # Находим первое и последнее объявление пользователя
        min_item_date = min(count_month_dict.keys())
        max_item_date = max(count_month_dict.keys())

        # Создаем временной интервал от первого до последнего объявления пользователя
        rng = pd.date_range(min_item_date, max_item_date, freq='M')

        # Инициализируем пустой список для количества объявлений в месяц
        data_for_ts = []

        # Заполняем список данных
        for i in rng:
            y = str(i.year)
            if i.month < 10:
                m = '0' + str(i.month)
            else:
                m = str(i.month)
            if y + '-' + m in count_month_dict.keys():
                data_for_ts.append(count_month_dict[y + '-' + m])
            else:
                data_for_ts.append(0)

        # Преобразуем временной интервал и данные в временной ряд
        ts = pd.Series(data_for_ts, rng)

        return ts

    def group_by_section(self, ts, support_time_list):
        """Разбивка объявлений на группы до/после обращения в поддержку"""

        # Инициализируем список временных чекпоинтов
        interval_time_list = [ts.index[0]]
        # Инициализируем список временных интервалов
        interval_list = []

        # Выделяем промежутки времени между первым объявленем, обращением в поддержку и последним объявлением
        for i in range(len(support_time_list)):
            interval_time_list.append(support_time_list[i])
            interval_list.append(ts[interval_time_list[i]:interval_time_list[i + 1]])

        interval_list.append(ts[interval_time_list[len(interval_time_list) - 1]:ts.index[ts.count() - 1]])

        return interval_list

    def solve_metrics(self, interval_list):
        """???"""

        x = interval_list[0].median()
        y = interval_list[1].median()

        # Проверки на 'nan'
        # Если нету объявлений "до" обращения в поддержку
        if x != x:
            x = 0

        # Если нету объявлений "после" обращения в поддержку
        if y != y:
            y = 0

        # Многомерный случай на будущее

        # Инициализируем список для результатов вычисления метрик
        # result_list = []
        # for i in range(len(interval_list)):
        #    result_list.append(interval_list[i].median())
        #    if result_list[i] != result_list[i]:
        #        result_list[i] = 0

        return y - x

    def handler_user_df(self):
        """Функция обрабатывает данные по объявлениям для каждого пользователя

        1. Получаем время обращения в поддержку
        2. Преобразуем данные во временной ряд
        3. Разбиваем объявления на группы до/после
        4. Считаем кол-во объявлений пользователя за месяц по периодам
        5. Считаем метрики пользователя до и после обращения в поддержку

        """

        pool = Pool()  # создаём бассейн, в котором будут купаться наши данные
        #us_id = "49\xa0500\xa0593"
        #print(self.item_df[self.item_df.user_id == us_id]['item_starttime'])
        #print(self.support_df[self.support_df.user_id == us_id]['activity_start_dt'])

        # Многопоточно и асинхронно обрабатываем данные
        metrics_list = list(pool.map(self.handler_for_each_user_df, pd.unique(self.item_df['user_id'])))

        pool.close()  # закрываем бассейн, он нам больше не нужен
        pool.join()  # возвращаемся в реальный мир

        x = metrics_list.count('Bad_data')
        print('Количество пользователей с обращениями больше 1: ', x)

        while 'Bad_data' in metrics_list:
                metrics_list.remove('Bad_data')

        print('Медиана дельты: ', np.median(metrics_list))
        print('Средняя дельты: ', np.average(metrics_list))

        return np.average(metrics_list)

    def handler_for_each_user_df(self, user_id):

        # Поолучаем время обращения в поддержку
        support_time = self.get_support_time(user_id)

        met = 'Bad_data'

        # Учитываем только случаи, когда человек обращался в поддержку один раз
        if len(support_time) == 1:

            # Считаем кол-во объявлений пользователя за месяц
            count_month_dict = self.item_counter(user_id)

            # Преобразуем данные в временной ряд
            ts = self.convert_to_ts(count_month_dict)

            if ts.count() != 0:

                #
                interval_list = self.group_by_section(ts, support_time)

                #
                met = self.solve_metrics(interval_list)

                if met != met:
                    print(user_id)

        return met

    # if user_id == "5\xa0800":
    #   break
        #print(self.item_df[self.item_df.user_id == "5\xa0800"]['item_starttime'])
        #print(self.support_df[self.support_df.user_id == "5\xa0800"]['activity_start_dt'])
        #print(self.support_df[self.support_df.user_id == "5\xa0800"]['ticket_subcategory'])
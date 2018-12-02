import pandas as pd
import numpy as np
from multiprocessing import Pool, Process, Queue, current_process


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

        interval_list = [ts[ts.index[0]:support_time_list[0]],
                         ts[support_time_list[0]:ts.index[ts.count() - 1]]]

        return interval_list

    def solve_metrics(self, interval_list):
        """Функция считает метрики пользователя до и после"""

        # Инициализируем метрики до и после нулевыми значениями, если попадется пустой временной ряд
        med_before, med_after, avg_before, avg_after = [0, 0, 0, 0]

        # Если временной ряд не пуст, вычисляем метрики до
        if interval_list[0].count() != 0:

            # Считаем медиану кол-ва объявлений до
            med_before = interval_list[0].median()

            # Считаем среднее значение кол-ва объявлений до
            avg_before = np.average(interval_list[0])

        # Если временной ряд не пуст, вычсиляем метрики после
        if interval_list[1].count() != 0:

            # Считаем медиану кол-ва объявлений после
            med_after = interval_list[1].median()

            # Считаем среднее значение кол-ва объявлений после
            avg_after = np.average(interval_list[1])

        # Считаем дельту медиан и среднего
        delta_med = med_after - med_before
        delta_avg = avg_after - avg_before

        return delta_med, delta_avg

    def handler_user_df(self):
        """Функция обрабатывает данные по объявлениям для каждого пользователя

        1. Получаем время обращения в поддержку
        2. Преобразуем данные во временной ряд
        3. Разбиваем объявления на группы до/после
        4. Считаем кол-во объявлений пользователя за месяц по периодам
        5. Считаем метрики пользователя до и после обращения в поддержку

        """

        pool = Pool()  # создаём бассейн, в котором будут купаться наши данные

        # Многопоточно и асинхронно обрабатываем данные
        metrics_list = list(pool.map(self.handler_for_each_user_df, pd.unique(self.item_df['user_id'])))

        pool.close()  # закрываем бассейн, он нам больше не нужен
        pool.join()  # возвращаемся в реальный мир

        user_count = len(pd.unique(self.item_df['user_id']))
        except_value_count = metrics_list.count('except_value')
        print('Все пользователи: ', user_count)
        print('Количество пользователей с обращениями больше 1: ', except_value_count)
        print('Процент обработанных записей: ', 1 - (except_value_count / user_count))

        while 'except_value' in metrics_list:
                metrics_list.remove('except_value')

        med_list = []
        avg_list = []
        for i in range(len(metrics_list)):
            med_list.append(metrics_list[i][0])
            avg_list.append(metrics_list[i][1])

        print('Средняя дельт-медиан: ', np.average(med_list))
        print('Средняя дельт-срдедних: ', np.average(avg_list))

    def handler_for_each_user_df(self, user_id):

        # Поолучаем время обращения в поддержку
        support_time = self.get_support_time(user_id)

        delta = 'except_value'

        # Учитываем только случаи, когда человек обращался в поддержку один раз
        if len(support_time) == 1:

            # Считаем кол-во объявлений пользователя за месяц
            count_month_dict = self.item_counter(user_id)

            # Преобразуем данные в временной ряд
            ts = self.convert_to_ts(count_month_dict)

            if ts.count() != 0:

                # Разделяем временной ряд на промежутки до и после обращения
                interval_list = self.group_by_section(ts, support_time)

                # Считаем метрики пользователя
                delta = self.solve_metrics(interval_list)

        return delta


class HandlerOfUsersBigData(HandlerOfUsers):

    def solve_metrics(self, interval_list):
        """Функция считает метрики пользователя до и после"""

        # Инициализируем метрики до и после нулевыми значениями, если попадется пустой временной ряд
        avg_before, avg_after = [0, 0]

        # Если временной ряд не пуст, вычисляем метрики до
        if interval_list[0].count() != 0:

            # Считаем среднее значение кол-ва объявлений до
            avg_before = np.average(interval_list[0])

        # Если временной ряд не пуст, вычсиляем метрики после
        if interval_list[1].count() != 0:

            # Считаем среднее значение кол-ва объявлений после
            avg_after = np.average(interval_list[1])

        # Считаем дельту медиан и среднего
        delta_avg = avg_after - avg_before
        print(avg_after)
        return delta_avg, avg_after

    def handler_for_each_user_df(self, user_id):

        # Поолучаем время обращения в поддержку
        support_time = self.get_support_time(user_id)

        delta = 'except_value'

        # Учитываем только случаи, когда человек обращался в поддержку один раз
        if len(support_time) == 1:

            # Считаем кол-во объявлений пользователя за месяц
            count_month_dict = self.item_counter(user_id)

            # Преобразуем данные в временной ряд
            ts = self.convert_to_ts(count_month_dict)
            del count_month_dict

            if ts.count() != 0:

                # Разделяем временной ряд на промежутки до и после обращения
                interval_list = self.group_by_section(ts, support_time)
                del ts

                # Считаем метрики пользователя
                delta = self.solve_metrics(interval_list)
                del interval_list

        return delta

    def handler_user_df(self, g_delta_met):
        """Функция обрабатывает данные по объявлениям для каждого пользователя

        1. Получаем время обращения в поддержку
        2. Преобразуем данные во временной ряд
        3. Разбиваем объявления на группы до/после
        4. Считаем кол-во объявлений пользователя за месяц по периодам
        5. Считаем метрики пользователя до и после обращения в поддержку

        """

        lost_users = 0
        lost_items = 0

        pool = Pool()
        metrics_list = list(pool.map(self.handler_for_each_user_df, pd.unique(self.item_df['user_id'])))
        pool.close()  # закрываем бассейн, он нам больше не нужен
        pool.join()  # возвращаемся в реальный мир

        except_value_count = metrics_list.count('except_value')

        while 'except_value' in metrics_list:
            metrics_list.remove('except_value')

        for j in range(len(metrics_list)):
            if metrics_list[j][0] < g_delta_met:
                lost_items += metrics_list[j][0] + g_delta_met
                if metrics_list[j][1] == 0:
                    lost_users += 1

        del metrics_list

        user_count = len(pd.unique(self.item_df['user_id']))

        return user_count, except_value_count, lost_items, lost_users

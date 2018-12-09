import pandas as pd
import numpy as np
from multiprocessing import Pool


class CriteriaHandler:
    """Обработчик критерия эффективности службы поддержки"""

    def __init__(self, users_df, support_df):
        self.users_df = users_df
        self.support_df = support_df

    def get_support_time(self, user_id):
        """Выделяем время обращения пользователя в поддержку"""

        return self.support_df[self.support_df.user_id == user_id].iloc[0][1]

    def item_counter(self, user_id):
        """Считаем количество объявлений пользователя в месяц

        На выходе получаем словарь, в котором:
        Ключи - год и месяц публикации объявления
        Значения - количество объявлений за год и месяц в ключе словаря
        """

        # Инициализируем словарь для подсчёта количество объявлений пользователя в месяц
        count_month_dict = {}

        # Заполняем словарь
        for item_date in self.users_df[self.users_df.user_id == user_id]['item_starttime']:

            # Узнаём год и месяц публикации объявления
            year, month, remainder = item_date.split('-')

            # Очищаем ненужное
            del remainder

            # Ключ словаря - год и месяц
            title = year + '-' + month

            if title in count_month_dict.keys():
                count_month_dict.update({title: count_month_dict[title] + 1})
            else:
                count_month_dict.update({title: 1})

        return count_month_dict

    @staticmethod
    def convert_to_ts(count_month_dict, support_time):
        """Функция преобразует количество объявлений пользователя по месяцам во временной ряд

        Функция возвращает 2 временных ряда:
        1. Количество объявлений пользователя по месяцам до обращения в поддержку
        2. Количество объявлений пользователя по месяцам после обращения в поддержку
        """

        # Находим первое и последнее объявление пользователя

        min_item_date = min(count_month_dict.keys())
        max_item_date = max(count_month_dict.keys())

        # Создаем временной интервал от первого объявления пользователя до обращения в поддержку
        time_rng_before = pd.date_range(min_item_date, support_time, freq='M')

        # Создаём временной интервал от обращения в поддержку до последнего объявления пользователя
        time_rng_after = pd.date_range(support_time, max_item_date, freq='M')
        time_rng_after = time_rng_after[1:]

        # Инициализируем пустой список для количества объявлений в месяц
        ts_data_before = []
        ts_data_after = []

        # Заполняем список данных от первого объявления пользователя до обращения в поддержку
        for i in time_rng_before:
            y = str(i.year)
            if i.month < 10:
                m = '0' + str(i.month)
            else:
                m = str(i.month)
            if y + '-' + m in count_month_dict.keys():
                ts_data_before.append(count_month_dict[y + '-' + m])
            else:
                ts_data_before.append(0)

        # Заполняем список данных от обращения в поддержку до последнего объявления пользователя
        for i in time_rng_after:
            y = str(i.year)
            if i.month < 10:
                m = '0' + str(i.month)
            else:
                m = str(i.month)
            if y + '-' + m in count_month_dict.keys():
                ts_data_after.append(count_month_dict[y + '-' + m])
            else:
                ts_data_after.append(0)

        # Преобразуем временной интервал и данные в временной ряд
        ts_before = pd.Series(ts_data_before, time_rng_before)
        ts_after = pd.Series(ts_data_after, time_rng_after)

        return [ts_before, ts_after]

    @staticmethod
    def metrics_calculation(interval_list):
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

        # Считаем дельту среднего
        delta_avg = avg_after - avg_before

        return delta_avg

    def handler_for_each_user(self, user_id):
        """Функция обрабатывает данные для каждого отдельного пользователя

        Алгоритм работы:
        1. Получаем время обращения в поддержку
        2. Получаем оценку службы поддержки, которую поставил пользователь
        3. Считаем кол-во объявлений пользователя за каждый месяц
        4. Преобразуем данные во временные ряды до и после обращения в службу поддержки
        5. Считаем метрики пользователя до и после обращения в поддержку
        """

        # Поолучаем время обращения в поддержку
        support_time = self.get_support_time(user_id)

        # Получаем оценку службы поддержки
        support_rate = self.support_df[self.support_df.user_id == user_id].iloc[0][2]

        # Считаем кол-во объявлений пользователя за месяц
        count_month_dict = self.item_counter(user_id)

        # Преобразуем данные в временной ряд
        interval_list = self.convert_to_ts(count_month_dict, support_time)

        delta = self.metrics_calculation(interval_list)

        return support_rate, delta

    def users_handler(self):
        """Функция параллельно обрабатывает данные всех пользователей

        Алгоритм работы:

        """

        pool = Pool()  # создаём бассейн, в котором будут купаться наши данные

        # Многопоточно и асинхронно обрабатываем данные
        metrics_list = list(pool.map(self.handler_for_each_user, self.support_df['user_id']))

        pool.close()  # закрываем бассейн, он нам больше не нужен
        pool.join()  # возвращаемся в реальный мир

        user_count = len(pd.unique(self.users_df['user_id']))
        print('Все пользователи: ', user_count)

        return metrics_list

    @staticmethod
    def transform_metrics_to_dict(metrics_list):

        metrics_dict = {}
        for i in range(len(metrics_list)):
            if metrics_list[i][0] in metrics_dict.keys():
                sub_list = metrics_dict[metrics_list[i][0]]
                sub_list.append(metrics_list[i][1])
                metrics_dict.update({metrics_list[i][0]: sub_list})
            else:
                sub_list = [metrics_list[i][1]]
                metrics_dict.update({metrics_list[i][0]: sub_list})

        return metrics_dict

class HandlerOfUsersBigData(CriteriaHandler):

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

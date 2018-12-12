import matplotlib.pyplot as plt
import numpy as np
import copy
import operator


class AvitoDraw:

    def __init__(self, data_dict):

        self.data_dict = data_dict
        self.data_filter(500)

        self.rate = ['Неудовлетворительно', 'Удовлетворительно', 'Нейтрально', 'Хорошо', 'Отлично']
        self.short_rate = ['Неуд.', 'Удов.', 'Нейт.', 'Хор.', 'Отл.']

    def data_filter(self, edge):
        """ Функция фильтруем дельта значения пользователей, убирая выбросы """

        for key in self.data_dict.keys():

            sub_list = self.data_dict[key]

            i = 0
            while i < len(sub_list):
                if float(sub_list[i]) > edge or float(sub_list[i]) < - edge:
                    del sub_list[i]
                else:
                    i += 1

            self.data_dict.update({key: sub_list})

    def random_set(self):
        """ Функция генерирует рандомную выборку из дельта значений пользователей"""

        random_data_dict = copy.deepcopy(self.data_dict)

        for key in random_data_dict.keys():

            sub_list = random_data_dict[key]

            i = 0
            d = 0
            while i < len(sub_list) - d:
                if 0.8 + np.random.rand() < 1:
                    del sub_list[i]
                    d += 1
                else:
                    i += 1

            random_data_dict.update({key: sub_list})

        return random_data_dict

    def print_average(self, all_data):
        """ Выводим средние дельта-значений по оценкам """
        for i in range(len(all_data)):
            print(self.rate[i] + ': ' + str(np.average(all_data[i])))

    def fill_data(self, random=False):
        """ Функция собирает массив из дельта значений пользователей

        flag random:
        1. False (default) - заполняем массив всеми данными
        2. True - заполняем массив случайными данными
        """

        if random is True:
            data_dict = self.random_set()
        else:
            data_dict = self.data_dict.copy()

        all_data = [np.array(data_dict['Не удовлетворительно']).astype(np.float),
                    np.array(data_dict['Удовлетворительно']).astype(np.float),
                    np.array(data_dict['Нейтрально']).astype(np.float),
                    np.array(data_dict['Хорошо']).astype(np.float),
                    np.array(data_dict['Отлично']).astype(np.float)]

        return all_data

    def get_random_average(self, count=10, random=True):
        """ Заполняем данные рандомными значениями count раз """

        delta_list = [[] for i in range(5)]
        for i in range(count):

            all_data = self.fill_data(random)

            for j in range(5):
                delta_list[j].append(np.average(all_data[j]))

        return delta_list

    def plot_multi_average(self, count=10):
        """ Строим график средних дельта-значений по рандомным выборкам """

        delta_list = self.get_random_average(count)
        x = [i for i in range(len(delta_list[0]))]

        fig, ax = plt.subplots()
        for i in range(5):
            ax.plot(x, delta_list[i], label=self.short_rate[i])
        ax.legend()

        ax.yaxis.grid(True)
        ax.set_xlabel('Выборки')
        ax.set_ylabel('Среднее дельта-поведения')

        plt.show()

        self.plot_average(delta_list)

    def plot_average(self, delta_list):
        """ Строим график средних по средним значениям рандомных выборок """

        y = [[] for i in range(5)]
        for i in range(5):
            y[i] = [np.average(delta_list[i]) for j in range(len(delta_list[i]))]

        print("Средние дельта-значений по всем пользователям")
        self.print_average(delta_list)

        x = [i for i in range(len(delta_list[0]))]

        fig, ax = plt.subplots()
        for i in range(5):
            ax.plot(x, y[i], label=self.short_rate[i])
        ax.legend()

        ax.yaxis.grid(True)
        ax.set_ylabel('Среднее средних дельта-поведений')

        plt.show()

    def simple_plot(self):
        """ Строим график средних дельта-значения от оценки """

        y = self.get_random_average(1, False)

        x = [i for i in range(len(y))]

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(y))])
        ax.set_xlabel('Оценки пользователей')
        ax.set_ylabel('Средняя дельта-поведения')

        # add x-tick labels
        plt.setp(ax, xticks=[y for y in range(len(y))],
                 xticklabels=self.short_rate)

        plt.show()

    def plot_violin(self):
        """ Строим violin plot, чтобы посмотреть распределение дельта-объявлений в зависимости от оценки """

        all_data = self.fill_data()

        print("Средние по средним дельта-значений рандомных выборок")
        self.print_average(all_data)
        print('\n')

        fig, ax = plt.subplots()

        ax.violinplot(all_data, showmeans=False, showmedians=True)

        # adding horizontal grid lines
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data))])
        ax.set_xlabel('Оценки пользователей')
        ax.set_ylabel('Дельта-поведения')

        # add x-tick labels
        plt.setp(ax, xticks=[y + 1 for y in range(len(all_data))],
                 xticklabels=self.short_rate)

        plt.show()


class AvitoDraw2:

    def __init__(self, all_data):
        self.all_data = all_data

    def data_handler_category(self):
        """ Обрабатываем всю информацию и рисуем по ней графики """

        # Инициализируем переменные для подсчёта количества всех пользователей по собственных категориям
        users = 0
        unhappy_users = 0
        lost_users = 0
        lost_items = 0

        # Инициализируем словари для подсчёта метрик в каждой категории и подкатегории
        users_dict = {}
        sub_users_dict = {}

        unhappy_users_dict = {}
        sub_unhappy_users_dict = {}

        lost_users_dict = {}
        sub_lost_users_dict = {}

        lost_items_dict = {}
        sub_lost_items_dict = {}

        for i in range(len(self.all_data)):

            # Считаем количество людей по категориям и подкатегориям
            if self.all_data[i][2] not in users_dict.keys():

                users_dict.update({self.all_data[i][2]: 1})

                sub_users_dict.update({self.all_data[i][2]: {self.all_data[i][3]: 1}})

            else:
                users_dict.update({self.all_data[i][2]: users_dict[self.all_data[i][2]] + 1})

                if self.all_data[i][3] not in sub_users_dict[self.all_data[i][2]].keys():
                    sub_users_dict[self.all_data[i][2]].update({self.all_data[i][3]: 1})
                else:
                    numb = sub_users_dict[self.all_data[i][2]][self.all_data[i][3]] + 1
                    sub_users_dict[self.all_data[i][2]].update({self.all_data[i][3]: numb})

            # Считаем количество недовольных людей по категориям и подкатегориям
            if float(self.all_data[i][0]) > 0:

                if self.all_data[i][2] not in unhappy_users_dict.keys():
                    unhappy_users_dict.update({self.all_data[i][2]: 1})

                    sub_unhappy_users_dict.update({self.all_data[i][2]: {self.all_data[i][3]: 1}})
                else:
                    unhappy_users_dict.update({self.all_data[i][2]: unhappy_users_dict[self.all_data[i][2]] + 1})

                    if self.all_data[i][3] not in sub_unhappy_users_dict[self.all_data[i][2]].keys():
                        sub_unhappy_users_dict[self.all_data[i][2]].update({self.all_data[i][3]: 1})
                    else:
                        numb = sub_unhappy_users_dict[self.all_data[i][2]][self.all_data[i][3]] + 1
                        sub_unhappy_users_dict[self.all_data[i][2]].update({self.all_data[i][3]: numb})

            # Считаем количество потерянных пользователей и подкатегориям
            if self.all_data[i][1] == "True":
                if self.all_data[i][2] not in lost_users_dict.keys():
                    lost_users_dict.update({self.all_data[i][2]: 1})

                    sub_lost_users_dict.update({self.all_data[i][2]: {self.all_data[i][3]: 1}})
                else:
                    lost_users_dict.update({self.all_data[i][2]: lost_users_dict[self.all_data[i][2]] + 1})

                    if self.all_data[i][3] not in sub_lost_users_dict[self.all_data[i][2]].keys():
                        sub_lost_users_dict[self.all_data[i][2]].update({self.all_data[i][3]: 1})
                    else:
                        numb = sub_lost_users_dict[self.all_data[i][2]][self.all_data[i][3]] + 1
                        sub_lost_users_dict[self.all_data[i][2]].update({self.all_data[i][3]: numb})

            # Считаем количество потерянных объявлений и подкатегориям
            if float(self.all_data[i][0]) > 0:
                if self.all_data[i][2] not in lost_items_dict.keys():
                    lost_items_dict.update({self.all_data[i][2]: float(self.all_data[i][0])})

                    sub_lost_items_dict.update({self.all_data[i][2]: {self.all_data[i][3]: float(self.all_data[i][0])}})
                else:
                    numb = float(self.all_data[i][0]) + lost_items_dict[self.all_data[i][2]]
                    lost_items_dict.update({self.all_data[i][2]: numb})

                    numb_2 = float(self.all_data[i][0])
                    if self.all_data[i][3] not in sub_lost_items_dict[self.all_data[i][2]].keys():
                        sub_lost_items_dict[self.all_data[i][2]].update({self.all_data[i][3]: numb_2})
                    else:
                        numb_3 = sub_lost_items_dict[self.all_data[i][2]][self.all_data[i][3]] + numb_2
                        sub_lost_items_dict[self.all_data[i][2]].update({self.all_data[i][3]: numb_3})

        # Считаем количество пользователей в собственных категориях
        for key in users_dict.keys():
            users += users_dict[key]

            if key in unhappy_users_dict.keys():
                unhappy_users += unhappy_users_dict[key]

            if key in lost_users_dict.keys():
                lost_users += lost_users_dict[key]

            if key in lost_items_dict.keys():
                lost_items += lost_items_dict[key]

        # Выводим информацию по количеству пользователей в собственных категориях
        print("Количество всех обработанных пользователей", users)
        print("Количество недовольных пользователей: ", unhappy_users)
        print("Количество потерянных пользователей: ", lost_users)
        print("Количество потерянных объявлений: ", lost_items)

        # Инициализируем словари отношений
        unhappy_slash_users = {}
        lost_items_slash_users = {}
        lost_items_slash_unhappy = {}

        unhappy_slash_lost_users = {}
        lost_items_slash_lost_users = {}
        lost_users_slash_users = {}

        # Считаем отношения по категориям
        for key in users_dict.keys():

            if key in unhappy_users_dict.keys():

                unhappy_slash_users.update({key: unhappy_users_dict[key] / users_dict[key]})

            if key in lost_items_dict.keys():

                lost_items_slash_users.update({key: lost_items_dict[key] / users_dict[key]})
                lost_items_slash_unhappy.update({key: lost_items_dict[key] / unhappy_users_dict[key]})

                lost_users_slash_users.update({key: lost_users_dict[key] / users_dict[key]})
                unhappy_slash_lost_users.update({key: unhappy_users_dict[key] / lost_users_dict[key]})
                lost_items_slash_lost_users.update({key: lost_items_dict[key] / lost_users_dict[key]})

        # Отрисовываем первый слайд (категории)
        self.double_barh_plot(users_dict, unhappy_users_dict, x=7.9, y=3.4, xlabel='Количество пользователей',
                              legend=('Все пользователи', 'Недовольные пользователи'))
        self.barh_plot(lost_items_dict, x=7.9, y=3.4, xlabel='Количество потерянных объявлений')

        # Отрисовываем первый слайд (отношения)
        self.double_simple_plot(lost_items_slash_users, lost_items_slash_unhappy)
        self.simple_plot(unhappy_slash_users)

        """
        # Отрисовываем первый слайд (подкатегории)
        self.double_barh_plot(sub_users_dict['Блокировки и отклонения'],
                              sub_unhappy_users_dict['Блокировки и отклонения'],
                              x=5.3, y=2, xlabel='Количество пользователей')
        self.barh_plot(sub_lost_items_dict['Блокировки и отклонения'],
                       x=5.3, y=2, xlabel='Количество потерянных объявлений')

        # Отрисовываем первый слайд (подкатегории) - альтернативный сценарий
        self.double_barh_plot(sub_users_dict['Работа с объявлениями и личным кабинетом'],
                              sub_unhappy_users_dict['Работа с объявлениями и личным кабинетом'],
                              xlabel='Количество пользователей')
        self.barh_plot(sub_lost_items_dict['Работа с объявлениями и личным кабинетом'],
                       x=8, xlabel='Количество потерянных объявлений')
        """
        # Отрисовываем второй слайд (категории)
        self.double_barh_plot(users_dict, lost_users_dict, x=10, y=3.4, xlabel='Количество пользователей',
                              legend=('Все пользователи', 'Потерянные пользователи'))

        # Отрисовываем второй слайд (отношения)
        self.simple_plot(lost_users_slash_users)
        self.simple_plot(unhappy_slash_lost_users)
        self.simple_plot(lost_items_slash_lost_users)

    @staticmethod
    def double_barh_plot(data_dict, data_dict_2, x=7.0, y=3.0, xlabel='', title='', legend=()):
        """ Функция отрисовки горизонтального бара с 2 наборами входных переменных

         x - длина полотна
         y - ширина полотна

         """

        fig, ax = plt.subplots()
        # Задаём размер области отрисовки
        fig.set_size_inches(x, y, forward=True)

        # Чистим данные от незначительных обращений
        data_dict = {k: v for k, v in data_dict.items() if v > 10}

        # Сортируем данные для графика
        sorted_list = sorted(data_dict.items(), key=operator.itemgetter(1))

        sorted_list_2 = []
        for i in range(len(sorted_list)):
            if sorted_list[i][0] in data_dict_2.keys():
                sorted_list_2.append((sorted_list[i][0], data_dict_2[sorted_list[i][0]]))
            else:
                sorted_list_2.append((sorted_list[i][0], 0))

        # Формируем данные для графика
        group_names = list(sorted_list[i][0] for i in range(len(sorted_list)))
        group_data = list(sorted_list[i][1] for i in range(len(sorted_list)))
        group_data_2 = list(sorted_list_2[i][1] for i in range(len(sorted_list)))

        # Отрисовываем график
        p1 = ax.barh(group_names, group_data, height=0.4)
        p2 = ax.barh(group_names, group_data_2, height=0.4)

        # Задаём заголовок и подпись, если переданы
        if xlabel != '':
            ax.set_xlabel(xlabel)
        if title != '':
            ax.set_title(title)

        if len(legend) != 0:
            plt.legend((p1[0], p2[0]), legend, loc='lower right')

        plt.show()

    @staticmethod
    def barh_plot(data_dict, x=7.0, y=3.0, xlabel='', title=''):
        """ Функция отрисовки горизонтального бара с 1 набором входных переменных

         x - длина полотна
         y - ширина полотна

         """

        fig, ax = plt.subplots()
        # Задаём размер области отрисовки
        fig.set_size_inches(x, y, forward=True)

        # Чистим данные от незначительных обращений
        data_dict = {k: v for k, v in data_dict.items() if v > 10}

        # Сортируем данные для графика
        sorted_list = sorted(data_dict.items(), key=operator.itemgetter(1))

        # Формируем данные для графика
        group_names = list(sorted_list[i][0] for i in range(len(sorted_list)))
        group_data = list(sorted_list[i][1] for i in range(len(sorted_list)))

        # Отрисовываем график
        ax.barh(group_names, group_data, height=0.4)

        # Задаём заголовок и подпись, если переданы
        if xlabel != '':
            ax.set_xlabel(xlabel)
        if title != '':
            ax.set_title(title)

        plt.show()

    @staticmethod
    def double_simple_plot(lost_items_slash_users, lost_items_slash_unhappy):
        """ Отрисовка потерянных объявлений ко всем пользователям и к недовольным по категориям """

        y1 = [i for i in lost_items_slash_users.values()]
        y2 = [i for i in lost_items_slash_unhappy.values()]

        x = list(lost_items_slash_users.keys())

        print("Пояснение к графикам отношений:")
        for i in range(len(x)):
            print(i, ": ", x[i])

        fig, ax = plt.subplots()
        p1 = ax.plot(x, y1)
        p2 = ax.plot(x, y2)

        ax.yaxis.grid(True)
        ax.set_xlabel('Категория')
        ax.set_ylabel('Отношение')

        # add x-tick labels
        plt.setp(ax, xticks=[x for x in range(len(x))], xticklabels=[i for i in range(len(x))])

        plt.legend((p1[0], p2[0]), ('потерянные объяв./все польз.', 'потерянные объяв./недовольные польз.'), loc='upper right')

        plt.show()

    @staticmethod
    def simple_plot(dict_slash_dict):
        """ Отрисовка отношения недовольных пользователей к довольным по категориям"""

        y = [i for i in dict_slash_dict.values()]

        x = list(dict_slash_dict.keys())

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.yaxis.grid(True)
        ax.set_xlabel('Категория')
        ax.set_ylabel('Отношение')

        # add x-tick labels
        plt.setp(ax, xticks=[x for x in range(len(x))], xticklabels=[i for i in range(len(x))])

        plt.show()

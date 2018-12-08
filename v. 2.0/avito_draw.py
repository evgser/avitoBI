import matplotlib.pyplot as plt
import numpy as np
import copy


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

    def get_random_average(self, count=100, random=True):

        list_1 = []
        list_2 = []
        list_3 = []
        list_4 = []
        list_5 = []
        for i in range(count):

            all_data = self.fill_data(random)

            list_1.append(np.average(all_data[0]))
            list_2.append(np.average(all_data[1]))
            list_3.append(np.average(all_data[2]))
            list_4.append(np.average(all_data[3]))
            list_5.append(np.average(all_data[4]))

        return list_1, list_2, list_3, list_4, list_5

    def plot_multi_average(self):

        list_1, list_2, list_3, list_4, list_5 = self.get_random_average(10)
        x = [i for i in range(len(list_1))]

        fig, ax = plt.subplots()
        ax.plot(x, list_1, label=self.short_rate[0])
        ax.plot(x, list_2, label=self.short_rate[1])
        ax.plot(x, list_3, label=self.short_rate[2])
        ax.plot(x, list_4, label=self.short_rate[3])
        ax.plot(x, list_5, label=self.short_rate[4])
        ax.legend()

        ax.yaxis.grid(True)
        ax.set_xlabel('Выборки')
        ax.set_ylabel('Среднее дельта-поведения')

        plt.show()

        self.plot_average(list_1, list_2, list_3, list_4, list_5)

    def plot_average(self, list_1, list_2, list_3, list_4, list_5):

        y1 = [np.average(list_1) for i in range(len(list_1))]
        y2 = [np.average(list_2) for i in range(len(list_2))]
        y3 = [np.average(list_3) for i in range(len(list_3))]
        y4 = [np.average(list_4) for i in range(len(list_4))]
        y5 = [np.average(list_5) for i in range(len(list_5))]

        self.print_average([list_1, list_2, list_3, list_4, list_5])

        x = [i for i in range(len(list_1))]

        fig, ax = plt.subplots()
        ax.plot(x, y1, label=self.short_rate[0])
        ax.plot(x, y2, label=self.short_rate[1])
        ax.plot(x, y3, label=self.short_rate[2])
        ax.plot(x, y4, label=self.short_rate[3])
        ax.plot(x, y5, label=self.short_rate[4])
        ax.legend()

        ax.yaxis.grid(True)
        ax.set_ylabel('Среднее средних дельта-поведений')

        plt.show()

    def simple_plot(self):
        """ Строим график средних дельта-поведений от оценки """
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

        self.print_average(all_data)

        fig, ax = plt.subplots()

        parts = ax.violinplot(all_data, showmeans=True, showmedians=True)
        #ax.set_title('Распределение поведения пользователей')

        # adding horizontal grid lines

        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data))])
        ax.set_xlabel('Оценки пользователей')
        ax.set_ylabel('Дельта-поведения')

        # add x-tick labels
        plt.setp(ax, xticks=[y + 1 for y in range(len(all_data))],
                 xticklabels=self.short_rate)

        plt.show()

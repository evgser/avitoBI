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

    def get_random_average(self, count=100, random=True):
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

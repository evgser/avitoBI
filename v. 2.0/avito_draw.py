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

    def lost_users_and_items_calculation(self):
        """ Функция считает количество всех потерянных объявлений и пользователей и выводит их в консоль """
        lost_users = 0
        lost_items = 0
        for i in range(len(self.all_data)):

            if self.all_data[i][1] == "True":
                lost_users += 1
            lost_items += float(self.all_data[i][0])

        print("Количество потерянных объявлений: ", lost_items)
        print("Количество потерянных пользователей: ", lost_users)

    def data_handler_category(self):
        """"""

        users_dict = {}
        unhappy_users_dict = {}
        lost_users_dict = {}
        lost_items_dict = {}
        for i in range(len(self.all_data)):

            # Считаем количество людей по категориям
            if self.all_data[i][2] not in users_dict.keys():
                users_dict.update({self.all_data[i][2]: 1})
            else:
                users_dict.update({self.all_data[i][2]: users_dict[self.all_data[i][2]] + 1})

            # Считаем количество недовольных людей по категориям
            if float(self.all_data[i][0]) > 0:
                if self.all_data[i][2] not in unhappy_users_dict.keys():
                    unhappy_users_dict.update({self.all_data[i][2]: 1})
                else:
                    unhappy_users_dict.update({self.all_data[i][2]: unhappy_users_dict[self.all_data[i][2]] + 1})

            # Cчитаем количество потерянных пользователей
            if self.all_data[i][1]:
                pass


        self.plot(unhappy_users_dict)
        print(lost_users_dict)

    def plot(self, data_dict):

        fig, ax = plt.subplots()
        fig.set_size_inches(7, 3, forward=True)

        sorted_list = sorted(data_dict.items(), key=operator.itemgetter(1))

        group_names = list(sorted_list[i][0] for i in range(len(sorted_list)))
        group_data = list(sorted_list[i][1] for i in range(len(sorted_list)))

        ax.barh(group_names, group_data, height=0.4)

        ax.set_xlabel('Performance')
        ax.set_title('How fast do you want to go today?')
        plt.show()

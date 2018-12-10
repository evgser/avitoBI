import pandas as pd
import avito_handler as ah
import avito_draw as ad
from datetime import datetime
import csv


if __name__ == '__main__':

    criterion_file = 'data_support.txt'
    criterion_file_tmp = 'data_support_tmp.txt'
    lost_users_and_items_file = 'data_lost_users_and_items.csv'
    lost_users_and_items_file_tmp = 'data_lost_users_and_items_tmp.csv'

    def criterion_handler(users_file, support_file, criterion_file):

        # Создаём DataFrame для пользователей и их обращений в поддержку
        users_df = pd.read_csv(users_file)
        support_df = pd.read_csv(support_file)

        # Создаём класс обработки критерия эффективности службы поддержки и записываем данные в словарь
        criterion = ah.CriterionHandler(users_df, support_df)
        metrics_list = criterion.users_handler()
        metrics_dict = criterion.transform_metrics_to_dict(metrics_list)

        # Завписываем данные эффективности службы поддержки
        f = open(criterion_file, 'w', encoding='utf-8')
        for i in metrics_dict.keys():
            criterion_line = str(i)
            for j in metrics_dict[i]:
                criterion_line = criterion_line + ', ' + str(j)
            criterion_line += '\n'
            f.writelines(criterion_line)
        f.close()

    def criterion_draw(criterion_file, count):
        """Рисуем графики эффективности службы поддержки"""

        # Читаем данные эффективности службы поддержки
        f = open(criterion_file, 'r', encoding='utf-8')

        # Формируем данные эффективности службы поддержки
        data_dict = {}
        for line in f:
            sub_list = line.split(',')
            data_dict.update({sub_list[0]: sub_list[1:]})

        # Создаём класс отрисовки графиков
        draw = ad.AvitoDraw(data_dict)

        # Рисуем график распределения дельта-значений по оценкам
        draw.plot_violin()

        # Рисуем график дельта-значений
        draw.simple_plot()

        # Рисуем график средних дельта-значений по рандомным выборкам и их их усредненных значений
        draw.plot_multi_average(count)

    def lost_users_and_items_handler(users_file, support_file, lost_users_and_items_file, avg_delta):

        # Создаём DataFrame для пользователей и их обращений в поддержку
        users_df = pd.read_csv(users_file)
        support_df = pd.read_csv(support_file)

        # Создаём класс обработки критерия эффективности службы поддержки и записываем данные в словарь
        handler = ah.HandlerOfLostUsersAndItems(users_df, support_df)
        # Задаём величину, от которой будем считать объявления потерянными
        handler.set_avg_delta(avg_delta)

        # Считаем метрики пользователя
        metric_list = handler.users_handler()

        # Записываем метрики в csv файл
        with open(lost_users_and_items_file, "w", newline="", encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(['lost_items', 'lost_user', 'ticket_category', 'ticket_subcategory'])
            writer.writerows(metric_list)

    def lost_users_and_items_draw(lost_users_and_items_file):

        # Инициализация списка для хранения метрик пользователей
        data_list = []

        # Чтение и заполнение списка метриками пользователей
        with open(lost_users_and_items_file, "r", newline="", encoding='UTF-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if reader.line_num != 1:
                    data_list.append([row[i] for i in range(4)])

        # Создание класса для отрисовки графиков
        draw = ad.AvitoDraw2(data_list)

        # Получаем потери в цифрах
        draw.lost_users_and_items_calculation()

        # тест
        draw.data_handler_category()


    print("Выберите действие")
    print("Часть 1: ")
    print("1 - Получить и записать критерий эффективности службы поддержки")
    print("2 - Получить и записать критерий эффективности службы поддержки (тестовая выборка)")
    print("3 - Построить графики эффективности службы поддержки" + '\n')

    print("Часть 2: ")
    print("4 - Получить и записать данные потерь пользователей и объявлений")
    print("5 - Получить и записать данные потерь пользователей и объявлений (тестовая выборка)")
    print("6 - Построить графики потерь пользователей и объявлений" + '\n')

    choice = int(input())

    # Выводим время начала работы программы
    print('\n')
    print("Время начала работы программы: ", datetime.now(), '\n')

    # Часть 1
    if choice == 1:
        criterion_handler('csv_db/part 1/3.0.0.csv', 'csv_db/part 1/2.0.0.csv', criterion_file)
    if choice == 2:
        criterion_handler('csv_db/part 1/3.0.0 tmp.csv', 'csv_db/part 1/2.0.0 tmp.csv', criterion_file_tmp)
    if choice == 3:

        print("Сколько рандомных выборок построить?")
        count = int(input())
        print('\n')

        criterion_draw(criterion_file, count)

    # Часть 2
    # Задаём значение, относительно которого мы будем принимать решение о эффективности службы поддержки
    avg_delta = -0.5573

    if choice == 4:
        lost_users_and_items_handler('csv_db/part 2/3.1.1.csv', 'csv_db/part 2/2.1.1.csv',
                                     lost_users_and_items_file, avg_delta)
    if choice == 5:
        lost_users_and_items_handler('csv_db/part 2/3.1.1 tmp.csv', 'csv_db/part 2/2.1.1 tmp.csv',
                                     lost_users_and_items_file_tmp, avg_delta)
    if choice == 6:
        lost_users_and_items_draw(lost_users_and_items_file)

    # Выводим время завершения программы
    print('\n')
    print(datetime.now())

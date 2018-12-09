import pandas as pd
import avito_handler as ah
import avito_draw as ad
from datetime import datetime


if __name__ == '__main__':

    criterion_file = 'data_support.txt'
    lost_users_and_items_file = 'data_lost_users_and_items.txt'

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

    def lost_users_and_items_handler(users_file, support_file, lost_users_and_items_file):
        pass

    def lost_users_and_items_draw(lost_users_and_items_file):
        pass


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

    if choice == 1:
        criterion_handler('csv_db/part 1/3.0.0.csv', 'csv_db/part 1/2.0.0.csv', criterion_file)
    if choice == 2:
        criterion_handler('csv_db/part 1/3.0.0 tmp.csv', 'csv_db/part 1/2.0.0 tmp.csv', criterion_file)
    if choice == 3:

        print("Сколько рандомных выборок построить?")
        count = int(input())
        print('\n')

        criterion_draw(criterion_file, count)

    if choice == 4:
        lost_users_and_items_handler('csv_db/part 2/3.1.1.csv', 'csv_db/part 2/2.1.1.csv',
                                     lost_users_and_items_file)
    if choice == 5:
        lost_users_and_items_handler('csv_db/part 2/3.1.1 tmp.csv', 'csv_db/part 2/2.1.1 tmp.csv',
                                     lost_users_and_items_file)
    if choice == 6:
        lost_users_and_items_draw(lost_users_and_items_file)

    # Выводим время завершения программы
    print('\n')
    print(datetime.now())

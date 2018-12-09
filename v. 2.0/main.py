import pandas as pd
import avito_handler as ah
import avito_draw as ad
from datetime import datetime
import csv

if __name__ == '__main__':

    # Выводим время начала работы программы
    print("Время начала работы программы: ", datetime.now())

    # print("Выберите действие")
    # print("1 - Получить критерий эффективности службы поддержки (все пользователи)")
    # print("2 - Получить критерий эффективности службы поддержки (рандомно выбранные пользователи)")
    # print("3 - *в разработке*")
    # choice = int(input())


    def criteria_handler():
        #if choice == 1 or choice == 2:
        users_file = 'csv_db/3.0.0.csv'
        support_file = 'csv_db/2.0.0.csv'

        # if choice == 3:
        #    pass

        # Создаём DataFrame для пользователей и их обращений в поддержку
        users_df = pd.read_csv(users_file)
        support_df = pd.read_csv(support_file)

        # Очищаем за собой переменные
        del users_file
        del support_file

        # Тестовый прогон
        spt_crt = ah.CriteriaHandler(users_df, support_df)
        metrics_list = spt_crt.users_handler()
        metrics_dict = spt_crt.transform_metrics_to_dict(metrics_list)

        criteria_file = 'data_support.txt'

        f = open(criteria_file, 'w', encoding='utf-8')
        for i in metrics_dict.keys():
            pam = str(i)
            for j in metrics_dict[i]:
                pam = pam + ', ' + str(j)
            pam += '\n'
            f.writelines(pam)
        f.close()

    def draw():
        criteria_file = 'data_support.txt'

        f = open(criteria_file, 'r', encoding='utf-8')

        data_dict = {}
        for line in f:
            sub_list = line.split(',')
            data_dict.update({sub_list[0]: sub_list[1:]})

        drw_obj = ad.AvitoDraw(data_dict)
        drw_obj.plot_multi_average()
        #drw_obj.plot_violin()
        #drw_obj.simple_plot()

    draw()

    # ? Задаём дельта значение пользователей при положительных оценках поддержки
    good_delta = 0.678469

    # Выводим время завершения программы
    print(datetime.now())

import pandas as pd
import matplotlib.pyplot as plt
import avito_handler as ah


if __name__ == '__main__':

    # Указываем csv, которые содержат выборки пользователей по двум категориям good/bad
    g_users_file = 'csv_db/part 3.1.csv'
    b_users_file = 'csv_db/part 3.2.csv'

    # Указываем csv, которые содержат выборки обращений пользователей по двум категориям оценки good/bad
    g_support_file = 'csv_db/part 2.1.1.csv'
    b_support_file = 'csv_db/part 2.1.2.csv'

    # Создаём df для каждой категории выборок
    g_users_df = pd.read_csv(g_users_file)
    b_users_df = pd.read_csv(b_users_file)
    g_support_df = pd.read_csv(g_support_file)
    b_support_df = pd.read_csv(b_support_file)

    g_met = ah.HandlerOfUsers(g_users_df, g_support_df)

    x = g_met.handler_user_df()
    print(x)

    """

    MONTH_COUNT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    MONTH_LABEL = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                   'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = (10, 5)
    
    plt.bar(range(12), MONTH_COUNT)
    plt.xticks(range(12), MONTH_LABEL, rotation=90)
    plt.ylabel('Количество объявлений')
    plt.title('Количество объявлений пользователя по месяцам')

    plt.show()
    """



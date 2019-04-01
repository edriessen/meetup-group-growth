import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re

def convert_meetup_mixed_date_to_date(date):
    return datetime.strptime(date, '%B %d, %Y')

def load_excel_as_dataframe(path_to_file):
    df = pd.read_excel(path_to_file, dtype='str')
    df['Joined Group on'] = df['Joined Group on'].apply(lambda x: convert_meetup_mixed_date_to_date(x))
    return df;

def get_yearmonth_label_from_date(date):
    if date.month < 10:
        return str(date.year) + '0' + str(date.month)
    else:
        return str(date.year) + str(date.month)

def add_year_moth_column_to_dataframe(dataframe, date_column):
    dataframe['YearMonth'] = dataframe[date_column].apply(lambda x: get_yearmonth_label_from_date(x))
    return dataframe

def get_x_marks(range):
    x_marks = []
    pattern = re.compile("[0-9]{4}(0(1|4|7)|10)$")
    for item in range:
        if pattern.match(item):
            x_marks.append(item)
        else:
            x_marks.append('')
    return x_marks

def convert_df_to_sorted_yearmonth_range(df):
    series = df['YearMonth'].value_counts()
    df = series.to_frame()
    df = df.sort_index()
    return df

def get_new_index(df):
    index = np.arange(int(df.index.min()), int(df.index.max()) + 1)
    index_str = []
    for item in index:
        if item % 100 > 0 and item % 100 < 13:
            index_str.append(str(item))
    return index_str

def add_missing_values_to_index(df):
    new_index = get_new_index(df)
    df = df.reindex(index=new_index).fillna(0)
    return df

def plot_user_growth(df, months_with_meetup):
    x = df.index
    y = df['cumsum']

    bar_colors = []
    bar_labels = []
    number_of_meetups = 0
    for item in x:
        if item in months_with_meetup:
            number_of_meetups += 1
            bar_colors.append('#7FCC00')
            # bar_labels.append(str(number_of_meetups))
        else:
            bar_colors.append('#aaaaaa')
            bar_labels.append('')
    ax = plt.subplot()
    ax.grid(color='#dddddd', linestyle='-', linewidth=1, axis='y', zorder=1)
    ax.bar(x, y, color=bar_colors, zorder=3)
    plt.xticks(np.arange(0, len(df.index.values)+1), get_x_marks(df.index.values), rotation=90)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.axes.tick_params(axis='y', color='white')
    rects = ax.patches
    plt.show()

def plot_meetup_growth_from_excel_file_by_months_of_years(excel_filepath, months_of_years):
    df = load_excel_as_dataframe(excel_filepath)
    df = add_year_moth_column_to_dataframe(df, 'Joined Group on')
    df = convert_df_to_sorted_yearmonth_range(df)
    df = add_missing_values_to_index(df)
    df['cumsum'] = df['YearMonth'].cumsum()
    print(df)
    plot_user_growth(df, months_of_years)

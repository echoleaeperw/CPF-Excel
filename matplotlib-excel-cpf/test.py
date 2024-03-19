import csv
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

plt.rcParams['font.family'] = 'Arial Unicode MS'

def make_plot(config):
    filename = config['filename']
    fig_size = tuple(config['fig_size'])
    y_label = config['y_label']
    left_ticks = config['left_ticks']
    right_ticks = config['right_ticks']
    date_interval = config['date_interval']
    legend_labels = config['legend_labels']
    rect = config['rect']
    # 根据数据文件名生成输出文件名

    output_file = os.path.splitext(filename)[0] + '.png'

    fig, ax_f = plt.subplots(figsize=fig_size)
    ax_c = ax_f.twinx()

    ax_f.set_ylabel(y_label)
    ax_c.set_ylabel(y_label)

    dates = []
    overnight_rates = []
    one_month_rates = []
    three_month_rates = []

    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            date = datetime.strptime(row[0], '%Y/%m/%d')
            dates.append(date)
            overnight_rates.append(float(row[1]))
            one_month_rates.append(float(row[2]))
            three_month_rates.append(float(row[3]))

    start_date = dates[0]
    end_date = dates[-1]

    ax_f.plot(dates, overnight_rates, label=legend_labels[0])
    ax_f.plot(dates, one_month_rates, label=legend_labels[1])
    ax_c.plot(dates, three_month_rates, label=legend_labels[2])

    ax_f.set_xlabel('')

    ax_f.set_xlim(start_date, end_date)
    ax_f.xaxis.set_major_locator(mdates.DayLocator(interval=date_interval))

    ax_f.set_yticks(left_ticks)
    ax_f.set_yticklabels([f'{tick:.1f}' for tick in left_ticks])

    ax_c.set_yticks(right_ticks)
    ax_c.set_yticklabels([f'{tick:.1f}' for tick in right_ticks])

    date_formatter = mdates.DateFormatter('%Y/%m/%d')
    ax_f.xaxis.set_major_formatter(date_formatter)

    labels = ax_f.get_xticklabels()
    plt.setp(labels, rotation=90, ha='center', va='bottom')
    ax_f.tick_params(axis='x', pad=65)

    ax_f.spines['left'].set_position(('data', mdates.date2num(start_date)))
    ax_f.spines['right'].set_position(('data', mdates.date2num(start_date)))

    ax_f.spines['top'].set_visible(False)
    ax_c.spines['top'].set_visible(False)

    lines_f, labels_f = ax_f.get_legend_handles_labels()
    lines_c, labels_c = ax_c.get_legend_handles_labels()
    ax_f.legend(lines_f + lines_c, labels_f + labels_c, loc='upper center', bbox_to_anchor=(0.5, -0.30), ncol=3, frameon=False)

    ax_f.set_ylabel('')
    ax_c.set_ylabel('')

    fig.tight_layout(rect=rect)

    # 保存图像文件
    output_dir = 'output_images'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(filename).split('.')[0] + '.png')
    plt.savefig(output_file)

    # 清空图形,准备绘制下一个图形
    plt.clf()


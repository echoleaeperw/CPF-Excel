import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 设置中文字体
plt.rcParams['font.family'] = 'Arial Unicode MS'

def make_plot(config):
    # 获取折线图的变量参数
    filename = config['filename']
    fig_size = tuple(config['fig_size'])
    y_label = config['y_label']
    left_ticks = config['left_ticks']
    right_ticks = config['right_ticks']
    date_interval = config['date_interval']
    legend_labels = config['legend_labels']
    rect = config['rect']
    # 根据数据文件名生成输出文件名
    output_file = os.path.splitext(filename)[0] + '.jpg'

    # 创建折线图和两个y轴
    fig, ax_f = plt.subplots(figsize=fig_size)
    ax_c = ax_f.twinx()

    ax_f.set_ylabel(y_label)
    ax_c.set_ylabel(y_label)

    # 初始化
    dates = []
    overnight_rates = []
    one_month_rates = []
    three_month_rates = []

    # 读取CSV文件数据
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            date = datetime.strptime(row[0], '%Y/%m/%d')
            dates.append(date)
            overnight_rates.append(float(row[1]))
            one_month_rates.append(float(row[2]))
            three_month_rates.append(float(row[3]))

    # 获取起始日期和结束日期

    start_date = dates[0]
    end_date = dates[-1]

    ax_f.plot(dates, overnight_rates, label=legend_labels[0])
    ax_f.plot(dates, one_month_rates, label=legend_labels[1])
    ax_c.plot(dates, three_month_rates, label=legend_labels[2])

    # x轴标签为空
    ax_f.set_xlabel('')

    ax_f.set_xlim(start_date, end_date)
    ax_f.xaxis.set_major_locator(mdates.DayLocator(interval=date_interval))

    # 设置两个y轴的刻度，便签都为空
    ax_f.set_yticks(left_ticks)
    ax_f.set_yticklabels([f'{tick:.1f}' for tick in left_ticks])

    ax_c.set_yticks(right_ticks)
    ax_c.set_yticklabels([f'{tick:.1f}' for tick in right_ticks])

    # # 设置x轴日期格式
    date_formatter = mdates.DateFormatter('%Y/%m/%d')
    ax_f.xaxis.set_major_formatter(date_formatter)

    # 日期竖直
    labels = ax_f.get_xticklabels()
    plt.setp(labels, rotation=90, ha='center', va='bottom')
    ax_f.tick_params(axis='x', pad=65)

    ax_f.spines['left'].set_position(('data', mdates.date2num(start_date)))
    ax_f.spines['right'].set_position(('data', mdates.date2num(start_date)))

    # 隐藏上方的边框
    ax_f.spines['top'].set_visible(False)
    ax_c.spines['top'].set_visible(False)

    # 合并两个y轴的图例
    lines_f, labels_f = ax_f.get_legend_handles_labels()
    lines_c, labels_c = ax_c.get_legend_handles_labels()
    ax_f.legend(lines_f + lines_c, labels_f + labels_c, loc='upper center', bbox_to_anchor=(0.5, -0.30), ncol=3, frameon=False)

    # 两个y标签为空
    ax_f.set_ylabel('')
    ax_c.set_ylabel('')

    # 调整布局
    fig.tight_layout(rect=rect)

    # 创建输出文件夹
    output_folder = 'output_images'
    os.makedirs(output_folder, exist_ok=True)

    # 生成输出图片的文件名
    output_filename = f"{os.path.splitext(os.path.basename(config['filename']))[0]}.png"
    output_path = os.path.join(output_folder, output_filename)

    plt.savefig(output_path)  # 保存图形到文件夹
    # 清空图形,准备绘制下一个图形
    plt.clf()



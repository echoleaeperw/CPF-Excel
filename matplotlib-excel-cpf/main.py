from graph import make_plot
import json

if __name__ == '__main__':
    # 读取JSON配置文件
    with open('plot_config.json', 'r') as f:
        plot_configs = json.load(f)

    # 遍历配置列表,为每个配置生成图形
    for config in plot_configs:
        make_plot(config)

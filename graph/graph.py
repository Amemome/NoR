import matplotlib.pyplot as plt     
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'   
matplotlib.rcParams['font.size'] = 12                
matplotlib.rcParams['axes.unicode_minus'] = False       
import numpy as np

class graph:
    def draw(self, command: dict):
        종류 = command.get('종류')
        함수매핑 = {
            '선그래프': self.draw_line,
            '막대그래프': self.draw_bar,
            '산점도그래프': self.draw_scatter
        }

        if 종류 not in 함수매핑:
            raise ValueError(f"알 수 없는 그래프 종류: {종류}")

        함수매핑[종류](command)
    def draw_line(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        option = command.get('옵션', {})
    
        plt.figure()
        plot_option = {}

        common_keys = ['color', 'label', 'marker', 'linestyle', 'linewidth']
        for key in common_keys:
            if key in option:
                plot_option[key] = option[key]

        plt.plot(x, y, **plot_option)

        if 'label' in option:
            plt.legend()
        if '제목' in option:
            plt.title(option['제목'])

        plt.tight_layout()
        plt.show()
    def draw_bar(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        option = command.get('옵션', {})
    
        plt.figure()
        plot_option = {}

        common_keys = ['color', 'alpha', 'label', 'width', 'edgecolor']
        for key in common_keys:
            if key in option:
                plot_option[key] = option[key]

        plt.bar(x, y, **plot_option)

        if 'label' in option:
            plt.legend()
        if '제목' in option:
            plt.title(option['제목'])

        plt.tight_layout()
        plt.show()
    def draw_scatter(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        option = command.get('옵션', {})
    
        plt.figure()
        plot_option = {}

        common_keys = ['color', 'marker', 'label', 's', 'edgecolors']
        for key in common_keys:
            if key in option:
                plot_option[key] = option[key]

        plt.scatter(x, y, **plot_option)

        if 'label' in option:
            plt.legend()
        if '제목' in option:
            plt.title(option['제목'])

        plt.tight_layout()
        plt.show()
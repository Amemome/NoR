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
            '산점도그래프': self.draw_scatter,
            '이중그래프': self.draw_dual_axis_graph
        }

        함수매핑[종류](command)
   
    COLOR_MAP = {
        '검정': '#000000', 'black': '#000000',
        '파랑': '#0000FF', 'blue': '#0000FF',
        '갈색': '#A52A2A', 'brown': '#A52A2A',
        '회색': '#808080', 'gray': '#808080', 'grey': '#808080',
        '초록': '#008000', 'green': '#008000',
        '주황': '#FFA500', 'orange': '#FFA500',
        '분홍': '#FFC0CB', 'pink': '#FFC0CB',
        '보라': '#800080', 'purple': '#800080',
        '빨강': '#FF0000', 'red': '#FF0000',
        '흰색': '#FFFFFF', 'white': '#FFFFFF',
        '노랑': '#FFFF00', 'yellow': '#FFFF00'
    }

    def get_color(self, color_name):
        return self.COLOR_MAP.get(color_name, color_name)

    def draw_line(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        x, y = self.resolve_xy(x, y)

        option = command.get('옵션', {})
        출력옵션 = option.get('출력', {})
        ax = self.apply_figure_settings(출력옵션) 
        plot_option = {}

        if 'label' in option:
            plot_option['label'] = option['label']  

        plot_option.update(self.get_marker_options(option.get('marker'), 'line'))

        if 'line' in option:
            line = option['line']
            plot_option['linestyle'] = option['line']['linestyle']
            plot_option['linewidth'] = option['line']['linewidth']
            plot_option['color'] = self.get_color(line['color'])
            plot_option['alpha'] = option['line']['alpha'] 

        plt.plot(x, y, **plot_option)

        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

        self.apply_common_decorations(option, 출력옵션)
        self.save_or_show(출력옵션)

    def draw_bar(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        x, y = self.resolve_xy(x, y)

        option = command.get('옵션', {})
        출력옵션 = option.get('출력', {})
        ax = self.apply_figure_settings(출력옵션)
        plot_option = {}

        if 'bar' in option:
            bar = option['bar']
            if 'color' in bar:
                plot_option['color'] = self.get_color(bar['color'])
            if 'alpha' in bar:
                plot_option['alpha'] = bar['alpha']
            if 'width' in bar:
                plot_option['width'] = bar['width']

        if 'label' in option:
            plot_option['label'] = option['label']
    

        plt.bar(x, y, **plot_option)
        
        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

        self.apply_common_decorations(option, 출력옵션)
        self.save_or_show(출력옵션)

    def draw_scatter(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        x, y = self.resolve_xy(x, y)

        option = command.get('옵션', {})
        출력옵션 = option.get('출력', {})
        ax = self.apply_figure_settings(출력옵션)
        plot_option = {}

        if 'color' in option:
            plot_option['color'] = self.get_color(option['color'])
        if 'label' in option:
            plot_option['label'] = option['label']

        plot_option.update(self.get_marker_options(option.get('marker'), 'scatter'))

        plt.scatter(x, y, **plot_option)

        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

        self.apply_common_decorations(option, 출력옵션)
        self.save_or_show(출력옵션)

    def set_axis(self, 축옵션: dict, 축: str):
        axis= 축옵션.get('이름', '')
        kwargs = {}

        if '색' in 축옵션:
            kwargs['color'] = self.get_color(축옵션['색'])
        if '정렬' in 축옵션:
            kwargs['loc'] = 축옵션['정렬']

        if '눈금' in 축옵션:
            눈금 = 축옵션['눈금']

            if 축 == 'x':
                if all(isinstance(t, str) for t in 눈금):
                    plt.xticks(ticks=list(range(len(눈금))), labels=눈금)
                else:
                    plt.xticks(눈금)

            elif 축 == 'y':
                if all(isinstance(t, str) for t in 눈금):
                    plt.yticks(ticks=list(range(len(눈금))), labels=눈금)
                else:
                    plt.yticks(눈금)

        if 축 == 'x':
            plt.xlabel(axis, **kwargs)
        elif 축 == 'y':
            plt.ylabel(axis, **kwargs)

    def resolve_xy(self, x, y):
        if x is None and y is None:
            return [], []

        if x is not None and y is None:
            if all(isinstance(val, str) for val in x):
                return x, [0] * len(x)
            elif all(isinstance(val, (int, float)) for val in x):
                return list(range(len(x))), x

        if y is not None and x is None:
            if all(isinstance(val, str) for val in y):
                return y, [0] * len(y)
            elif all(isinstance(val, (int, float)) for val in y):
                return list(range(len(y))), y

        if all(isinstance(val, str) for val in x + y):
            print("❌ x와 y 둘 다 문자열일 수 없습니다.")
            return [], []

        if all(isinstance(val, str) for val in y) and all(isinstance(val, (int, float)) for val in x):
            return y, x

        return x, y

    def apply_figure_settings(self, 출력옵션: dict):
        fig, ax = plt.subplots(
            figsize=tuple(출력옵션.get('그래프 크기', (6, 4))),
            dpi=출력옵션.get('해상도', 100),
            facecolor=출력옵션.get('배경색', 'white')
        )
        ax.set_facecolor(출력옵션.get('내부 배경색', 'white'))
        return ax

    def apply_common_decorations(self, option: dict, 출력옵션: dict):
        if 'label' in option:
            plt.legend(loc=출력옵션.get('범례 위치', 'best'))
        if '제목' in option:
            plt.title(option['제목'])
        plt.tight_layout()

    def save_or_show(self, 출력옵션: dict):
        if '파일로 저장' in 출력옵션:
            plt.savefig(출력옵션['파일로 저장'])
        else:
            plt.show()

    def get_marker_options(self, marker_option: dict, plot_type: str):
        result = {}

        if not marker_option:
            return result

        result['marker'] = marker_option.get('문양', 'o')
        color = marker_option.get('색')
        if color:
            result['markerfacecolor' if plot_type == 'line' else 'facecolors'] = self.get_color(color)

        size = marker_option.get('크기')
        if size:
            if plot_type == 'line':
                result['markersize'] = size
            elif plot_type == 'scatter':
                result['s'] = size

        return result
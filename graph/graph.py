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

        출력옵션 = option.get('출력', {})
    
        plt.figure(
            figsize=tuple(출력옵션.get('그래프 크기', (6, 4))),
            dpi=출력옵션.get('해상도', 100),
            facecolor=출력옵션.get('배경색', 'white')
        )   
        plot_option = {}

        if 'label' in option:
            plot_option['label'] = option['label']  

        if 'marker' in option:
            plot_option['marker'] = option['marker']['문양']
            plot_option['markersize'] = option['marker']['크기']
            plot_option['markerfacecolor'] = option['marker']['색']
            plot_option['markeredgecolor'] = option['marker']['테두리 색'] 

        if 'line' in option:
            plot_option['linestyle'] = option['line']['linestyle']
            plot_option['linewidth'] = option['line']['linewidth']
            plot_option['color'] = option['line']['color']
            plot_option['alpha'] = option['line']['alpha'] 

        plt.plot(x, y, **plot_option)

        if 'label' in option:
            plt.legend(loc=출력옵션.get('범례 위치', 'best'))
        if '제목' in option:
            plt.title(option['제목'])
        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

        plt.tight_layout()

        if '파일로 저장' in 출력옵션:
            plt.savefig(출력옵션['파일로 저장'])
        else:
            plt.show()
            
    def draw_bar(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        option = command.get('옵션', {})
        출력옵션 = option.get('출력', {})

        plt.figure(
            figsize=tuple(출력옵션.get('그래프 크기', (6, 4))),
            dpi=출력옵션.get('해상도', 100),
            facecolor=출력옵션.get('배경색', 'white')
        )
        plot_option = {}

        if 'bar' in option:
            bar = option['bar']
            if 'color' in bar:
                plot_option['color'] = bar['color']
            if 'alpha' in bar:
                plot_option['alpha'] = bar['alpha']
            if 'width' in bar:
                plot_option['width'] = bar['width']
            if 'edgecolor' in bar:
                plot_option['edgecolor'] = bar['edgecolor']

        if 'label' in option:
            plot_option['label'] = option['label']
    
        plt.bar(x, y, **plot_option)
      
        if 'label' in option:
            plt.legend(loc=출력옵션.get('범례 위치', 'best'))
        if '제목' in option:
            plt.title(option['제목'])
        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

        plt.tight_layout()

        if '파일로 저장' in 출력옵션:
            plt.savefig(출력옵션['파일로 저장'])
        else:
            plt.show()

    def draw_scatter(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        option = command.get('옵션', {})
        출력옵션 = option.get('출력', {})

        plt.figure(
            figsize=tuple(출력옵션.get('그래프 크기', (6, 4))),
            dpi=출력옵션.get('해상도', 100),
            facecolor=출력옵션.get('배경색', 'white')
        )

        plot_option = {}

        if 'color' in option:
            plot_option['color'] = option['color']
        if 'label' in option:
            plot_option['label'] = option['label']
        if 'edgecolors' in option:
            plot_option['edgecolors'] = option['edgecolors']

        if 'marker' in option:
            marker_opt = option['marker']
            plot_option['marker'] = marker_opt.get('문양', 'o')
            plot_option['s'] = marker_opt.get('크기', 20)
            plot_option['facecolors'] = marker_opt.get('색', 'blue')
            plot_option['edgecolors'] = marker_opt.get('테두리 색', 'black')

        plt.scatter(x, y, **plot_option)

        if 'label' in option:
            plt.legend(loc=출력옵션.get('범례 위치', 'best'))
        if '제목' in option:
            plt.title(option['제목'])
        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

        plt.tight_layout()

        if '파일로 저장' in 출력옵션:
            plt.savefig(출력옵션['파일로 저장'])
        else:
            plt.show()

    def set_axis(self, 축옵션: dict, 축: str):
        axis = 축옵션.get('이름', '')
        kwargs = {}

        if '색' in 축옵션:
            kwargs['color'] = 축옵션['색']
        if '정렬' in 축옵션:
            kwargs['loc'] = 축옵션['정렬']
        if '눈금' in 축옵션:
            if 축 == 'x':
                plt.xticks(축옵션['눈금'])
            elif 축 == 'y':
                plt.yticks(축옵션['눈금'])

        if 축 == 'x':
            plt.xlabel(axis, **kwargs)
        elif 축 == 'y':
            plt.ylabel(axis, **kwargs)

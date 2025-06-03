import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['axes.unicode_minus'] = False

legend_position_map = {
    "최적": "best",
    "우상단": "upper right",
    "좌상단": "upper left",
    "좌하단": "lower left",
    "우하단": "lower right",
    "오른쪽": "right",
    "좌중앙": "center left",
    "우중앙": "center right",
    "하중앙": "lower center",
    "상중앙": "upper center",
    "중앙": "center"
}

line_style_map = {
    "실선": "-",
    "점선": ":",
    "파선": "--",
    "점선파선": "-."
}

marker_shape_map = {
    "원": "o",

    "사각형": "s",
    "네모": "s",

    "점": ".",

    "엑스": "x",

    "삼각형": "^",
    "세모": "^",
    "삼각형 위": "^",
    "위쪽 삼각형": "^",

    "삼각형 아래": "v",
    "아래쪽 삼각형": "v",

    "삼각형 왼쪽": "<",
    "왼쪽 삼각형": "<",

    "삼각형 오른쪽": ">",
    "오른쪽 삼각형": ">",

    "별": "*",
    "별표": "*"
}
class graph:
    save_counter = {'선그래프': 0, '막대그래프': 0, '산점도그래프': 0}
    output_folder = 'static'

    def draw(self, command: dict):
        self._plot(command, 저장=False)

    def save(self, command: dict):
        self._plot(command, 저장=True)

    def _plot(self, command: dict, 저장: bool = False):
        종류 = command.get('종류')
        option = command.get('옵션', {})
        출력옵션 = option.get('출력', {})

        draw_func = {
            '선그래프': self.draw_line,
            '막대그래프': self.draw_bar,
            '산점도그래프': self.draw_scatter,
            '선': self.draw_line,
            '막대': self.draw_bar,
            '산점도': self.draw_scatter,
            'line': self.draw_line,
            'bar': self.draw_bar,
            'scatter': self.draw_scatter
        }.get(종류)

        if draw_func is None:
            print(f"❌ 지원하지 않는 그래프 종류: {종류}")
            return

        self.apply_figure_settings(출력옵션)
        draw_func(command)
        self.apply_common_decorations(option, 출력옵션)

        if 저장:
            self.save_figure(command.get('이름'))
        else:
            plt.show()

    def save_figure(self, 그래프이름):
        파일명 = f"{그래프이름}.png"
        
        # 전체 파일 경로 생성
        full_path = os.path.join(self.output_folder, 파일명)

        try:
            plt.savefig(full_path, bbox_inches='tight') # bbox_inches='tight'는 여백을 최소화
            print(f"✅ 파일 저장됨: {full_path}")
        except Exception as e:
            print(f"❌ 그래프 저장 중 오류 발생: {e}")

    def draw_line(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        x, y = self.resolve_xy(x, y)

        option = command.get('옵션', {})
        plot_option = {}

        if 'label' in option:
            plot_option['label'] = option['label']

        plot_option.update(self.get_marker_options(option.get('marker'), 'line'))

        if 'line' in option:
            line = option['line']
            plot_option['linestyle'] = line_style_map.get(line.get('linestyle'), line.get('linestyle'))
            plot_option['linewidth'] = line.get('linewidth')
            plot_option['color'] = self.get_color(line.get('color'))
            plot_option['alpha'] = line.get('alpha')

        plt.plot(x, y, **plot_option)

        if 'x축' in option:
            self.set_axis(option['x축'], 'x')
        if 'y축' in option:
            self.set_axis(option['y축'], 'y')
    def draw_bar(self, command: dict):
        # ... (이전 코드 생략) ...
        x_raw, y_raw = self.resolve_xy(command.get('x'), command.get('y'))

        x_is_categorical = all(isinstance(val, str) for val in x_raw) and len(x_raw) > 0

        x_for_plotting = []
        x_tick_labels = None

        if x_is_categorical:
            x_tick_labels = x_raw
            x_for_plotting = list(range(len(x_raw)))
        else:
            x_for_plotting = [val for val in x_raw if isinstance(val, (int, float))]
            x_tick_labels = None

        y_for_plotting = [val for val in y_raw if isinstance(val, (int, float))]

        if not x_for_plotting or not y_for_plotting:
            print("❌ 그래프를 그릴 유효한 데이터가 부족합니다.")
            return

        option = command.get('옵션', {})
        plot_option = {}

        if 'bar' in option:
            bar = option['bar']
            plot_option['color'] = self.get_color(bar.get('color'))
            plot_option['alpha'] = bar.get('alpha')

            # --- 이 부분 수정 ---
            width_val = bar.get('width')
            if isinstance(width_val, (int, float)):
                # 이미 숫자형이라면 그대로 사용
                plot_option['width'] = width_val
            elif isinstance(width_val, str):
                # 문자열이라면 float으로 변환 시도
                try:
                    plot_option['width'] = float(width_val)
                except ValueError:
                    # 변환 실패 시 경고 출력 및 기본값 사용
                    print(f"⚠️ 경고: 막대 너비 '{width_val}'이(가) 유효한 숫자가 아닙니다. 기본값 0.8을 사용합니다.")
                    plot_option['width'] = 0.8 # Matplotlib 기본값
            else:
                # None이거나 예상치 못한 다른 타입일 경우 기본값 사용
                plot_option['width'] = 0.8 # Matplotlib 기본값
            # --- 수정 끝 ---

        if 'label' in option:
            plot_option['label'] = option['label']

        plt.bar(x_for_plotting, y_for_plotting, **plot_option)

        if 'x축' in option:
            x_axis_option_for_set_axis = option['x축'].copy()
            if x_is_categorical:
                x_axis_option_for_set_axis['눈금'] = x_tick_labels
            self.set_axis(x_axis_option_for_set_axis, 'x')
        elif x_is_categorical:
            plt.xticks(ticks=x_for_plotting, labels=x_tick_labels)

        if 'y축' in option:
            self.set_axis(option['y축'], 'y')

    def draw_scatter(self, command: dict):
        x = command.get('x')
        y = command.get('y')
        x, y = self.resolve_xy(x, y)

        option = command.get('옵션', {})
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

    def apply_figure_settings(self, 출력옵션: dict):
        facecolor = self.get_color(출력옵션.get('배경색', 'white'))
        inner_color = self.get_color(출력옵션.get('내부 배경색', 'white'))

        fig, ax = plt.subplots(
            figsize=tuple(출력옵션.get('그래프 크기', (6, 4))),
            dpi=출력옵션.get('해상도', 100),
            facecolor=facecolor
        )
        ax.set_facecolor(inner_color)
        return ax

    def apply_common_decorations(self, option: dict, 출력옵션: dict):
        if 'label' in option:
            plt.legend(loc=legend_position_map.get(출력옵션.get('범례 위치', 'best'), 출력옵션.get('범례 위치', 'best')))
        if '제목' in option:
            plt.title(option['제목'])
        plt.tight_layout()

    def set_axis(self, 축옵션: dict, 축: str):
        axis = 축옵션.get('이름', '')
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
            return x, [0]*len(x)
        if y is not None and x is None:
            return list(range(len(y))), y
        return x, y

    def get_color(self, color_name):
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
        return COLOR_MAP.get(color_name, color_name)

    def get_marker_options(self, marker_option: dict, plot_type: str):
        result = {}
        if not marker_option:
            return result

        result['marker'] = marker_shape_map.get(marker_option.get('문양', 'o'), marker_option.get('문양', 'o'))
        color = marker_option.get('색')
        if color:
            key = 'markerfacecolor' if plot_type == 'line' else 'facecolors'
            result[key] = self.get_color(color)

        size = marker_option.get('크기')
        if size:
            result['markersize' if plot_type == 'line' else 's'] = size

        return result

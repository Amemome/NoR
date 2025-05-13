from graph import graph

graph1 = {
    '종류': '선그래프',
    'x': [1, 2, 3],
    'y': [4, 5, 6],
    '옵션': {
        '제목': '샘플 선그래프',
        'color': 'green',
        'marker': 'o',
        'linestyle':'--',
        'linewidth': 5,
        'label' : '예시 데이터'
    }
}
graph2 = {
    '종류': '막대그래프',
    'x': ['이운길', '최현경', '류지성'],
    'y': [150, 200, 175],
    '옵션': {
        '제목' : '샘플 막대그래프',
        'color': 'blue',
        'alpha': 0.7,
        'width': 0.5,
        'label' : '예시 데이터',
        'edgecolor' : 'black'
    }
}
graph3 = {
    '종류': '산점도그래프',
    'x': [1,2,3,4,5],
    'y': [10, 20, 14, 30, 25],
    '옵션': {
        'color': 'orange',
        'marker': 'x',
        'width': 0.5,
        's' : 200,
        'alpha' : 0.7,
        'edgecolors' : 'red'
    }
}

g = graph()
g.draw(graph1)
g.draw(graph2)
g.draw(graph3)
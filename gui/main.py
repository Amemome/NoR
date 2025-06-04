from lang.nor import NoR

gram = """
그리기
그래프생성 "막대 그래프 테스트"
종류는 막대

라벨은 "식사량"
범례는 center

데이터는 [
[1,2,3,4,5]
]

제목은 "막대 기본 테스트" 

막대의 색은 "검정"

배경은 "노랑"
내부 배경색은 "파랑"
그리기
"""

nor = NoR(debug_mode=True, server_mode=False)

result = nor.run(gram)

print(len(result))

for err in result:
    print(str(err))
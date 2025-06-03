from lang.nor import NoR

gram = """
그래프생성 "기본 설정 테스트"
종류는 산점도 
마커의 종류는 별
마커의 색은 "green"
라벨은 "범레123"
범례는 우하단

데이터는 [[1,2,3,4,5], [5,4,3,2,1]]

제목은 "산점도 기본 테스트" 
그래프 크기는 [5, 6]  
x축의 색은 "빨강"
x축의 이름은 "엑스축"
y축의 이름은 "와이"

배경은 "노랑"
내부 배경색은 "파랑"
그리기
"""

nor = NoR(debug_mode=True, server_mode=True)

result = nor.run(gram)

print(result)
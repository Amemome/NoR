from nor import NoR

gram = """
// Test 3: 객체 선택자 없는 속성 및 기본값
그래프생성 "기본 설정 테스트"
종류는 산점도그래프 
마커의 종류는 ^
라벨은 "범레123"
범례는 우상단

데이터는 [[1,2,3,4,5], [5,4,3,2,1]]

제목은 "산점도 기본 테스트" 
그래프 크기는 [5, 6]  
x축의 색은 "black"
x축의 이름은 "엑스축"
y축의 이름은 "와이"
x축의 라벨은 "하이"
저장
"""

nor = NoR(debug_mode=True, server_mode=False)

result = nor.run(gram)

print(result)
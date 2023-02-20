매개변수
second,  # 경과 시간 (안 씀)
front_image,  # 전면 이미지 (안 씀)
rear_image,  # 후면 이미지 (없음)
front_lidar,  # 전면 라이다 센서
rear_lidar  # 후면 라이다 센서 (없음)

변수
situation: 도로 상황
steer: 조향
velocity: 속력
v: 세로선, 0 ~ 6 (상단: 255, 하단: 0)
l: 가로선이 왼쪽에서 만나는 좌표, 0 ~ 2
r: 가로선이 오른쪽에서 만나는 좌표, 0 ~ 2
l, r은 중앙이 0, 위로부터 l[0]/r[0], l[1]/r[1], l[2]/r[2]

canny 창
차선 인식 상황

요구사항
pip install jajucha
pip install opencv-python
pip install keyboard
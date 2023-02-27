<div align="center">
    <img src="https://capsule-render.vercel.app/api?type=transparent&height=150&animation=fadeIn&fontColor=8c8cff&text=CarDS&fontSize=80&fontAlignY=50&desc=2023년%20동산고등학교%20자율주행자동차%20대회&descAlignY=85"/>
</div>

<div align=right>
    <h6>
        by jtaeyeon05<br/>
        (2023/02/20~)
    </h6>
</div>

<div align="center">
    <a href="https://github.com/error0918/CarDS/archive/refs/heads/master.zip">
        다운로드
    </a>
</div>

<details>
    <summary>목차</summary>
    <h6>
        <ul dir="auto">
            <a href="https://github.com/error0918/CarDS#-----Introduction">
                <li>
                    📜 Introduction
                </li>
            </a>
            <a href="https://github.com/error0918/CarDS#-----Structure">
                <li>
                    👀 Required
                </li>
            </a>
            <a href="https://github.com/error0918/CarDS#-----Required">
                <li>
                    🖥️ Required
                </li>
            </a>
            <a href="https://github.com/error0918/CarDS#-----Variables">
                <li>
                    🆎 Variables
                </li>
            </a>
            <a href="https://github.com/error0918/CarDS#-----ETC">
                <li>
                    🧐 ETC
                </li>
            </a>
        </ul>
    </h6>
</details>

---

<h2>
    📜 Introduction
</h2>

2023년 2월 25일, 현대 모비스와 하나고등학교에서 주최하는 파이썬을 이용한 자율주행자동차 대회 동산고등학교 코드

---

<h2>
    👀 Structure
</h2>

```
├── data
│   │   자율주행 자동차를 주행하기 위한 data class 들이 작성되어 있습니다.
│   ├── __init__.py
│   ├── data.py
│   ├── difference.py
│   └── result.py
├── internal
│   │   자율주행 자동차를 주행하기 위한 구체적인 알고리즘들이 작성되어 있습니다.
│   ├── __init__.py
│   ├── halt.py
│   │   └   자율주행 자동차를 안전하게 중지하기 위한 함수가 작성되어 있습니다.
│   ├── module.py
│   │   └   자율주행 자동차의 주행과 관련된 함수들이 작성되어 있습니다.
│   └── util.py
│       └   코드 작성의 편의를 위한 함수들이 작성되어 있습니다.
├── jajucha
│   │   jajucha 라이브러리 내부 파일입니다.
│   ├── __init__.py
│   ├── communication.py
│   ├── config.py
│   ├── control.py
│   ├── graphics.py
│   └── planning.py
├── config.py
│   주행 설정 파일이 저장되어있습니다. canny 이미지 보여주기 여부, 자동차 별 오차 등을 입력할 수 있습니다.
├── main.py
│   자율주행 자동차 주행을 위한 메인 파일입니다.
├── offset.py
│   자율주행 자동차 오차 확인을 위한 테스트 파일입니다.
└── README.md
```

<br/>

<h3>
    internal/module.py
</h3>

```python
hold_frame: Tuple[bool, int] = (False, 0)  
# 프레임 유지 변수 (프레임 유지 정의 여부, 남은 프레임 수)
last_result: Result = Result()
# 지난 주행 결과

class Direction(Enum): pass
# 주행 방향 Enum

def operation(result_list: List[Result]) -> Result: pass
# Result 결합 함수

def default(data: Data, difference_data: Difference) -> Result: pass
# 기본적으로 사용되는 module

def velocity(data: Data) -> Result: pass
# 속도

def steer(data: Data, difference_data: Difference) -> Result: pass
# 직진 조향
    
def curve(data: Data, difference_data: Difference) -> Result: pass
# 곡선
    
def left_right_angle(data: Data) -> Result: pass
# 왼쪽 직각
    
def right_right_angle(data: Data) -> Result: pass
# 오른쪽 직각

def four_lane(data: Data, direction: Direction = Direction.Stop) -> Result: pass
# 사차선
    
def left_three_lane(data: Data, direction: Direction = Direction.Stop) -> Result: pass
# ㅓ 삼차선
    
def right_three_lane(data: Data, direction: Direction = Direction.Stop) -> Result: pass
# ㅏ 삼차선
    
def t_three_lane(data: Data, direction: Direction = Direction.Stop) -> Result: pass
# T 삼차선
    
def lidar_scan(data: Data, direction: Direction = Direction.Stop, scan_distance: int = 250) -> Result: pass
# 근접 라이다 감지

def exit_left_dot_line(data: Data, difference_data: Difference) -> Result: pass  # Warning: Experimental Feature
# 왼쪽 점선 코스 탈출

def exit_right_dot_line(data: Data, difference_data: Difference) -> Result: pass  # Warning: Experimental Feature
# 오른쪽 점선 코스 탈출

def back_car(data: Data, scan_v_distance: int = 60, scan_lidar_distance: int = 160) -> Result: pass  # Warning: Experimental Feature
# V 또는 라이다 초 근접시 후진

def hold_result() -> Result: pass  # Warning: Experimental Feature
# 프레임 유지

def manual_drive() -> Result: pass  # Warning: Test Feature
# 수동 주행


class non_op:
    @staticmethod
    def esc_to_pause(): pass
    # ESC로 종료하기

    @staticmethod
    def control_current_velocity(current_velocity: int) -> int: pass  # Return New Current Velocity
    # Shift (*), Control (/)로 현재 속도 변경

    @staticmethod
    def control_base_velocity(): pass
    # +, -로 기본 속도 변경

    @staticmethod
    def save_result(result: Result): pass
    # 지난번 주행 결과 저장

    @staticmethod
    def get_last_result(): pass
    # 지난번 주행 결과 불러오기
```

<br/>

<h3>
    config.py
</h3>

```python
is_canny_show: bool  # canny 이미지 보여주기 여부 
is_esc_to_halt: bool  # esc로 종료할 때 자율주행 자동차를 halt할지 여부
```

---

<h2>
    🖥️ Required
</h2>

<h3>
    Python
</h3>

```
Recommanded: 3.7.8
Available with Python 3.7.8 or newer version
```

<br/>

<h3>
    Library
</h3>

```
pip install jajucha
pip install opencv-python
pip install keyboard
```

---

<h2>
    🆎 Variables
</h2>

```python
def process(
    self,
    second,  # 경과 시간
    front_image,  # 전면 이미지
    rear_image,  # 후면 이미지 (없음)
    front_lidar,  # 전면 라이다 센서
    rear_lidar  # 후면 라이다 센서 (없음)
): pass

@dataclass()
class Data:
    second: int  # 경과 시간
    front_lidar: int  # 전면 라이다 센서
    v: List[int]  # 세로선, 0 ~ 6 (상단: 255, 하단: 0)
    l: List[int]  # 가로선이 왼쪽에서 만나는 좌표, 0 ~ 2
    r: List[int]  # 가로선이 오른쪽에서 만나는 좌표, 0 ~ 2
    # l, r은 중앙이 0, 위로부터 l[0]/r[0], l[1]/r[1], l[2]/r[2]

@dataclass()
class Difference:
    l: List[int]  # 직진 코스에서 자율주행 자동차가 인식하는 l
    r: List[int]  # 직진 코스에서 자율주행 자동차가 인식하는 r
    base_v: int  # 기본 속도
    steer: int  # 자율주행 자동차가 직진하는 steer

@dataclass()
class Result:
    situation: Optional[str] = None  # 도로 상황
    steer: Optional[float] = None  # 조향
    velocity: Optional[int] = None  # 속력
    #  None일 경우 다음 값으로 넘어감
```

---

<h2>
    🧐 ETC
</h2>

```
canny 창: 차선 인식 상황
```

---

<div align="center">
    <h6>
        Copyright 2023. jtaeyeon05 all rights reserved 
    </h6>
</div>

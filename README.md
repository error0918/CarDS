<div align="center">
    <img src="https://capsule-render.vercel.app/api?type=transparent&height=150&animation=fadeIn&fontColor=8c8cff&text=CarDS&fontSize=80&fontAlignY=50&desc=2023년%20동산고등학교%20자율주행자동차%20대회&descAlignY=85"/>
</div>

<details>
    <summary>목차</summary>
    <h6>
        <ul dir="auto">
            <a href="https://github.com/error0918/CarDS/tree/main/#-----Introduction">
                <li>
                    📜 Introduction Me
                </li>
            </a>
            <a href="https://github.com/error0918/CarDS/tree/main/#-----Required">
                <li>
                    🖥️ Required
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

<h3>
    Library
</h3>

```
pip install jajucha
pip install opencv-python
pip install keyboard
```

---

<div align="center">
    <h6>
        Copyright 2023. jtaeyeon05 all rights reserved 
    </h6>
</div>
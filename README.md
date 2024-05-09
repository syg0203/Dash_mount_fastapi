# Dashboard
```
Fastapi하위 어플리케이션에 Dash(plotly)를 마운트한 가이드라인 코드
```
## URL
```
127.0.0.1:2030/
```
## File Tree
```
📦dash
 ┣ 📂src : 플롯, 대시보드 모듈을 임포트하여 대시 앱을 구성
 ┃ ┣ 📜__init__.py : Dash 애플리케이션 스크립트의 app 패키징 스크립트
 ┃ ┗ 📜example1.py : Dash 애플리케이션 스크립트
 ┣ 📜app.py : fastapi에 하위 대시 애플리케이션 마운트
 ┣ 📜dashboard_layout.py : (dashboard_layout.py): 대시보드의 HTML 레이아웃을 정의를 정의한 모듈
 ┗ 📜plots.py : 다양한 종류의 플롯(파이 차트, 막대 차트, 분포 플롯 등)을 생성하는 함수들을 포함하는 모듈
 ```
## TODO
```
1. dbc.col 분리
```
![image](https://github.com/syg0203/Dash_mount_fastapi/assets/79491796/90d8239a-6b70-4991-aca2-37cab46ff66a)

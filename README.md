# DTUMOS (Dynamic Taxi-based Urban Mobility Operation System)

**성남시 택시 시뮬레이션 시스템**

DTUMOS는 대한민국 경기도 성남시의 택시 운영을 시뮬레이션하고 최적화하는 시스템입니다. 실제 택시 데이터를 기반으로 승객-차량 매칭을 최적화하고, 시뮬레이션 결과를 시각화하여 분석할 수 있습니다.

---

## 📋 목차 (Table of Contents)

- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [설정 옵션](#설정-옵션)
- [모듈 설명](#모듈-설명)
- [시각화](#시각화)
- [요구사항](#요구사항)

---

## 🚀 주요 기능

### 1. **데이터 전처리 (Data Preprocessing)**
- 실제 택시 운행 데이터 처리
- 성남시 지역 경계(boundary) 내 데이터 필터링
- 승객 및 차량 데이터 정규화

### 2. **차량 시뮬레이션 (Vehicle Simulation)**
- 다양한 택시 대수 설정 가능
- 교대 근무 스케줄 시뮬레이션 지원
- 시간대별 운행 패턴 재현

### 3. **최적화 기반 배차 (Optimized Dispatch)**
- OR-Tools를 활용한 최적 배차 알고리즘
- 승객-차량 비용 행렬 기반 매칭
- MIP(Mixed Integer Programming) 기반 최적화

### 4. **결과 시각화 (Visualization)**
- 인터랙티브 대시보드 생성
- 시간대별 운행 현황 차트
- 지도 기반 공간 분석
- 차량 운행 효율성 분석

---

## 📁 프로젝트 구조

```
DTUMOS/
├── main.py                          # 메인 실행 스크립트
├── requirements.txt                 # Python 패키지 의존성
├── data/                           # 데이터 디렉토리
│   ├── etc/                        # 원본 데이터
│   │   ├── Seongnam_Taxi_20240418.csv
│   │   └── seongnam_boundary.geojson
│   └── agents/                     # 전처리된 에이전트 데이터
│       ├── passenger/              # 승객 데이터
│       └── vehicle/                # 차량 데이터
├── modules/                        # 핵심 모듈
│   ├── preprocess/                # 데이터 전처리
│   │   ├── passenger_preprocessor.py
│   │   ├── vehicle_preprocessor.py
│   │   └── data_preprocessor.py
│   ├── engine/                    # 시뮬레이션 엔진
│   │   ├── simulator.py          # 메인 시뮬레이터
│   │   ├── config_manager.py     # 설정 관리
│   │   ├── io_manager.py         # 입출력 관리
│   │   └── state_updater.py      # 상태 업데이트
│   ├── dispatch/                  # 배차 알고리즘
│   │   ├── dispatch_algorithms.py # 최적화 알고리즘
│   │   ├── cost_matrix.py        # 비용 행렬 계산
│   │   └── dispatch_flow.py      # 배차 흐름 제어
│   ├── routing/                   # 경로 계산
│   │   └── osrm_client.py        # OSRM 클라이언트
│   ├── analytics/                 # 분석 및 시각화
│   │   ├── dashboard.py          # 대시보드 생성
│   │   ├── service_charts.py     # 서비스 차트
│   │   ├── fleet_charts.py       # 차량 운영 차트
│   │   └── spatial_charts.py     # 공간 분석 차트
│   └── utils/                     # 유틸리티
│       └── distance_utils.py     # 거리 계산
└── visualization/                 # 시각화 리소스
    ├── dashboard/                 # 대시보드 HTML/JS
    └── simulation/                # 시뮬레이션 시각화
```

---

## 🔧 설치 방법

### 1. 저장소 클론
```bash
git clone <repository-url>
cd DTUMOS
```

### 2. 가상환경 생성 및 활성화 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### 3. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

---

## 💻 사용 방법

### 기본 실행

```bash
python main.py
```

### 주요 설정 파라미터 (main.py에서 수정)

```python
# 데이터 설정
BASE_DATE = "2024-04-18"              # 시뮬레이션 날짜
TIME_RANGE_START = 1080               # 시작 시간 (분 단위, 18:00)
TIME_RANGE_END = 1260                 # 종료 시간 (분 단위, 21:00)

# 차량 설정
NUM_TAXIS = 950                       # 시뮬레이션에 사용할 택시 수
USE_SHIFT = True                      # 교대 근무 시뮬레이션 여부
RANDOM_SEED = 42                      # 재현성을 위한 난수 시드

# 시뮬레이션 설정
base_configs['dispatch_mode'] = 'in_order'  # 배차 모드
base_configs['matrix_mode'] = 'haversine_distance'  # 거리 계산 방식
```

---

## ⚙️ 설정 옵션

### 배차 모드 (Dispatch Mode)
- `in_order`: 순차적 배차
- `optimization`: 최적화 기반 배차 (OR-Tools)

### 거리 계산 방식 (Matrix Mode)
- `haversine_distance`: Haversine 공식 기반 직선 거리
- `osrm`: OSRM 기반 실제 도로 거리

### 시간 설정
- 시간은 **분(minute) 단위**로 설정
- 예시:
  - `1080` = 18:00 (오후 6시)
  - `1260` = 21:00 (오후 9시)

---

## 📦 모듈 설명

### 1. **Preprocess (전처리 모듈)**
- `passenger_preprocessor.py`: 승객 데이터 전처리 및 필터링
- `vehicle_preprocessor.py`: 차량 데이터 생성 및 스케줄 설정
- `data_preprocessor.py`: 통합 데이터 전처리

**주요 기능:**
- 지역 경계 내 데이터 필터링
- 시간대별 데이터 크롭
- 교대 근무 스케줄 생성

### 2. **Engine (시뮬레이션 엔진)**
- `simulator.py`: 메인 시뮬레이션 로직
- `config_manager.py`: 설정 관리 및 검증
- `state_updater.py`: 승객/차량 상태 업데이트
- `io_manager.py`: 결과 저장 및 로드

**시뮬레이션 프로세스:**
1. 초기 데이터 로드
2. 시간 단위 반복 시뮬레이션
3. 승객 요청 처리
4. 차량 배차 및 상태 업데이트
5. 결과 기록 및 저장

### 3. **Dispatch (배차 알고리즘)**
- `dispatch_algorithms.py`: OR-Tools 기반 최적화
- `cost_matrix.py`: 승객-차량 간 비용 행렬 계산
- `dispatch_flow.py`: 배차 흐름 제어

**최적화 알고리즘:**
- MIP (Mixed Integer Programming) 기반
- 비용 최소화 목적함수
- 제약조건:
  - 각 차량은 최대 1명의 승객 배정
  - 각 승객은 정확히 1대의 차량 배정

### 4. **Analytics (분석 및 시각화)**
- `dashboard.py`: 대시보드 자동 생성
- `service_charts.py`: 서비스 지표 차트
- `fleet_charts.py`: 차량 운영 차트
- `spatial_charts.py`: 지도 기반 공간 분석

**생성되는 차트:**
- 시간대별 대기 승객 수
- 차량 가동률
- 서비스 성공/실패율
- 지역별 수요 히트맵

### 5. **Routing (경로 계산)**
- `osrm_client.py`: OSRM(Open Source Routing Machine) API 클라이언트

### 6. **Utils (유틸리티)**
- `distance_utils.py`: Haversine 거리 계산 등

---

## 📊 시각화

### 시뮬레이션 실행 후 결과 확인

```bash
# 1. HTML 대시보드 열기
open ./visualization/dashboard/assets/html/index_<simulation_name>.html

# 2. 또는 npm으로 인터랙티브 대시보드 실행
cd visualization/simulation
npm install
npm run dev
```

### 생성되는 결과 파일

```
simul_result/
└── scenario_base/
    └── <timestamp>/
        ├── passenger_marker.json    # 승객 마커 데이터
        ├── trip.json               # 운행 기록
        ├── record.csv              # 시뮬레이션 기록
        └── result.json             # 종합 결과
```

---

## 📝 요구사항

### Python 버전
- Python 3.8 이상

### 주요 패키지
- `pandas`: 데이터 처리
- `numpy`: 수치 계산
- `geopandas`: 지리 데이터 처리
- `folium`: 지도 시각화
- `plotly`: 인터랙티브 차트
- `ortools`: 최적화 알고리즘
- `osmnx`: 도로망 데이터
- `matplotlib`: 차트 생성

전체 패키지 목록은 `requirements.txt` 참조

---

## 🔍 주요 알고리즘

### OR-Tools 기반 배차 최적화

**목적함수 (Objective Function):**
```
Minimize: Σ cost[i,j] × x[i,j]
```

**제약조건 (Constraints):**
```
Σ x[i,j] ≤ 1  (각 차량 i는 최대 1명의 승객 배정)
j

Σ x[i,j] = 1  (각 승객 j는 정확히 1대의 차량 배정)
i
```

**비용 행렬 (Cost Matrix):**
- 차량과 승객 간의 거리 또는 시간
- Haversine 거리 또는 OSRM 경로 거리 사용

---

## 📖 시뮬레이션 프로세스

```
1. 데이터 로드
   ↓
2. 전처리 (승객/차량)
   ↓
3. 시뮬레이션 초기화
   ↓
4. [시간 루프]
   ├─ 새로운 승객 요청 추출
   ├─ 차량 상태 업데이트
   ├─ 배차 알고리즘 실행
   ├─ 승객-차량 매칭
   └─ 기록 저장
   ↓
5. 결과 분석 및 시각화
   ↓
6. 대시보드 생성
```

---

## 🎯 시뮬레이션 결과 지표

시뮬레이션은 다음 지표들을 기록합니다:

- **waiting_passenger_cnt**: 대기 중인 승객 수
- **fail_passenger_cnt**: 배차 실패 승객 수
- **empty_vehicle_cnt**: 빈 차량 수
- **driving_vehicle_cnt**: 운행 중인 차량 수
- **iter_time(second)**: 각 시간 단계의 실행 시간

---

## 🤝 기여 (Contributing)

버그 리포트, 기능 제안, Pull Request 환영합니다!

---

## 📄 라이센스 (License)

이 프로젝트의 라이센스는 저장소를 확인해주세요.

---

## 📧 문의 (Contact)

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해주세요.

---

## 🙏 감사의 말 (Acknowledgments)

- OSRM (Open Source Routing Machine)
- OR-Tools (Google Optimization Tools)
- 성남시 택시 데이터 제공처

---

**Last Updated**: 2024-04-18

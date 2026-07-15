---
name: travel-plan-builder
description: 검증된 리서치를 단일 HTML 인터랙티브 여행 계획서로 만든다. 날짜별 탭 + 타임라인 + Leaflet 지도 + 구간별 구글맵 길찾기 + 선택지 저장(localStorage) + KML 내보내기 패턴. "여행 계획서 작성/수정", "일정 UI 개선", "계획서 HTML" 요청 시 적용.
license: MIT
metadata:
  category: travel
  locale: ko-KR
  phase: v1
---

# 인터랙티브 여행 계획서 빌더

## 이 스킬이 하는 일

`travel-research` 스킬(또는 동등한 조사)의 결과를 **의존성 없는 단일 `index.html`**로 만든다.
구조·데이터 모델은 아래 명세를 그대로 따른다. (저장소에 완성된 예시 여행 폴더 `YYYYMM_지역명/index.html`이 있으면 그 파일 구조를 레퍼런스로 삼는다. 배포 키트에는 예시가 없을 수 있으니, 없으면 이 문서만으로 제작한다.)

## 절대 규칙 (데이터 무결성)

1. **확정 정보는 불변**: 항공편·기차·숙소·확정 예약(식당 등)은 사용자가 저장해 둔 값을 그대로 쓴다. 임의로 시간/역/주소를 바꾸지 않는다.
2. **단일 소스 원칙**: 같은 정보(기차 시간, 숙소 주소)가 페이지 여러 곳에 나오면 반드시 일치시킨다. 수정 전 기존 파일에서 불일치를 먼저 찾아 확정 정보 기준으로 통일한다.
3. 확정 항목에는 `확정` 배지를, 변경 가능한 항목에는 예약/대안 링크를 단다.
4. 모든 시간·요금에 "조사 기준일"을 명시한다.

## 기술 스택 (단일 파일, CDN만 사용)

- Tailwind CSS: `https://cdn.tailwindcss.com` (JS로 주입한 DOM도 JIT 적용됨)
- Leaflet 1.9.4 + 구글맵 타일: `https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}` (subdomains `mt0~mt3`)
- 폰트: Noto Sans KR
- 상태 저장: `localStorage` (체크리스트, 선택지) — 서버 불필요
- 로컬 확인: 저장소 루트의 `server.py` (`python server.py` 후 브라우저)

## 페이지 구조

```
<header>  여행 제목 · 기간 · "검증 기준일" 표기
<nav>     sticky 상단 칩 네비: [개요·예약] [패키지 비교] [D1 날짜(요일) 도시] ... [D7]
<main>
  ├─ 개요 탭: 전체 지도(도시 핀+이동 폴리라인) + KML 다운로드 버튼
  │           항공/기차/숙소 확정 카드 · 예약 우선순위 체크리스트(긴급도 색상+예약 버튼)
  │           교통권 전략 표 · 계절 팁 (일몰/더위/치안)
  ├─ 비교 탭: 여행사 패키지 vs 우리 일정 표 + 후기 분석 반영 문구
  └─ 날짜별 탭 (JS 렌더링): 아래 데이터 모델에서 자동 생성
<script>  DAYS 데이터 → 렌더링 → 지도 lazy init
```

## 핵심 데이터 모델 (JS)

일정은 HTML로 직접 쓰지 말고 **`DAYS` 배열 → 렌더 함수** 패턴으로 생성한다. 지도 핀·타임라인·길찾기가 한 소스에서 나와 불일치가 원천 차단된다.

```js
const DAYS = [{
  id:'d1', date:'8/8', dow:'토', city:'프라하', flag:'🇨🇿', color:'amber',
  title:'하루 컨셉', sunset:'20:35',           // 일몰시각 = 야경 일정의 근거
  note:'요일 주의사항 (일요일 미사, 월요일 휴관 등)',
  stops:[{
    t:'13:00', icon:'🏰', title:'프라하성',
    coord:[50.0903,14.4005],                    // 지도 핀 + 길찾기의 소스
    g:'Prague Castle',                          // 구글맵 검색 쿼리
    hl:true, badge:'예약 필수',                  // 하이라이트/배지
    move:{mode:'transit', label:'22번 트램 15분'}, // 이전 stop→현재 이동수단
    desc:'가격·팁·주의 (후기 근거 포함)',
    links:[{k:'book', label:'🎟️ 공식 예매', url:'...'},
           {k:'review', label:'⭐ 후기', url:'...'}]
  }],
  alts:[{tag:'예정 코스', title:'…', desc:'…'}]  // 선택지 카드 (클릭 저장)
}];
```

## 자동 생성 규칙

- **길찾기 버튼**: 연속된 두 stop의 좌표로 자동 생성 —
  `https://www.google.com/maps/dir/?api=1&origin={lat},{lng}&destination={lat},{lng}&travelmode={walking|transit|driving}`
- **스팟 지도 링크**: `https://www.google.com/maps/search/?api=1&query={encodeURIComponent(g)}`
- **일자별 지도**: 번호 원형 마커(`L.divIcon`) + 순서 폴리라인 + `fitBounds`. 같은 좌표 연속 중복은 폴리라인에서 생략
- **지도 초기화는 lazy**: 탭 최초 표시 때 `initDayMap()`, 재표시 때 `invalidateSize()` (숨긴 div에 초기화하면 깨짐 — 반드시 이 패턴)
- **선택지 카드**: 클릭 → `.selected` 토글 → `localStorage`에 저장. 체크리스트도 동일
- **인쇄 CSS**: `@media print`에서 nav 숨기고 전 탭 펼치고 지도 숨김

## 콘텐츠 작성 규칙

- 각 stop의 `desc`에 리서치 근거를 녹인다: 가격(현지통화+원화), 예약 사이트(공식만, 리셀러 경고), 혼잡 회피 시간대, 후기 한 줄
- 야경 일정은 일몰 시각 기준 "블루아워" 시간대를 명시
- 이동일은 역 이름을 정확히 (예: "빈 서역 — 중앙역 아님 주의!")
- 체크리스트는 긴급도순: `지금 즉시(빨강) → N주 내 → 출발 전`
- KML 파일(`travel_pins.kml`)을 일정과 동기화: 폴더=도시, 핀 설명에 날짜/팁 포함

## 검증 & 마무리

1. `<script>` 블록을 추출해 `node --check`로 문법 검증
2. 확정 정보(항공/기차/숙소)가 페이지 내 모든 위치에서 일치하는지 grep으로 확인
3. `AGENTS.md` 규칙에 따라 `git add . && git commit -m "의미 있는 메시지"`

## 완료 기준

- 단일 HTML로 열리고, 날짜 칩으로 하루씩 넘겨볼 수 있다
- 모든 연속 일정 구간에 길찾기 버튼이 있다
- 일자별 지도 번호와 타임라인 번호가 일치한다
- 확정 정보가 원본과 1글자도 다르지 않다
- 예약 체크리스트가 오늘 날짜 기준 긴급도로 정렬되어 있다

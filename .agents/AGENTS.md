# Travel 워크스페이스 공통 규칙 (모든 여행 폴더에 적용)

이 저장소는 여행별 폴더(`YYYYMM_지역명/`)로 구성된다. 루트 `index.html`은 여행 목록 허브다.

# Git Tracking Rule
웹페이지 소스코드(`index.html` 등)를 대규모로 수정하거나 기능이 완성될 때마다,
반드시 `git add .` 및 `git commit -m "의미 있는 커밋 메시지"` 후 `git push origin main`로 백업/트래킹한다.

# Skills (모든 AI 도구 공통 — Claude Code / Codex / Gemini 등)
여행 계획 작업은 아래 스킬 문서를 먼저 읽고 절차를 따른다.

| 스킬 | 경로 | 용도 |
|---|---|---|
| travel-research | `.agents/skills/travel-research/SKILL.md` | 필수 방문지 3-트랙 병렬 리서치 (여행사 패키지 / 실제 후기 / 공식 운영정보) |
| travel-plan-builder | `.agents/skills/travel-plan-builder/SKILL.md` | 단일 HTML 인터랙티브 계획서 (날짜 탭 + 지도 + 길찾기 + 선택 저장 + KML) |
| myrealtrip-search | `.agents/skills/myrealtrip-search/SKILL.md` | 마이리얼트립 MCP로 항공/숙소/투어 검색 + 날짜별 예약가능 조회 |

전체 워크플로우와 복붙용 프롬프트: 루트의 `여행계획_AI작업가이드.md` 참고.

# 새 여행 폴더 시작 절차
1. `YYYYMM_지역명/` 폴더 생성, `research/` 하위 폴더 준비
2. 확정 정보(항공·기차·숙소·확정 예약)를 사용자에게 받아 고정 — **절대 임의 변경 금지**
3. travel-research 스킬로 3-트랙 리서치 → `research/*.md` 기록
4. travel-plan-builder 스킬로 `index.html` + `travel_pins.kml` 생성
5. 루트 `index.html` 허브에 여행 카드 추가 (커버 이미지 포함)
6. git 커밋 + 푸시

# 핵심 불변 규칙
- 확정 정보는 저장된 값 그대로 사용, 문서 내 모든 위치에서 일치시킬 것
- 모든 조사 결과에 조사일과 출처 URL을 남길 것
- 링크는 실접속 검증된 것만, 투어는 해당 날짜 예약 가능 확인된 것만 게재

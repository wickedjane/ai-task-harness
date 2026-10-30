# 새 작업 환경에서 가져갈 기능

기본은 기존 interview → scope → verify → explain 흐름이다. 아래 보조 스킬은 해당 상황에서만 읽는다. 한 번에 전부 로드하거나 설치하지 않는다.

| 필요 시점 | 자료 | 얻을 결과 |
|---|---|---|
| 첫 접속, 실행 도구가 낯설 때 | `skill-library/environment-preflight/SKILL.md` | 실제 가능한 도구·실행·미리보기 경로 확인 |
| 범위 확정 직후 | `templates/ACCEPTANCE.md` | 요구사항과 통과 조건을 연결 |
| UI를 구현할 때 | `templates/SCREEN_STATES.md` | 정상·로딩·빈 상태·오류·재시도 설계 |
| 기능이 돌아가기 시작했을 때 | `skill-library/edge-case-review/SKILL.md` | 재현 가능한 예외·결함 목록 |
| CSV/JSON/표 데이터가 제공됐을 때 | `skill-library/data-check/SKILL.md` | 필드·결측·중복·단위·집계 근거 확인 |
| 분류·추출·요약 등 AI 출력이 제품 기능일 때 | `skill-library/ai-output-check/SKILL.md` | 입출력 계약과 작게 고정한 평가 사례 |
| 도구 추가를 검토할 때 | `guides/MCP_CATALOG.md`, `templates/TOOL_CHECK.md` | 설치 필요·외부 통신·실제 호출 여부 판단 |
| 작업 지시·세션 재개 기준을 정할 때 | `guides/PROMPTING_AND_STATE.md` | 목표·완료 조건·핵심 업무 상태 |
| 독립 작업을 나눠 맡길 때 | `skill-library/parallel-task-coordination/SKILL.md`, `guides/SUBAGENTS.md` | 역할·파일 소유권·결과 통합 |
| 반복 작업용 스킬을 만들 때 | `templates/SKILL.md.template` | 목적·입력·완료 기준이 짧은 스킬 |

## 적용 방법

저장소를 clone한 뒤 코딩 에이전트에게 필요한 파일 경로를 명시적으로 읽히면 된다. `skill-library/`는 이식용 묶음이며 clone만으로 자동 발견되지 않는다. 자동 설치가 필요한 경우 대상 도구의 공식 경로·권한을 확인한다. 관리형 환경의 전역 설정이나 운영 영역을 수정하지 않는다.

## 작은 규모로 유지할 것

- 기본 도구로 실제 수행이 되면 MCP를 추가하지 않는다. 설치·인증 비용보다 얻는 시간이 커야 한다.
- 별도 에이전트는 독립 조사·구현·검토가 가능하고 환경이 지원할 때 쓴다. 지원하지 않으면 같은 세션에서 근거를 다시 읽어 검토하고 독립 검토였다고 말하지 않는다.
- 대형 PRD·슬라이드·외부 위키 게시·배포·다중 에이전트 오케스트레이터는 과제가 요구할 때만 도입한다.
- AI 기능을 만드는 것과 AI로 개발하는 것은 다르다. 앱 자체가 모델을 호출해야 한다면 제공된 실행 경로부터 확인하고 개인 API 키가 필요하다고 가정하지 않는다.

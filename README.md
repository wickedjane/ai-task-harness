# AI Task Harness

180분 실무형 과제의 요구 확인 → 구현 → 검증 → 제출 전 이해 점검을 돕는 작은 지침 모음입니다. 공식 시험 자료나 문제·정답이 아닙니다.

## 시작

공개 저장소 반입이 허용된 **응시 환경 안의 코딩 에이전트**에게 다음과 같이 요청합니다. 공개 저장소이므로 GitHub 로그인은 필요 없습니다.

> https://github.com/wickedjane/ai-task-harness 를 참고용 하위 폴더에 clone해 줘. 하네스의 AGENTS.md와 PLAN.md를 읽고, 과제 원문과 기존 지침을 우선해서 적용해 줘. 실제 마감과 남은 시간을 먼저 확인하고, 필요한 단계 문서만 읽어 줘. 실제 과제 코드는 원래 작업 공간에 작성해 줘.

에이전트가 실행할 명령 예시:

```sh
git clone --depth 1 https://github.com/wickedjane/ai-task-harness.git ai-task-harness
```

같은 폴더가 이미 있으면 내용을 확인하고 덮어쓰지 않습니다. clone만으로 지침이 자동 적용된다고 가정하지 않고 `ai-task-harness/AGENTS.md`와 `ai-task-harness/PLAN.md`를 명시적으로 읽힙니다. 외부 브라우저 접속·개인 파일 업로드를 요구하지 않습니다. 반입이 차단되면 우회 설치에 시간을 쓰지 말고 과제 원문과 제공 도구로 진행합니다.

## 필요한 것만 읽기

| 문서 | 읽는 때 |
|---|---|
| AGENTS.md · PLAN.md | 시작할 때: 작업 원칙과 시간 배분 |
| skills/interview.md · scope.md | 요구사항 확인과 범위 결정 |
| skills/verify.md | 실제 실행과 요구사항 대조 |
| skills/explain.md | 설계 결정·핵심 기능 완성 때 이해 점검, 제출 전 직접 설명 연습 |
| templates/의 요구사항·설계/결정·검증/한계 양식 3개 | 아키텍처·대안·절충·데이터 부족·실행 근거를 기록할 틀이 필요할 때만 |
| skill-library/frontend-delivery/SKILL.md | 역할별 실제 화면·입출력 계약·디자인·폼 상태·권한·통합 검증 |
| skill-library/evaluation-design/SKILL.md | 문제 유형별 지표·기준안 비교·차트·검증 한계 |
| guides/OPTIONAL_TOOLS.md | 원본 디자인 플러그인이나 추가 도구가 필요할 때만 |
| templates/EVALUATION.md | 평가 기준과 실제 비교 결과를 기록할 틀이 필요할 때 |
| scripts/compare_runs.py | 집계한 실행 결과 CSV로 비교표·절충 산점도를 만들 때 |
| skill-library/data-check/SKILL.md | 데이터 정제·SQL 집계·분석·보고서: 결측·조인·지표·검산·재현 |
| skill-library/ai-output-check/SKILL.md | 제품 기능에 모델 출력이 있을 때: 출력 계약·고정 사례·품질 비교 |
| skill-library/parallel-task-coordination/SKILL.md | 서브에이전트나 별도 터미널로 독립 작업을 나누고 통합할 때 |

총 20개 파일이며 기본으로 읽는 것은 2개입니다. 과제를 읽은 뒤 해당하는 보조 스킬만 추가로 읽습니다. 평가 보고서 도구는 Python 표준 라이브러리만 사용합니다. MCP·모델·역할 설정은 없습니다. 절차 문서와 선택 스킬은 필요할 때 파일을 직접 읽으면 되며 설치하지 않아도 됩니다. 보조 스킬은 자체 작성물입니다.

데이터·AI 출력 스킬은 일반 개발 절차에서 놓치기 쉬운 검증 기준이 있어 포함했습니다. 환경 점검·예외 재현·화면 상태·통과 기준은 기존 단계 문서에 통합했습니다. 원본 플러그인은 선택 가이드에 출처·용도·조건만 안내하고 코드·자산을 포함하거나 자동 설치하지 않습니다. 커스텀 역할 TOML과 중복 양식은 포함하지 않습니다.

## 평가 보고서 예제

아래는 실제 성능을 주장하지 않는 합성 CSV로 형식을 확인하는 예제입니다. 하네스 루트에서 실행합니다.

```sh
python3 scripts/compare_runs.py examples/runs.synthetic.csv --baseline base --metric cost:min --metric quality:max --output /tmp/evaluation-example.html
```

결과는 외부 통신 없는 HTML로 저장됩니다. 파일 미리보기가 지원되지 않으면 같은 폴더를 제공 환경에서 허용한 로컬 서버로 열거나 표를 확인합니다. 실제 과제에서는 측정한 CSV와 새 출력 경로를 사용합니다. 이 도구는 AUC 계산기나 제약 검증기가 아니며, 원본 실행에서 계산한 지표를 비교합니다. CSV 형식과 지표 선택은 evaluation-design 스킬에 있습니다.

도구 검증: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

템플릿은 필수 제출물이 아닙니다. 기존 과제 README·AGENTS.md·공식 양식을 유지하고 필요한 기록만 통합합니다. 후속 평가 시간·문항 수·규칙은 실제 안내를 따릅니다. AI 금지 후속 평가에서는 직접 답합니다.

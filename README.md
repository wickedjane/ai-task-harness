# AI Task Harness

AI와 실무형 과제를 수행할 때 요구 확인 → 범위 결정 → 구현 → 검증 → 설명을 돕는 한국어 Markdown 지침 모음입니다. 특정 시험의 공식 자료나 문제·정답을 제공하지 않습니다.

## 구성
- `AGENTS.md`: 작업 순서와 기록 원칙
- `PLAN.md`: 180분 작업 배분 예시
- `skills/`: interview, scope, verify, explain 절차 문서
- `templates/`: 요구사항·결정·검증·결과물 설명의 빈 양식
- `guides/CAPABILITY_MENU.md`: 새 환경에서 필요한 보조 기능 선택표
- `guides/MCP_CATALOG.md`: MCP 후보·도입 조건·공식 출처
- `skill-library/`: 환경 점검·예외 검토·데이터 점검·AI 출력 평가의 이식용 SKILL.md
- `mcp/`: 비활성 상태로 보관하는 설정 예시. 자동 적용하지 않습니다.
- `guides/PROMPTING_AND_STATE.md`: 작업 계약·업무 상태·완료 판단
- `guides/SUBAGENTS.md`: 공식 기능과 개인 운영 방식, 역할 분담·병렬화 예시
- `role-examples/`: 자동 활성화되지 않는 커스텀 역할 TOML 3종

## 사용
공개 자료 반입이 허용된 작업 환경 안에서 저장소를 가져옵니다. 아래 명령은 새 `ai-task-harness` 하위 폴더를 만듭니다. 같은 이름의 폴더가 이미 있으면 내용을 확인하고 다른 새 경로를 사용하세요.

```sh
git clone --depth 1 https://github.com/wickedjane/ai-task-harness.git ai-task-harness
```

제공된 코딩 에이전트에게 `ai-task-harness/AGENTS.md`와 `ai-task-harness/PLAN.md`를 읽고 적용하도록 요청합니다. clone 전에 시작한 에이전트가 하위 폴더 지침을 자동 적용한다고 가정하지 않습니다. 경로는 에이전트의 현재 작업 폴더에 맞춥니다.

템플릿은 필요한 부분만 실제 작업 문서에 옮깁니다. 기존 과제 README·AGENTS.md·코드를 덮어쓰지 않습니다. 필수 파일명과 작성 양식은 과제 안내가 우선입니다. 내려받은 저장소는 참고용으로 유지하고 실제 과제 코드는 원래 작업 공간에서 작성합니다.

`skills/*.md`는 직접 읽는 절차 문서이며 자동 등록되는 CLI 명령이나 설치형 스킬이 아닙니다. 공개 자료 사용 허용 여부는 해당 환경의 규정을 확인하세요. 이 묶음은 외부 서비스·개인 API 키를 요구하지 않으며 파일 외부 전송이나 push를 실행하는 스크립트가 없습니다.
`skill-library/*/SKILL.md`는 이름·설명이 있는 재사용 스킬입니다. clone만으로 등록되지 않으므로 필요한 파일을 명시적으로 읽히거나 대상 도구가 허용한 설치 방식을 따릅니다. 새 스킬용 빈 양식은 `templates/SKILL.md.template`입니다.
서브에이전트를 쓰려면 먼저 `guides/SUBAGENTS.md`를 읽힙니다. 새 환경에서 역할 파일을 복사하거나 기능을 강제로 켜지 않고, 제공 기능·허용 모델을 확인한 뒤 선택적으로 적용합니다. 병렬 운영 스킬은 이 저장소의 자체 작성물이며 OpenAI 공식 배포 스킬이 아닙니다.

## 설명 연습
실제 후속 평가 전에만 AI와 구조·선택 이유·검증·한계를 점검합니다. AI 금지 평가가 시작되면 스스로 답하며 이 지침을 답안 생성에 사용하지 않습니다.

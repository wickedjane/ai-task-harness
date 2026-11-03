"""Compare already-measured runs; no dependencies, network, or metric fabrication."""
import argparse
import csv
from html import escape
import math
from pathlib import Path

META = ('data_version', 'constraint_set', 'metric_definition', 'evidence_kind')
REQUIRED = ('run_id', 'method', 'valid', 'runtime_seconds') + META


def parse_metrics(specs):
    result = []
    for spec in specs:
        name, sep, direction = spec.rpartition(':')
        if not sep or not name or direction not in ('min', 'max'):
            raise ValueError('Use --metric COLUMN:min or COLUMN:max')
        if name in REQUIRED or any(n == name for n, _ in result):
            raise ValueError('Metric column is reserved or duplicated: ' + name)
        result.append((name, direction))
    if not result:
        raise ValueError('At least one metric is required')
    return result


def read_runs(path, metrics):
    rows = []
    seen = set()
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        required = set(REQUIRED) | {n for n, _ in metrics}
        if len(headers) != len(set(headers)) or not required.issubset(headers):
            raise ValueError('Missing or duplicate CSV columns: ' + ', '.join(sorted(required - set(headers))))
        for line, row in enumerate(reader, 2):
            if None in row or any(row.get(k) is None or not row[k].strip() for k in required):
                raise ValueError(f'Row {line}: missing values or extra cells')
            row = {k: v.strip() if v is not None else '' for k, v in row.items()}
            if row['run_id'] in seen:
                raise ValueError('Duplicate run_id: ' + row['run_id'])
            seen.add(row['run_id'])
            if row['valid'] not in ('true', 'false'):
                raise ValueError(f'Row {line}: valid must be true or false')
            if row['evidence_kind'] not in ('measured', 'synthetic'):
                raise ValueError(f'Row {line}: evidence_kind must be measured or synthetic')
            for key in ['runtime_seconds'] + [n for n, _ in metrics]:
                try:
                    value = float(row[key])
                except ValueError as exc:
                    raise ValueError(f'Row {line}: {key} must be numeric') from exc
                if not math.isfinite(value):
                    raise ValueError(f'Row {line}: {key} must be finite')
                if key == 'runtime_seconds' and value < 0:
                    raise ValueError(f'Row {line}: runtime_seconds must be nonnegative')
                row[key] = value
            row['valid'] = row['valid'] == 'true'
            rows.append(row)
    if not rows:
        raise ValueError('CSV has no runs')
    if len({tuple(r[k] for k in META) for r in rows}) != 1:
        raise ValueError('Comparison requires matching data_version, constraint_set, metric_definition and evidence_kind')
    return rows


def pareto_ids(rows, metrics):
    """Observed nondominated valid runs, using only the specified metrics."""
    candidates = [r for r in rows if r['valid']]

    def dominates(a, b):
        av = [a[n] if d == 'min' else -a[n] for n, d in metrics]
        bv = [b[n] if d == 'min' else -b[n] for n, d in metrics]
        return all(x <= y for x, y in zip(av, bv)) and any(x < y for x, y in zip(av, bv))

    return {r['run_id'] for r in candidates if not any(dominates(other, r) for other in candidates)}


def number(value):
    return f'{value:.6g}'


def scatter(rows, metrics, frontier):
    if len(metrics) != 2:
        return '<p>절충 산점도는 지표를 정확히 두 개 지정하면 표시합니다.</p>'
    points = [r for r in rows if r['valid']]
    (xname, xd), (yname, yd) = metrics
    xmin, xmax = min(r[xname] for r in points), max(r[xname] for r in points)
    ymin, ymax = min(r[yname] for r in points), max(r[yname] for r in points)
    xspan, yspan = xmax - xmin, ymax - ymin
    if not math.isfinite(xspan) or not math.isfinite(yspan):
        raise ValueError('Metric range is too large to plot')

    def position(value, low, span, start, width):
        return start + width * ((value - low) / span if span else 0.5)

    marks = []
    for row in points:
        x = position(row[xname], xmin, xspan, 100, 500)
        y = position(row[yname], ymin, yspan, 340, -260)
        is_frontier = row['run_id'] in frontier
        label = escape(row['run_id'])
        tooltip = escape(f"{row['run_id']}: {xname}={number(row[xname])}, {yname}={number(row[yname])}")
        shape = (f'<rect x="{x-5:.2f}" y="{y-5:.2f}" width="10" height="10" fill="#0f766e"/>'
                 if is_frontier else f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#64748b"/>')
        marks.append(f'<g><title>{tooltip}</title>{shape}<text x="{x+9:.2f}" y="{y-9:.2f}">{label}</text></g>')
    return f'''<svg viewBox="0 0 800 430" role="img" aria-labelledby="chart-title chart-desc">
<title id="chart-title">유효한 후보의 절충 산점도</title>
<desc id="chart-desc">사각형은 표시한 두 지표에서 관측된 비지배 후보입니다. 모든 수치는 아래 표에서도 확인할 수 있습니다.</desc>
<path d="M80 55 V360 H640" fill="none" stroke="#334155"/>
<text x="350" y="410" text-anchor="middle">{escape(xname)} ({xd})</text>
<text x="18" y="220" transform="rotate(-90 18 220)" text-anchor="middle">{escape(yname)} ({yd})</text>
<text x="100" y="385" text-anchor="middle">{number(xmin)}</text>
<text x="600" y="385" text-anchor="middle">{number(xmax)}</text>
<text x="72" y="344" text-anchor="end">{number(ymin)}</text>
<text x="72" y="84" text-anchor="end">{number(ymax)}</text>
{''.join(marks)}</svg>'''


def render(rows, metrics, baseline_id):
    matches = [r for r in rows if r['run_id'] == baseline_id]
    if not matches or not matches[0]['valid']:
        raise ValueError('Baseline must exist and be valid')
    baseline = matches[0]
    frontier = pareto_ids(rows, metrics)
    body = []
    for row in rows:
        cells = [escape(row['run_id']), escape(row['method']), '유효' if row['valid'] else '무효 — 비교 제외', number(row['runtime_seconds'])]
        for name, direction in metrics:
            cells.append(number(row[name]))
            delta = baseline[name] - row[name] if direction == 'min' else row[name] - baseline[name]
            if not math.isfinite(delta):
                raise ValueError('Metric delta is too large to compare')
            cells.append(number(delta) if row['valid'] else '비교 제외')
        cells.append('관측된 비지배 후보' if row['run_id'] in frontier else '—')
        body.append('<tr>' + ''.join('<td>' + c + '</td>' for c in cells) + '</tr>')
    headers = ['실행', '방법', '유효성', '시간(초)']
    for name, direction in metrics:
        headers.extend([f'{name} ({direction})', '기준안 대비 개선량 (+가 개선)'])
    headers.append('지정한 지표 내 비교')
    meta = ' · '.join(f'{key}: {baseline[key]}' for key in META)
    synthetic = baseline['evidence_kind'] == 'synthetic'
    banner = ('합성 예제 — 실제 성능이나 평가 결과가 아닙니다.' if synthetic
              else '입력 CSV에 실측으로 표시된 결과입니다. 이 도구는 원본 실행·제약 충족을 독립 검증하지 않습니다.')
    return f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>실행 결과 비교</title><style>
body{{font-family:system-ui,sans-serif;color:#172033;background:#f8fafc;margin:0;padding:24px;line-height:1.6}}
main{{max-width:1100px;margin:auto}} .note{{border-left:4px solid #0f766e;padding:12px;background:#fff}}
.table{{overflow:auto}} table{{border-collapse:collapse;background:#fff;width:100%}} th,td{{border:1px solid #cbd5e1;padding:9px;text-align:left}}
svg{{width:100%;max-width:900px;background:#fff}} svg text{{font:13px system-ui;fill:#172033}} code{{overflow-wrap:anywhere}}
</style><main><h1>실행 결과 비교</h1><p class="note">{banner}</p>
<p>기준안: <strong>{escape(baseline_id)}</strong></p><p><code>{escape(meta)}</code></p>
<p>min은 작을수록, max는 클수록 좋습니다. 개선량은 원래 지표 단위의 차이이며 비율이 아닙니다.</p>
{scatter(rows, metrics, frontier)}
<p>사각형: 표시한 두 지표에서 관측된 비지배 후보. 원: 그 외 유효 후보. 독립 실행을 연결한 수렴 곡선이 아니며 전역 최적성·통계적 유의성을 증명하지 않습니다.</p>
<div class="table"><table><thead><tr>{''.join('<th scope="col">'+escape(h)+'</th>' for h in headers)}</tr></thead><tbody>{''.join(body)}</tbody></table></div>
<p>원본 데이터·제약·지표 정의와 실행 환경을 직접 확인하세요. 무효 후보는 개선 비교·산점도·파레토 판단에서 제외합니다. 시간은 지정 지표의 파레토 계산에 포함되지 않습니다. 정확히 두 지표인 경우에만 산점도를 표시합니다.</p>
</main></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--metric', action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        if args.csv_file.resolve() == args.output.resolve():
            raise ValueError('Output must not overwrite the source CSV')
        if args.output.is_symlink():
            raise ValueError('Output must not be a symlink')
        metrics = parse_metrics(args.metric)
        rows = read_runs(args.csv_file, metrics)
        report = render(rows, metrics, args.baseline)
        with args.output.open('w' if args.overwrite else 'x', encoding='utf-8') as out:
            out.write(report)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(2, f'Error: {exc}\n')
    print(f'Wrote {args.output}: {len(rows)} runs; evidence={rows[0]["evidence_kind"]}')


if __name__ == '__main__':
    main()

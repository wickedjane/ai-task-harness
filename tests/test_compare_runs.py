import csv
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('compare_runs', ROOT / 'scripts/compare_runs.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompareRunsTest(unittest.TestCase):
    def setUp(self):
        self.metrics = MODULE.parse_metrics(['cost:min', 'quality:max'])
        self.example = ROOT / 'examples/runs.synthetic.csv'
        with self.example.open() as stream:
            self.raw = list(csv.DictReader(stream))

    def load_modified(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'runs.csv'
            with path.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(self.raw[0]))
                writer.writeheader()
                writer.writerows(rows)
            return MODULE.read_runs(path, self.metrics)

    def test_pareto_uses_both_directions_and_excludes_invalid(self):
        rows = MODULE.read_runs(self.example, self.metrics)
        self.assertEqual(MODULE.pareto_ids(rows, self.metrics), {'candidate-a', 'candidate-b'})

    def test_tied_valid_runs_both_remain(self):
        rows = MODULE.read_runs(self.example, self.metrics)
        rows.append(dict(rows[1], run_id='tie'))
        self.assertIn('tie', MODULE.pareto_ids(rows, self.metrics))

    def test_different_evaluation_conditions_rejected(self):
        for key in MODULE.META:
            with self.subTest(key=key):
                changed = [dict(r) for r in self.raw]
                changed[1][key] = 'measured' if key == 'evidence_kind' else 'other'
                with self.assertRaises(ValueError):
                    self.load_modified(changed)

    def test_missing_nan_infinite_and_duplicate_rejected(self):
        for bad in ['', 'nan', 'inf', '-inf', 'unknown']:
            with self.subTest(bad=bad):
                changed = [dict(r) for r in self.raw]
                changed[1]['cost'] = bad
                with self.assertRaises(ValueError):
                    self.load_modified(changed)
        with self.assertRaises(ValueError):
            self.load_modified(self.raw + [self.raw[0]])

    def test_invalid_baseline_rejected(self):
        rows = MODULE.read_runs(self.example, self.metrics)
        for baseline in ['invalid', 'missing']:
            with self.assertRaises(ValueError):
                MODULE.render(rows, self.metrics, baseline)

    def test_html_escape_and_synthetic_disclosure(self):
        rows = MODULE.read_runs(self.example, self.metrics)
        rows[1]['method'] = '<script>alert(1)</script>'
        html = MODULE.render(rows, self.metrics, 'base')
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('합성 예제', html)
        self.assertIn('<svg', html)

    def test_equal_and_zero_values_plot_without_division_error(self):
        rows = MODULE.read_runs(self.example, self.metrics)
        for row in rows:
            row.update(cost=0, quality=0)
        html = MODULE.render(rows, self.metrics, 'base')
        self.assertNotIn('nan', html)
        self.assertIn('<svg', html)

    def test_invalid_metric_specifications(self):
        for specs in [[], ['cost'], ['cost:bad'], ['cost:min', 'cost:max'], ['run_id:min']]:
            with self.assertRaises(ValueError):
                MODULE.parse_metrics(specs)

    def test_improvement_direction_and_invalid_exclusion(self):
        rows = MODULE.read_runs(self.example, self.metrics)
        html = MODULE.render(rows, self.metrics, 'base')
        self.assertIn('<td>80</td><td>20</td><td>70</td><td>10</td>', html)
        self.assertIn('<td>40</td><td>비교 제외</td><td>99</td><td>비교 제외</td>', html)

    def test_single_metric_has_table_without_tradeoff_chart(self):
        metrics = MODULE.parse_metrics(['quality:max'])
        rows = MODULE.read_runs(self.example, metrics)
        self.assertNotIn('<svg', MODULE.render(rows, metrics, 'base'))
        self.assertEqual(MODULE.pareto_ids(rows, metrics), {'candidate-b'})

    def test_negative_time_and_invalid_boolean_rejected(self):
        for key, value in [('runtime_seconds', '-1'), ('valid', 'yes')]:
            changed = [dict(r) for r in self.raw]
            changed[1][key] = value
            with self.assertRaises(ValueError):
                self.load_modified(changed)

    def test_cli_preserves_existing_output_and_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'report.html'
            cmd = [sys.executable, str(ROOT / 'scripts/compare_runs.py'), str(self.example),
                   '--baseline', 'base', '--metric', 'cost:min', '--metric', 'quality:max', '--output', str(out)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            out.write_text('keep me')
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
            self.assertEqual(out.read_text(), 'keep me')
            self.assertEqual(subprocess.run(cmd + ['--overwrite'], capture_output=True).returncode, 0)
            original = self.example.read_bytes()
            cmd[-1] = str(self.example)
            self.assertEqual(subprocess.run(cmd + ['--overwrite'], capture_output=True).returncode, 2)
            self.assertEqual(self.example.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()

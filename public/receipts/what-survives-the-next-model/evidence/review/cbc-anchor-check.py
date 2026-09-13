"""Audit saved CBC human-anchor margins without rerunning author experiments."""
import csv
import json
from collections import Counter
from pathlib import Path

sample_path = Path(__file__).with_name('cbc-anchor-sample.csv')
with sample_path.open() as handle:
    rows = list(csv.DictReader(handle))
raw = [float(row['raw_margin']) for row in rows]
corrected = [float(row['cbc_margin']) for row in rows]
flips = [row for row, a, b in zip(rows, raw, corrected) if (a > 0) != (b > 0)]
result = {
    'source_commit': '37d500566b0b7a7701a1ca199fafc467f2612587',
    'rows': len(rows),
    'raw_agreement': sum(value > 0 for value in raw) / len(rows),
    'corrected_agreement_strict_gt_zero': sum(value > 0 for value in corrected) / len(rows),
    'changed_verdicts': len(flips),
    'all_changed_verdicts_had_raw_margin_zero': all(float(row['raw_margin']) == 0 for row in flips),
    'changed_corrected_margins': dict(Counter(row['cbc_margin'] for row in flips)),
    'corrected_agreement_tolerance_1e_12': sum(value > 1e-12 for value in corrected) / len(rows),
    'positive_counts_by_tolerance': {
        str(tol): {'raw':sum(value > tol for value in raw), 'corrected':sum(value > tol for value in corrected)}
        for tol in [1e-16, 1e-15, 1e-14, 1e-13, 1e-12, 1e-11, 1e-10]
    },
    'large_margin_changes': sum(abs(a-b) > 1e-12 for a,b in zip(raw,corrected)),
}
assert len(rows) == 700
assert len(flips) == 55
assert result['all_changed_verdicts_had_raw_margin_zero']
assert all(0 < float(row['cbc_margin']) < 1e-12 for row in flips)
assert result['raw_agreement'] == result['corrected_agreement_tolerance_1e_12']
assert all(counts['raw'] == counts['corrected'] == 481 for counts in result['positive_counts_by_tolerance'].values())
text = json.dumps(result, indent=2)
Path(__file__).with_name('cbc-anchor-check.json').write_text(text + '\n')
print(text)

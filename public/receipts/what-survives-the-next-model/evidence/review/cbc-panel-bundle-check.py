"""Check saved CBC tie flips against a pinned evaluator panel; no network calls."""
import argparse
import csv
import gzip
import hashlib
import io
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


AUTHOR_REVISION = '37d500566b0b7a7701a1ca199fafc467f2612587'
PANEL_BLOB_SHA1 = '047fc2ce03acd4115675caf76d9ed529811de3af'
PANEL_SHA256 = 'c2615f257fd1ccf7277c093f65fea483435689aa564fec57f313f58f6664bf5f'
SAMPLE_SHA256 = '163c3359bfc69c88aa45cdce930c284544f2b4b385ccbf96edf7cd846058634c'
KEYS = ('item_id', 'item_numeric_id', 'subset', 'language')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_rows(data):
    return list(csv.DictReader(io.StringIO(data.decode('utf-8'))))


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--panel', type=Path, default=base / 'cbc-pinned-complete-panel.csv.gz')
    parser.add_argument('--sample', type=Path, default=base / 'cbc-anchor-sample.csv')
    parser.add_argument('--output', type=Path, default=base / 'cbc-panel-bundle-check.json')
    args = parser.parse_args()

    stored = args.panel.read_bytes()
    panel_bytes = gzip.decompress(stored) if stored.startswith(b'\x1f\x8b') else stored
    sample_bytes = args.sample.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(panel_bytes)).encode() + b'\0' + panel_bytes).hexdigest()
    require(blob == PANEL_BLOB_SHA1, 'Panel does not match the pinned author Git blob.')
    require(hashlib.sha256(panel_bytes).hexdigest() == PANEL_SHA256, 'Panel SHA-256 mismatch.')
    require(hashlib.sha256(sample_bytes).hexdigest() == SAMPLE_SHA256, 'Anchor sample SHA-256 mismatch.')
    panel, sample = read_rows(panel_bytes), read_rows(sample_bytes)
    require(len(panel) == 52500 and len(sample) == 700, 'Unexpected pinned row counts.')
    groups = defaultdict(list)
    for row in panel:
        groups[tuple(row[k] for k in KEYS)].append(row)
    backbones = sorted({row['evaluator_model'] for row in panel})
    require(len(backbones) == 5, 'Expected five evaluators.')

    def verdict(row, field):
        return Fraction(row[field]) > 0

    flips = [row for row in sample if verdict(row, 'raw_margin') != verdict(row, 'cbc_margin')]
    require(len(flips) == 55, 'Expected 55 strict-positive verdict flips.')
    details = []
    for row in flips:
        cells = groups[tuple(row[k] for k in KEYS)]
        require(sorted(cell['evaluator_model'] for cell in cells) == backbones,
                'A flipped item lacks a complete five-evaluator panel.')
        require(all(cell['margin'] and cell['chosen_score'] and cell['rejected_score'] for cell in cells),
                'A flipped item has a missing source score or margin.')
        margins = [Fraction(cell['margin']) for cell in cells]
        require(all(Fraction(cell['chosen_score']) - Fraction(cell['rejected_score']) == margin
                    for cell, margin in zip(cells, margins)), 'A source margin disagrees with its scores.')
        require(all(value.denominator == 1 for value in margins) and sum(margins) == 0,
                'A flipped source panel is not an exact integer zero-sum tie.')
        require(Fraction(row['raw_margin']) == 0 and 0 < Fraction(row['cbc_margin']) < Fraction('1e-16'),
                'A flipped saved margin falls outside the recorded tie/residue bounds.')
        details.append({**{k: row[k] for k in KEYS}, 'panel_size': len(cells),
                        'integer_margins': [int(value) for value in margins], 'exact_margin_sum': '0'})

    exceptions = []
    for row in sample:
        if abs(Fraction(row['raw_margin']) - Fraction(row['cbc_margin'])) <= Fraction('1e-12'):
            continue
        cells = groups[tuple(row[k] for k in KEYS)]
        present = [cell for cell in cells if cell['margin']]
        missing = [cell['evaluator_model'] for cell in cells if not cell['margin']]
        require(sorted(cell['evaluator_model'] for cell in cells) == backbones and len(present) == 4,
                'A larger difference does not have exactly one missing evaluator margin.')
        mean = sum(Fraction(cell['margin']) for cell in present) / len(present)
        require(mean == Fraction(row['raw_margin']), 'Available margins do not reproduce the saved raw mean.')
        require(verdict(row, 'raw_margin') == verdict(row, 'cbc_margin'), 'A larger difference flips a verdict.')
        exceptions.append({**{k: row[k] for k in KEYS}, 'saved_raw_margin': row['raw_margin'],
                           'saved_cbc_margin': row['cbc_margin'], 'nonmissing_margin_count': len(present),
                           'missing_backbones': missing, 'exact_raw_mean_of_available': str(mean),
                           'correctness_changed': False})
    require(len(exceptions) == 3, 'Expected three larger saved margin differences.')
    result = {
        'author_repository_revision': AUTHOR_REVISION,
        'pinned_panel_url': 'https://github.com/KurbanIntelligenceLab/multilingual-judge-calibration/blob/'
                            + AUTHOR_REVISION + '/data/external_validation/mrewardbench_panel/analysis_1500_item/pilot_complete_panel.csv',
        'decompressed_panel_size_bytes': len(panel_bytes),
        'decompressed_panel_git_blob_sha1': blob,
        'decompressed_panel_sha256': PANEL_SHA256,
        'anchor_sample_sha256': SAMPLE_SHA256,
        'panel_rows': len(panel),
        'anchor_rows': len(sample),
        'expected_backbones': backbones,
        'flipped_rows': len(flips),
        'all_flips_have_complete_nonmissing_five_evaluator_panels': True,
        'all_flipped_source_margins_are_integer_chosen_minus_rejected': True,
        'all_flipped_source_margin_sums_are_exactly_zero': True,
        'all_flipped_saved_raw_margins_are_zero_and_corrected_margins_below_1e_minus_16': True,
        'large_margin_difference_rows': exceptions,
        'flipped_item_details': details,
        'scope': 'Pinned saved-data verification; no model-score collection or provider calls rerun. '
                 'The cause of missing provider scores is not established.',
    }
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'flipped_item_details'}, indent=2))


if __name__ == '__main__':
    main()

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist():
    for rel in ['README.md', 'LICENSE', 'requirements.txt', 'AGENTS.md', 'scripts/check_deck_static.py', 'templates/atlas_simulation/electrical_iv_atlas.in.j2', 'data/silvaco_examples_index.public.json', 'skills/nl_to_silvaco_simulation/SKILL.md']:
        assert (ROOT / rel).is_file(), rel


def test_no_runtime_outputs():
    forbidden = {'.str', '.log', '.out', '.csv', '.png', '.plt', '.dat', '.set', '.history'}
    assert not [p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in forbidden]

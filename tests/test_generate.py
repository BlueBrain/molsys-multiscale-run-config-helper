import filecmp
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
EXPECTED_DIR = DATA_DIR / "expected"
OUTPUT_DIR = DATA_DIR / "generated"


from  multiscale_run_config_helper import generate as tested

def test_generate():
    tested.generate(str(DATA_DIR / 'ngv_config.json'), str(OUTPUT_DIR), 'All', False)

    assert filecmp.cmp(EXPECTED_DIR / 'mrci_inh_gids.txt', OUTPUT_DIR/ 'mrci_inh_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_L1_gids.txt', OUTPUT_DIR / 'mrci_L1_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_L2_gids.txt', OUTPUT_DIR / 'mrci_L2_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_L3_gids.txt', OUTPUT_DIR / 'mrci_L3_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_L4_gids.txt', OUTPUT_DIR / 'mrci_L4_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_L5_gids.txt', OUTPUT_DIR / 'mrci_L5_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_L6_gids.txt', OUTPUT_DIR/ 'mrci_L6_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_exc_gids.txt', OUTPUT_DIR / 'mrci_exc_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'mrci_gids.txt', OUTPUT_DIR / 'mrci_gids.txt')
    assert filecmp.cmp(EXPECTED_DIR / 'node_sets.json', OUTPUT_DIR/ 'node_sets.json')

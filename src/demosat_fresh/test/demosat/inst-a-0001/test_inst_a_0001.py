import pytest
from tts_fresh.utils.step_utils import get_steps
from demosat_fresh.test.test_utils import run_simple_test, assert_all_steps_have_state

def test_inst_a_0001():
    report, seq_json = run_simple_test(__file__)

    fr_report = report['fr_checks']['CAT_A']['INST-A-0001']

    # Last command is not covered by this FR, to test the case when the FR isn't triggered
    all_but_last_step = list(range(1, len(get_steps(seq_json))))
    assert_all_steps_have_state('VIOLATED', fr_report, all_but_last_step)


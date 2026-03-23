import json
import shutil
import pytest

from pathlib import Path
from tts_fresh.check_frs import check_flight_rules
from demosat_fresh.test.test_utils import run_test, assert_all_steps_have_state, CliArgs
import defusedxml.ElementTree as ET

TEST_DIR = Path(__file__).absolute().parent
OUT_DIR = TEST_DIR.joinpath('out')


def test_cmd_a_0001_hw_commands():
    if OUT_DIR.is_dir():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(exist_ok=True)

    with TEST_DIR.joinpath('hardware_commands.txt').open() as f:
        hardware_commands = [ln.strip() for ln in f]

    for cmd in hardware_commands:
        _test_single_command(cmd)

def _test_single_command(cmd):
    seq_json_file = _write_hw_sequence(cmd)
    report_file = OUT_DIR.joinpath(cmd + '_fresh_report.json')
    args = CliArgs.custom_for_test(__file__, seq_json_file, report_file, OUT_DIR)
    report, seq_json = run_test(args)

    fr_report = report['fr_checks']['CAT_A']['CMD-A-0001']

    assert_all_steps_have_state('VIOLATED', fr_report, seq_json)


def _write_hw_sequence(cmd: str) -> Path:
    seq_json_file = OUT_DIR.joinpath(cmd + '.seq.json')
    seq_json = {
        "id": cmd,
        "metadata": {},
        "hardware_commands": [
            {
                "stem": cmd
            }
        ]
    }

    with seq_json_file.open('w') as f:
        json.dump(seq_json, f, indent=4)

    return seq_json_file


def test_cmd_a_0001_fsw_sequence():
    seq_json_file = _write_fsw_sequence()
    report_file = OUT_DIR.joinpath('fsw_fresh_report.json')
    args = CliArgs.custom_for_test(__file__, seq_json_file, report_file, OUT_DIR)
    report, seq_json = run_test(args)

    fr_report = report['fr_checks']['CAT_A']['CMD-A-0001']

    fr_report['state'] == 'PASSED'


def _write_fsw_sequence():
    seq_json_file = OUT_DIR.joinpath('cmd_no_op.seq.json')
    seq_json = {
        "id": "test",
        "metadata": {},
        "steps": [
            {
                "args": [],
                "stem": "CMD_NO_OP",
                "time": {
                    "tag": "00:00:01",
                    "type": "COMMAND_RELATIVE"
                },
                "type": "command"
            }
        ]
    }

    with seq_json_file.open('w') as f:
        json.dump(seq_json, f, indent=4)

    return seq_json_file


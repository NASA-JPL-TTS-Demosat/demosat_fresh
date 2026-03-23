from tts_fresh.mission_config import MissionConfigBase
import demosat_fresh.flightrules.demosat
from tts_fresh.fresh_io.seqjson_io import seqjson_to_seqdict
import pathlib

class DemosatMissionConfig(MissionConfigBase):
    """
    A concrete implementation of MissionConfigBase specifically tailored for the DemoSat mission. 
    It provides the necessary mission-specific logic, such as locating the flight rules package, 
    defining the I/O methods for sequence files, and managing configuration paths.
    """

    @property
    def mission_name(self) -> str:
        """
        Returns the formal name of the mission for identification and logging purposes.
        This string is used by the core FRESH engine to distinguish DemoSat validation runs from other missions.

        :return: The string 'DemoSat'.
        :rtype: str
        """
        return 'DemoSat'

    def get_flight_rules_package(self):
        """
        Retrieves the Python package that contains the set of flight rules specific to the DemoSat mission.
        The validation engine dynamically imports this module to discover and execute the mission's custom compliance checks.

        :return: The module reference for the demosat flight rules package.
        :rtype: module
        """
        return demosat_fresh.flightrules.demosat

    def get_io_method(self):
        """
        Returns the I/O function responsible for converting DemoSat-specific sequence JSON files into the internal SeqDict format.
        This ensures that the validation engine can correctly interpret the command structure used by this mission.

        :return: The seqjson_to_seqdict function.
        :rtype: callable
        """
        return seqjson_to_seqdict

    def get_default_config_file_path(self):
        """
        Provides the absolute filesystem path to the default JSON configuration file for DemoSat.
        This file typically contains the operational thresholds and constants required for the mission's flight rules.

        :return: A path object pointing to the demosat_default_config.json file.
        :rtype: pathlib.Path
        """
        return pathlib.Path(__file__).parent.joinpath('config/demosat_default_config.json')

    def get_fr_criticality_from_id(self, fr_id: str) -> str:
        """
        Parses the criticality level from a DemoSat flight rule ID string based on the mission's naming convention.
        It expects the ID to be structured with hyphens and extracts the middle segment representing the rule's severity.

        :param fr_id: The unique identifier string for the flight rule.
        :type fr_id: str
        :return: The extracted criticality string.
        :rtype: str
        :raises ValueError: If the flight rule ID does not follow the expected hyphenated format.
        """
        try:
            _, crit, _ = fr_id.split('-')
            return crit
        except ValueError:
            raise ValueError(f'Invalid EURC FR ID: {fr_id}')

    def get_seq_file_extension(self) -> str:
        """
        Specifies the file extension pattern that identifies valid DemoSat sequence files.
        This is used by the command-line interface to filter and locate input files within a directory.

        :return: The glob pattern '*.seq.json'.
        :rtype: str
        """
        return '*.seq.json'

    def get_testing_cmd_dict_path(self) -> str:
        """
        Returns the path to the command dictionary used specifically for DemoSat sequence validation.
        This XML file defines the valid command stems and arguments permitted for the mission's command sequences.

        :return: The string path to the DEMOSAT_TESTING command.xml file.
        :rtype: str
        """
        return str(pathlib.Path(__file__).parent.joinpath('test/dictionaries/DEMOSAT_TESTING/command.xml'))

    def get_control_flow_directives(self):
        """
        Returns the set of command stems that indicate nonlinear control flow.
        These are used by the timing checker to determine where static timing analysis
        may become ambiguous.
        """
        return {
            'SEQ_IF',
            'SEQ_IF_AND',
            'SEQ_IF_OR',
            'SEQ_ELSE',
            'SEQ_END_IF',
            'SEQ_WAIT_UNTIL',
            'SEQ_WAIT_UNTIL_AND',
            'SEQ_WAIT_UNTIL_OR',
            'SEQ_WAIT_UNTIL_TIMEOUT',
            'SEQ_END_WAIT_UNTIL',
            'SEQ_WHILE_LOOP',
            'SEQ_WHILE_LOOP_AND',
            'SEQ_WHILE_LOOP_BREAK',
            'SEQ_WHILE_LOOP_CONTINUE',
            'SEQ_WHILE_LOOP_OR',
            'SEQ_END_WHILE_LOOP',
        }
"""
File: test_utils.py
Author: Guy Matz
Email: gmatz@matz.org
Github: https://www.github.com/guymatz/
Description: Tests for utils.py
"""

import json
import os

from . import Test
from isin import _get_lagged_diffs, _assign_burst_number_to_spike, _assign_burst_info


# pylint: disable=too-many-instance-attributes
class TestISIn(Test):
    """Tests for isin.py

    Spike Train compareed against output from
    using https://github.com/igm-team/meaRtools/blob/master/meaRtools/R/burst_stats.R
    as ref
    """

    def setUp(self) -> None:
        self.test_data_dir = "tests/data"
        # test_data_file = os.path.join(test_data_dir, "cult.json")
        self.test_spikes = os.path.join(
            self.test_data_dir, "isin_short_spike_train.json"
        )
        self.lagged_diffs = os.path.join(self.test_data_dir, "isin_lagged_diffs.json")
        self.filtered_diffs = os.path.join(
            self.test_data_dir, "isin_filtered_diffs.json"
        )
        self.assigned_bursts = os.path.join(
            self.test_data_dir, "isin_assigned_bursts.json"
        )
        self.assign_burst_info = os.path.join(
            self.test_data_dir, "isin_assigned_burst_info.json"
        )

        # Original data tested with these parameters
        self.N: int = 3  # pylint: disable=invalid-name
        self.ISI_N: int = 6  # pylint: disable=invalid-name

        self.spike_train: list[float] = []
        with open(self.test_spikes, encoding="utf-8") as f:
            self.spike_train = json.load(f)

    def tearDown(self) -> None:
        pass

    def test_get_lagged_diffs(self) -> None:
        """Testing portion of matlab code with the comment:
        % Look both directions from each spike
        """

        # test data was created with N=3
        test_diffs = _get_lagged_diffs(self.spike_train, 3)
        with open(self.lagged_diffs, encoding="utf-8") as f:
            good_diffs = json.load(f)
        for n in range(1, len(good_diffs)):
            self.assertListAlmostEqual(test_diffs[n], good_diffs[n], 3)

    def test_assign_burst_number_to_spike(self) -> None:
        """Testing portion of matlab code with the comment:
        % Assign burst numbers to each spike
        """

        # test data was created with N=3 & ISI_N = 6
        test_diffs: list[list[float]] = _get_lagged_diffs(self.spike_train, self.N)

        assigned_bursts: list[int] = _assign_burst_number_to_spike(
            self.spike_train, test_diffs, self.N, self.ISI_N
        )
        with open(self.assigned_bursts, encoding="utf-8") as f:
            test_assigned_bursts: list[int] = json.load(f)
        self.assertListEqual(assigned_bursts, test_assigned_bursts)

    def test_assign_burst_info(self) -> None:
        """Testing portion of matlab code with the comment:
        % Assign burst information
        """

        # test data was created with N=3 & ISI_N = 6
        test_diffs: list[list[float]] = _get_lagged_diffs(self.spike_train, self.N)

        assign_burst_nums: list[int] = _assign_burst_number_to_spike(
            self.spike_train, test_diffs, self.N, self.ISI_N
        )
        assign_burst_info: dict[str, list[float]] = _assign_burst_info(
            self.spike_train, assign_burst_nums
        )
        with open(self.assign_burst_info, encoding="utf-8") as f:
            test_assign_burst_info: dict[str, list[int]] = json.load(f)
        self.assertListAlmostEqual(
            assign_burst_info["start"], test_assign_burst_info["start"], 3
        )
        self.assertListAlmostEqual(
            assign_burst_info["end"], test_assign_burst_info["end"], 3
        )
        self.assertListEqual(assign_burst_info["S"], test_assign_burst_info["S"])
        self.assertListEqual(
            assign_burst_info["C"], test_assign_burst_info["C"]
        )  # TODO

    # Source - https://stackoverflow.com/a/8312110
    # pylint: disable=invalid-name
    def assertListAlmostEqual(self, list1, list2, places):
        """Check List of floats are equal within some tolerance"""

        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, places)


if __name__ == "__main__":
    unittest.main()

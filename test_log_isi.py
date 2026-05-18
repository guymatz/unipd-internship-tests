"""
File: test_max_interval.py
Author: Guy Matz
Email: gmatz@matz.org
Github: https://www.github.com/guymatz/
Description: tests for max_interval.py
"""

import json
import os

from . import Test
from log_isi import _get_peaks


# pylint: disable=too-many-instance-attributes
class TestLogISI(Test):
    """Tests for log_isi.py

    Spike Train compareed against output from
    using https://github.com/igm-team/meaRtools/blob/master/meaRtools/R/log.pasq_method.R
    as reference
    """

    def setUp(self) -> None:
        test_data_dir = "tests/data"
        # This datafile is in Experiments_neuronal_cultures/Data_AD/Alz_ab_m/Culture1REC1
        test_data_file = os.path.join(test_data_dir, "alz_ab_m_culture_c1r1.json")
        # mi == max_interval!
        self.test_get_peaks_baseline = os.path.join(
            test_data_dir, "logisi_get_peaks.json"
        )

        self.sampling_rate: int = 1000
        self.max_begin_isi: float = 0.17
        self.max_end_isi: float = 0.3
        self.min_burst_duration: float = 0.01
        self.min_ibi: float = 0.4
        self.min_spikes_in_burst: int = 3

        self.spike_train: list[float] = []
        with open(test_data_file, encoding="utf-8") as f:
            self.spike_train = json.load(f)

    def tearDown(self) -> None:
        pass

    def test_get_peaks(self) -> None:
        """Test _get_peaks method against output from reference"""
        with open(self.test_get_peaks, encoding="utf-8") as f:
            get_peaks_baseline = json.load(f)

        peaks: list[list[float, int]] = _get_peaks(
            self.spike_train, self.max_begin_isi, self.max_end_isi, self.sampling_rate
        )
        self.assertListEqual(burst_detection_baseline, bursts)

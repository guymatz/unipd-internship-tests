"""
File: test_max_interval.py
Author: Guy Matz
Email: gmatz@matz.org
Github: https://www.github.com/guymatz/
Description: tests for max_interval.py
"""

import json
import os
import numpy as np

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
        self.test_data_file = os.path.join(test_data_dir, "alz_ab_m_culture_c1r1.json")
        self.test_get_peaks_baseline = os.path.join(
            test_data_dir, "logisi_get_peaks.json"
        )

        # tolerance when comparing floats
        self.tolerance = 3

        self.sampling_rate: int = 1000
        self.max_begin_isi: float = 0.17
        self.max_end_isi: float = 0.3
        self.min_burst_duration: float = 0.01
        self.min_ibi: float = 0.4
        self.min_spikes_in_burst: int = 3

        self.spike_train: list[float] = []
        with open(self.test_data_file, encoding="utf-8") as f:
            self.spike_train = json.load(f)
        self.spike_train = [x / 1000 for x in self.spike_train]

    def tearDown(self) -> None:
        pass

    def test_get_peaks(self) -> None:
        """Test _get_peaks method against output from reference"""
        with open(self.test_get_peaks_baseline, encoding="utf-8") as f:
            peaks_baseline = json.load(f)
        # stop hard-coding
        histogram = np.histogram(self.spike_train, density=True, bins=range(0, 36001, 2000))
        peaks_n_locs: list[dict[str, int], dict[str, float]] = _get_peaks(histogram)
        breakpoint()
        for idx, peak in enumerate(peaks_n_locs):
            self.assertAlmostEqual(peak["pks"], peaks_baseline[idx]["pks"], self.tolerance)
            self.assertEqual(peak["locs"], peaks_baseline[idx]["locs"])

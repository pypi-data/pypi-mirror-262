"""Cryonirsp scan step parser."""
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.models.tags import CryonirspStemName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess


def zero_size_scan_step_test(fits_obj) -> bool:
    """Test if the dual internal scan loop trick is being used."""
    if fits_obj.num_cn2_scan_steps > 0 and fits_obj.cn2_step_size == 0:
        return fits_obj.cn2_step_size == 0
    return False


def single_scan_step_key(fits_obj: CryonirspL0FitsAccess):
    """Return the single_step_key based on how the scanning is being done."""
    if zero_size_scan_step_test(fits_obj):
        return "cn1_scan_step"
    return "scan_step"


def total_num_key(fits_obj: CryonirspL0FitsAccess):
    """Return the total_num_key based on how the scanning is being done."""
    if zero_size_scan_step_test(fits_obj):
        return "num_cn1_scan_steps"
    return "num_scan_steps"


class NumberOfScanStepsBud(Stem):
    """Bud for finding the total number of scan steps."""

    def __init__(self):
        super().__init__(stem_name=CryonirspBudName.num_scan_steps.value)

    def setter(self, fits_obj: CryonirspL0FitsAccess) -> Type[SpilledDirt] | tuple[int, int]:
        """
        Setter for the bud.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt

        num_scan = getattr(fits_obj, total_num_key(fits_obj))
        single_step = getattr(fits_obj, single_scan_step_key(fits_obj))

        return num_scan, single_step

    def getter(self, key) -> str | float | int:
        """
        Getter and check for bud.

        Return value if only a single value was found in dataset. Error if multiple values were found or if the actual
        scan steps found do not form a complete set based on the number-of-scan-steps header key.
        """
        values = self.key_to_petal_dict.values()
        num_steps_set = set([v[0] for v in values])

        # This is copied from UniqueBud because we still want to check this
        if len(num_steps_set) > 1:
            raise ValueError(
                f"Multiple {self.stem_name} values found for key {key}. Values: {num_steps_set}"
            )

        # Now check that all the steps we expect are present
        all_steps = sorted(list(set([v[1] for v in values])))
        # scan step is 1-based
        if all_steps != list(range(1, max(all_steps) + 1)):
            raise ValueError(f"Not all sequential steps could be found. Found {all_steps}")

        return len(all_steps)


class ScanStepNumberFlower(SingleValueSingleKeyFlower):
    """Flower for a scan step."""

    def __init__(self):
        super().__init__(tag_stem_name=CryonirspStemName.scan_step.value, metadata_key="")

    def setter(self, fits_obj: CryonirspL0FitsAccess):
        """
        Setter for a flower.

        Parameters
        ----------
        fits_obj:
            A single FitsAccess object
        """
        if fits_obj.ip_task_type != "observe":
            return SpilledDirt
        # Set the meta-data key, which isn't known at object creation time.
        self.metadata_key = single_scan_step_key(fits_obj)
        return super().setter(fits_obj)

"""
Test LMU Memory Map Control
"""

import logging
import sys

sys.path.append(__file__.split("pyLMUSharedMemory")[0])
from pyLMUSharedMemory import lmu_data, lmu_mmap


def test_api():
    # Add logger
    logger = logging.getLogger(__name__)
    test_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.addHandler(test_handler)
    logger.info(__doc__)

    # Test run
    SEPARATOR = "=" * 50
    print("Test API - Direct Access")
    info = lmu_mmap.MMapControl(lmu_data.LMUConstants.LMU_SHARED_MEMORY_FILE, lmu_data.LMUObjectOut)
    info.create(1)
    info.update()

    print(SEPARATOR)
    print("Test API - Close")
    info.close()

    print(SEPARATOR)
    print("Test API - Copy Access")
    info.create(0)
    info.update()

    print(SEPARATOR)
    print("Test API - Read")
    version = info.data.generic.gameVersion
    track = info.data.scoring.scoringInfo.mTrackName.decode()
    vehicle = info.data.telemetry.telemInfo[0].mVehicleName.decode()
    total = info.data.scoring.scoringInfo.mNumVehicles
    print(f"version: {version if version else 'not running'}")
    print(f"track name: {track if version else 'not running'}")
    print(f"vehicle name: {vehicle if version else 'not running'}")
    print(f"total cars: {total if version else 'not running'}")

    print(SEPARATOR)
    info.close()


if __name__ == "__main__":
    test_api()

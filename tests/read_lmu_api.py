"""
Test & read data from LMU's built-in Shared Memory Interface
"""

from __future__ import annotations

import ctypes
import sys

sys.path.append(".")
from pyLMUSharedMemory import lmu_data, lmu_enum


def verify_struct_size(s_class: ctypes.Structure, size_origin: int):
    size = ctypes.sizeof(s_class)
    print(f"{s_class.__name__:<24} Size: {size:<10} ORG: {size_origin:<10} Match: {size_origin == size}")
    if size_origin != size:
        raise ValueError("Structure size mismatch.")


def compare_struct_size():
    print("Verify Struct Size:")
    verify_struct_size(lmu_data.LMUVect3, 24)
    verify_struct_size(lmu_data.LMUWheel, 260)
    verify_struct_size(lmu_data.LMUVehicleTelemetry, 1888)
    verify_struct_size(lmu_data.LMUVehicleScoring, 584)
    verify_struct_size(lmu_data.LMUScoringInfo, 548)
    verify_struct_size(lmu_data.LMUApplicationState, 260)
    verify_struct_size(lmu_data.LMUScoringData, 126832)
    verify_struct_size(lmu_data.LMUTelemetryData, 196356)
    verify_struct_size(lmu_data.LMUPathData, 1300)
    verify_struct_size(lmu_data.LMUEvent, 64)
    verify_struct_size(lmu_data.LMUGeneric, 332)
    verify_struct_size(lmu_data.LMUObjectOut, 324820)
    verify_struct_size(lmu_data.LMULayout, 324820)


def event_info(data: lmu_data.LMUEvent):
    print("Event Info:")
    print("SME_ENTER:", data.SME_ENTER)
    print("SME_EXIT:", data.SME_EXIT)
    print("SME_SET_ENVIRONMENT:", data.SME_SET_ENVIRONMENT)
    print("SME_UPDATE_SCORING:", data.SME_UPDATE_SCORING)
    print("SME_UPDATE_TELEMETRY:", data.SME_UPDATE_TELEMETRY)


def generic_info(data: lmu_data.LMUGeneric):
    print("Game info:")
    print("Version:", data.gameVersion)
    print("FFB torque:", data.FFBTorque)
    print("HWND:", data.appInfo.mAppWindow)
    print("Screen width:", data.appInfo.mWidth)
    print("Screen height:", data.appInfo.mHeight)
    print("Refresh rate:", data.appInfo.mRefreshRate)
    print("Options location:", data.appInfo.mOptionsLocation)
    print("Options page:", data.appInfo.mOptionsPage)


def path_info(data: lmu_data.LMUPathData):
    print("Path info:")
    print("User data:", data.userData)
    print("Custom variables:", data.customVariables)
    print("Steward results:", data.stewardResults)
    print("Player profile:", data.playerProfile)
    print("Plugins folder:", data.pluginsFolder)


def scoring_info(data: lmu_data.LMUScoringInfo):
    print("Scoring info:")
    print("Track name:", data.mTrackName)
    print("Local player name:", data.mPlayerName)
    print("Setting name:", data.mPlrFileName)
    print("Total vehicles:", data.mNumVehicles)

    print("mSessionTimeRemaining:", data.mSessionTimeRemaining)
    print("mTimeOfDay:", data.mTimeOfDay)
    print("mIsFixedSetup:", data.mIsFixedSetup)

    print("mTrackGripLevel:", lmu_enum.LMUTrackGripLevel(data.mTrackGripLevel))
    print("mCloudCoverage:", lmu_enum.LMUCloudCoverage(data.mCloudCoverage))

    print("mTrackLimitsStepsPerPenalty:", data.mTrackLimitsStepsPerPenalty)
    print("mTrackLimitsStepsPerPoint:", data.mTrackLimitsStepsPerPoint)


def player_scoring_info(data: lmu_data.LMUVehicleScoring):
    print("Selected Player scoring info:")
    print("Slot ID:", data.mID)
    print("Driver name:", data.mDriverName)
    print("VEH file:", data.mVehFilename)
    print("Is local player:", data.mIsPlayer)


def player_telemetry_info(data: lmu_data.LMUVehicleTelemetry):
    print("Selected player telemetry info:")
    print("Slot ID:", data.mID)
    print("Vehicle:", data.mVehicleName)
    print("Gear:", data.mGear)
    print("Throttle:", data.mUnfilteredThrottle)
    print("Brake:", data.mUnfilteredBrake)
    print("Clutch:", data.mUnfilteredClutch)

    print("mLapInvalidated:", data.mLapInvalidated)
    print("mABSActive:", data.mABSActive)
    print("mTCActive:", data.mTCActive)
    print("mSpeedLimiterActive:", data.mSpeedLimiterActive)

    print("mWiperState", lmu_enum.LMUWiperStatus(data.mWiperState))
    print("mTC:", data.mTC)
    print("mTCMax:", data.mTCMax)
    print("mTCSlip:", data.mTCSlip)
    print("mTCSlipMax:", data.mTCSlipMax)
    print("mTCCut:", data.mTCCut)
    print("mTCCutMax:", data.mTCCutMax)
    print("mABS:", data.mABS)
    print("mABSMax:", data.mABSMax)
    print("mMotorMap:", data.mMotorMap)
    print("mMotorMapMax:", data.mMotorMapMax)
    print("mMigration:", data.mMigration)
    print("mMigrationMax:", data.mMigrationMax)

    print("mFrontAntiSway:", data.mFrontAntiSway)
    print("mFrontAntiSwayMax:", data.mFrontAntiSwayMax)
    print("mRearAntiSway:", data.mRearAntiSway)
    print("mRearAntiSwayMax:", data.mRearAntiSwayMax)

    print("mLiftAndCoastProgress:", data.mLiftAndCoastProgress)
    print("mTrackLimitsSteps:", data.mTrackLimitsSteps)

    print("mRegen:", data.mRegen)
    print("mStateOfCharge:", data.mStateOfCharge)
    print("mVirtualEnergy:", data.mVirtualEnergy)

    print("mTimeGapCarAhead:", data.mTimeGapCarAhead)
    print("mTimeGapCarBehind:", data.mTimeGapCarBehind)
    print("mTimeGapPlaceAhead:", data.mTimeGapPlaceAhead)
    print("mTimeGapPlaceBehind:", data.mTimeGapPlaceBehind)

    print("mVehicleModel:", data.mVehicleModel)
    print("mVehicleClass:", lmu_enum.LMUVehicleClass(data.mVehicleClass))
    print("mVehicleChampionship:", lmu_enum.LMUVehicleChampionship(data.mVehicleChampionship))


def player_wheel_info(data: list[lmu_data.LMUWheel]):
    for index in range(4):
        print(lmu_enum.LMUWheelIndex(index).name, "Wheel Info:")
        print("mOptimalTemp:", data[index].mOptimalTemp)
        print("mCompoundIndex:", data[index].mCompoundIndex)
        print("mCompoundType:", lmu_enum.LMUCompoundType(data[index].mCompoundType))


def vehicle_model_info(data: list[lmu_data.LMUVehicleTelemetry], total_vehicles: int):
    print("Available vehicle model list from session:")
    for model in set(data[i].mVehicleModel for i in range(total_vehicles)):
        print(model)


def list_zero_data(data, source):
    print("List of zero data:", source.__name__)
    for var, _ in source._fields_:
        value = getattr(data, var)
        if not value:
            print(var, value)


def test_data(info: lmu_data.SimInfo, player_index, selected_player_index):
    """Example usage"""
    separator = "-" * 40

    print(separator)

    print("Player Index:")
    print("Local player index:", player_index)
    print("Selected player index:", selected_player_index)

    print(separator)

    event_info(info.LMUData.generic.events)

    print(separator)

    generic_info(info.LMUData.generic)

    print(separator)

    path_info(info.LMUData.paths)

    print(separator)

    scoring_info(info.LMUData.scoring.scoringInfo)

    print(separator)

    player_scoring_info(info.LMUData.scoring.vehScoringInfo[selected_player_index])

    print(separator)

    player_telemetry_info(info.LMUData.telemetry.telemInfo[selected_player_index])

    print(separator)

    player_wheel_info(info.LMUData.telemetry.telemInfo[selected_player_index].mWheels)

    print(separator)

    vehicle_model_info(info.LMUData.telemetry.telemInfo, info.LMUData.scoring.scoringInfo.mNumVehicles)


def verify_data(info: lmu_data.SimInfo, player_index):
    separator = "-" * 40

    print(separator)

    list_zero_data(info.LMUData.scoring.scoringInfo, lmu_data.LMUScoringInfo)

    print(separator)

    list_zero_data(info.LMUData.scoring.vehScoringInfo[player_index], lmu_data.LMUVehicleScoring)

    print(separator)

    list_zero_data(info.LMUData.telemetry.telemInfo[player_index], lmu_data.LMUVehicleTelemetry)

    print(separator)

    list_zero_data(info.LMUData.telemetry.telemInfo[player_index].mWheels[0], lmu_data.LMUWheel)


if __name__ == "__main__":
    compare_struct_size()

    info = lmu_data.SimInfo()

    # Uncomment to save raw memory data to file
    # info.save("LMU_SHARED_MEMORY_FILE.txt")

    player_index = info.LMUData.telemetry.playerVehicleIdx
    selected_player_index = player_index

    test_data(info, player_index, selected_player_index)

    verify_data(info, selected_player_index)

"""
Python mapping of LMU's built-in Shared Memory Interface

This library is based on:
- LMU SharedMemoryInterface header file by S397, found in game's `Support\\SharedMemoryInterface` folder.
- pyRfactor2SharedMemory by Tony Whitley: https://github.com/TonyWhitley/pyRfactor2SharedMemory

Type hints & annotation:
- Annotate "ctypes type" as "Python type" according to table from:
  https://docs.python.org/3/library/ctypes.html#fundamental-data-types
- Annotate array object as list[type].
"""

from __future__ import annotations

import ctypes
import mmap

from ._common import _t, typedstruct


# Constants
class LMUConstants:
    """LMU constants"""

    LMU_SHARED_MEMORY_FILE: str = "LMU_Data"
    LMU_PROCESS_NAME: str = "Le Mans Ultimate"

    MAX_MAPPED_VEHICLES: int = 104
    MAX_PATH_LENGTH: int = 260  # maximum length for path on windows
    INVALID_CAR_INDEX: int = -1


# InternalsPlugin
@typedstruct(pack=4)
class LMUVect3(ctypes.Structure):
    """Mapping of 'TelemVect3' from InternalsPlugin.hpp"""

    __slots__ = ()

    x: float = _t(ctypes.c_double)
    y: float = _t(ctypes.c_double)
    z: float = _t(ctypes.c_double)


@typedstruct(pack=4)
class LMUWheel(ctypes.Structure):
    """Mapping of 'TelemWheelV01' from InternalsPlugin.hpp

    Attributes:
        mSuspensionDeflection: meters
        mRideHeight: meters
        mSuspForce: pushrod load in Newtons
        mBrakeTemp: Celsius
        mBrakePressure: currently 0.0-1.0, depending on driver input and brake balance; will convert to true brake pressure (kPa) in future
        mRotation: radians/sec
        mLateralPatchVel: lateral velocity at contact patch
        mLongitudinalPatchVel: longitudinal velocity at contact patch
        mLateralGroundVel: lateral velocity at contact patch
        mLongitudinalGroundVel: longitudinal velocity at contact patch
        mCamber: radians (positive is left for left-side wheels, right for right-side wheels)
        mLateralForce: Newtons
        mLongitudinalForce: Newtons
        mTireLoad: Newtons
        mGripFract: an approximation of what fraction of the contact patch is sliding
        mPressure: kPa (tire pressure)
        mTemperature: Kelvin (subtract 273.15 to get Celsius) left/center/right (not to be confused with inside/center/outside!)
        mWear: wear (0.0-1.0, fraction of maximum) ... this is not necessarily proportional with grip loss
        mTerrainName: the material prefixes from the TDF file
        mSurfaceType: 0=dry, 1=wet, 2=grass, 3=dirt, 4=gravel, 5=rumblestrip, 6 = special
        mFlat: whether tire is flat
        mDetached: whether wheel is detached
        mStaticUndeflectedRadius: tire radius in centimeters
        mVerticalTireDeflection: how much is tire deflected from its (speed-sensitive) radius
        mWheelYLocation: wheel's y location relative to vehicle y location
        mToe: current toe angle w.r.t. the vehicle
        mTireCarcassTemperature: rough average of temperature samples from carcass (Kelvin)
        mTireInnerLayerTemperature: rough average of temperature samples from innermost layer of rubber (before carcass) (Kelvin)
        mOptimalTemp: optimal temperature (Celsius)
        mCompoundIndex: compound index count from available compound list for specific car & track
        mCompoundType: 0 = soft, 1 = medium, 2 = hard, 3 = wet
        mExpansion: for future use
    """

    __slots__ = ()

    mSuspensionDeflection: float = _t(ctypes.c_double)
    mRideHeight: float = _t(ctypes.c_double)
    mSuspForce: float = _t(ctypes.c_double)
    mBrakeTemp: float = _t(ctypes.c_double)
    mBrakePressure: float = _t(ctypes.c_double)
    mRotation: float = _t(ctypes.c_double)
    mLateralPatchVel: float = _t(ctypes.c_double)
    mLongitudinalPatchVel: float = _t(ctypes.c_double)
    mLateralGroundVel: float = _t(ctypes.c_double)
    mLongitudinalGroundVel: float = _t(ctypes.c_double)
    mCamber: float = _t(ctypes.c_double)
    mLateralForce: float = _t(ctypes.c_double)
    mLongitudinalForce: float = _t(ctypes.c_double)
    mTireLoad: float = _t(ctypes.c_double)
    mGripFract: float = _t(ctypes.c_double)
    mPressure: float = _t(ctypes.c_double)
    mTemperature: list[float] = _t(ctypes.c_double * 3)
    mWear: float = _t(ctypes.c_double)
    mTerrainName: bytes = _t(ctypes.c_char * 16)
    mSurfaceType: int = _t(ctypes.c_ubyte)
    mFlat: bool = _t(ctypes.c_bool)
    mDetached: bool = _t(ctypes.c_bool)
    mStaticUndeflectedRadius: int = _t(ctypes.c_ubyte)
    mVerticalTireDeflection: float = _t(ctypes.c_double)
    mWheelYLocation: float = _t(ctypes.c_double)
    mToe: float = _t(ctypes.c_double)
    mTireCarcassTemperature: float = _t(ctypes.c_double)
    mTireInnerLayerTemperature: list[float] = _t(ctypes.c_double * 3)
    mOptimalTemp: float = _t(ctypes.c_float)
    mCompoundIndex: int = _t(ctypes.c_ubyte)
    mCompoundType: int = _t(ctypes.c_ubyte)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 18)


@typedstruct(pack=4)
class LMUVehicleTelemetry(ctypes.Structure):
    """Mapping of 'TelemInfoV01' from InternalsPlugin.hpp

    Attributes:
        mID: slot ID (note that it can be re-used in multiplayer after someone leaves)
        mDeltaTime: time since last update (seconds)
        mElapsedTime: game session time
        mLapNumber: current lap number
        mLapStartET: time this lap was started
        mVehicleName: current vehicle name
        mTrackName: current track name
        mPos: world position in meters
        mLocalVel: velocity (meters/sec) in local vehicle coordinates
        mLocalAccel: acceleration (meters/sec^2) in local vehicle coordinates
        mOri: rows of orientation matrix (use TelemQuat conversions if desired) also converts local
        mLocalRot: rotation (radians/sec) in local vehicle coordinates
        mLocalRotAccel: rotational acceleration (radians/sec^2) in local vehicle coordinates
        mGear: -1=reverse, 0=neutral, 1+ = forward gears
        mEngineRPM: engine RPM
        mEngineWaterTemp: Celsius
        mEngineOilTemp: Celsius
        mClutchRPM: clutch RPM
        mUnfilteredThrottle: ranges  0.0-1.0
        mUnfilteredBrake: ranges  0.0-1.0
        mUnfilteredSteering: ranges -1.0-1.0 (left to right)
        mUnfilteredClutch: ranges  0.0-1.0
        mFilteredThrottle: ranges  0.0-1.0
        mFilteredBrake: ranges  0.0-1.0
        mFilteredSteering: ranges -1.0-1.0 (left to right)
        mFilteredClutch: ranges  0.0-1.0
        mSteeringShaftTorque: torque around steering shaft (used to be mSteeringArmForce, but that is not necessarily accurate for feedback purposes)
        mFront3rdDeflection: deflection at front 3rd spring
        mRear3rdDeflection: deflection at rear 3rd spring
        mFrontWingHeight: front wing height
        mFrontRideHeight: front ride height
        mRearRideHeight: rear ride height
        mDrag: drag
        mFrontDownforce: front downforce
        mRearDownforce: rear downforce
        mFuel: amount of fuel (liters)
        mEngineMaxRPM: rev limit
        mScheduledStops: number of scheduled pitstops
        mOverheating: whether overheating icon is shown
        mDetached: whether any parts (besides wheels) have been detached
        mHeadlights: whether headlights are on
        mDentSeverity: dent severity at 8 locations around the car (0=none, 1=some, 2=more)
        mLastImpactET: time of last impact
        mLastImpactMagnitude: magnitude of last impact
        mLastImpactPos: location of last impact
        mEngineTorque: current engine torque (including additive torque) (used to be mEngineTq, but there's little reason to abbreviate it)
        mCurrentSector: the current sector (zero-based) with the pitlane stored in the sign bit (example: entering pits from third sector gives 0x80000002)
        mSpeedLimiter: whether speed limiter is on
        mMaxGears: maximum forward gears
        mFrontTireCompoundIndex: index within brand
        mRearTireCompoundIndex: index within brand
        mFuelCapacity: capacity in liters
        mFrontFlapActivated: whether front flap is activated
        mRearFlapActivated: whether rear flap is activated
        mRearFlapLegalStatus: 0=disallowed, 1=criteria detected but not allowed quite yet, 2 = allowed
        mIgnitionStarter: 0=off 1=ignition 2 = ignition+starter
        mFrontTireCompoundName: name of front tire compound
        mRearTireCompoundName: name of rear tire compound
        mSpeedLimiterAvailable: whether speed limiter is available
        mAntiStallActivated: whether (hard) anti-stall is activated
        mUnused: unused
        mVisualSteeringWheelRange: the *visual* steering wheel range
        mRearBrakeBias: fraction of brakes on rear
        mTurboBoostPressure: current turbo boost pressure if available
        mPhysicsToGraphicsOffset: offset from static CG to graphical center
        mPhysicalSteeringWheelRange: the *physical* steering wheel range
        mDeltaBest: deltabest
        mBatteryChargeFraction: Battery charge as fraction [0.0-1.0]
        mElectricBoostMotorTorque: current torque of boost motor (can be negative when in regenerating mode)
        mElectricBoostMotorRPM: current rpm of boost motor
        mElectricBoostMotorTemperature: current temperature of boost motor
        mElectricBoostWaterTemperature: current water temperature of boost motor cooler if present (0 otherwise)
        mElectricBoostMotorState: 0=unavailable 1=inactive, 2=propulsion, 3=regeneration
        mLapInvalidated: is lap invalidated
        mABSActive: ABS activation state
        mTCActive: TC activation state
        mSpeedLimiterActive: speed limiter activation state
        mWiperState: 0=off, 1=auto, 2=slow, 3=fast
        mTC: TC level
        mTCMax: max TC steps
        mTCSlip: TC slip level
        mTCSlipMax: max TC slip steps
        mTCCut: TC cut level
        mTCCutMax: max TC cut steps
        mABS: ABS level
        mABSMax: max ABS steps
        mMotorMap: motor map level
        mMotorMapMax: max motor map steps
        mMigration: brake migration level
        mMigrationMax: max brake migration steps
        mFrontAntiSway: front anti sway bar level
        mFrontAntiSwayMax: max front anti sway bar steps
        mRearAntiSway: rear anti sway bar level
        mRearAntiSwayMax: max rear anti sway bar steps
        mLiftAndCoastProgress: lift and coast progress step (from 0 to 255)
        mTrackLimitsSteps: Normalized track limits points (TrackLimitPoints * TrackLimitStepsPerPoint)
        mRegen: motor regen (kW)
        mStateOfCharge: battery state of charge (percent)
        mVirtualEnergy: fraction
        mTimeGapCarAhead: time gap car ahead
        mTimeGapCarBehind: time gap car behind
        mTimeGapPlaceAhead: time gap place ahead
        mTimeGapPlaceBehind: time gap place behind
        mVehicleModel: brand & model name
        mVehicleClass: full class name, may not be same as mVehicleClass
        mVehicleChampionship: championship & year
        mExpansion: for future use (note that the slot ID has been moved to mID above)
        mWheels: wheel info (0=front left, 1=front right, 2=rear left, 3=rear right)
    """

    __slots__ = ()

    mID: int = _t(ctypes.c_int)
    mDeltaTime: float = _t(ctypes.c_double)
    mElapsedTime: float = _t(ctypes.c_double)
    mLapNumber: int = _t(ctypes.c_int)
    mLapStartET: float = _t(ctypes.c_double)
    mVehicleName: bytes = _t(ctypes.c_char * 64)
    mTrackName: bytes = _t(ctypes.c_char * 64)
    mPos: LMUVect3 = _t(LMUVect3)
    mLocalVel: LMUVect3 = _t(LMUVect3)
    mLocalAccel: LMUVect3 = _t(LMUVect3)
    mOri: list[LMUVect3] = _t(LMUVect3 * 3)
    mLocalRot: LMUVect3 = _t(LMUVect3)
    mLocalRotAccel: LMUVect3 = _t(LMUVect3)
    mGear: int = _t(ctypes.c_int)
    mEngineRPM: float = _t(ctypes.c_double)
    mEngineWaterTemp: float = _t(ctypes.c_double)
    mEngineOilTemp: float = _t(ctypes.c_double)
    mClutchRPM: float = _t(ctypes.c_double)
    mUnfilteredThrottle: float = _t(ctypes.c_double)
    mUnfilteredBrake: float = _t(ctypes.c_double)
    mUnfilteredSteering: float = _t(ctypes.c_double)
    mUnfilteredClutch: float = _t(ctypes.c_double)
    mFilteredThrottle: float = _t(ctypes.c_double)
    mFilteredBrake: float = _t(ctypes.c_double)
    mFilteredSteering: float = _t(ctypes.c_double)
    mFilteredClutch: float = _t(ctypes.c_double)
    mSteeringShaftTorque: float = _t(ctypes.c_double)
    mFront3rdDeflection: float = _t(ctypes.c_double)
    mRear3rdDeflection: float = _t(ctypes.c_double)
    mFrontWingHeight: float = _t(ctypes.c_double)
    mFrontRideHeight: float = _t(ctypes.c_double)
    mRearRideHeight: float = _t(ctypes.c_double)
    mDrag: float = _t(ctypes.c_double)
    mFrontDownforce: float = _t(ctypes.c_double)
    mRearDownforce: float = _t(ctypes.c_double)
    mFuel: float = _t(ctypes.c_double)
    mEngineMaxRPM: float = _t(ctypes.c_double)
    mScheduledStops: int = _t(ctypes.c_ubyte)
    mOverheating: bool = _t(ctypes.c_bool)
    mDetached: bool = _t(ctypes.c_bool)
    mHeadlights: bool = _t(ctypes.c_bool)
    mDentSeverity: list[int] = _t(ctypes.c_ubyte * 8)
    mLastImpactET: float = _t(ctypes.c_double)
    mLastImpactMagnitude: float = _t(ctypes.c_double)
    mLastImpactPos: LMUVect3 = _t(LMUVect3)
    mEngineTorque: float = _t(ctypes.c_double)
    mCurrentSector: int = _t(ctypes.c_int)
    mSpeedLimiter: int = _t(ctypes.c_ubyte)
    mMaxGears: int = _t(ctypes.c_ubyte)
    mFrontTireCompoundIndex: int = _t(ctypes.c_ubyte)
    mRearTireCompoundIndex: int = _t(ctypes.c_ubyte)
    mFuelCapacity: float = _t(ctypes.c_double)
    mFrontFlapActivated: int = _t(ctypes.c_ubyte)
    mRearFlapActivated: int = _t(ctypes.c_ubyte)
    mRearFlapLegalStatus: int = _t(ctypes.c_ubyte)
    mIgnitionStarter: int = _t(ctypes.c_ubyte)
    mFrontTireCompoundName: bytes = _t(ctypes.c_char * 18)
    mRearTireCompoundName: bytes = _t(ctypes.c_char * 18)
    mSpeedLimiterAvailable: int = _t(ctypes.c_ubyte)
    mAntiStallActivated: int = _t(ctypes.c_ubyte)
    mUnused: list[int] = _t(ctypes.c_ubyte * 2)
    mVisualSteeringWheelRange: float = _t(ctypes.c_float)
    mRearBrakeBias: float = _t(ctypes.c_double)
    mTurboBoostPressure: float = _t(ctypes.c_double)
    mPhysicsToGraphicsOffset: list[float] = _t(ctypes.c_float * 3)
    mPhysicalSteeringWheelRange: float = _t(ctypes.c_float)
    mDeltaBest: float = _t(ctypes.c_double)
    mBatteryChargeFraction: float = _t(ctypes.c_double)
    mElectricBoostMotorTorque: float = _t(ctypes.c_double)
    mElectricBoostMotorRPM: float = _t(ctypes.c_double)
    mElectricBoostMotorTemperature: float = _t(ctypes.c_double)
    mElectricBoostWaterTemperature: float = _t(ctypes.c_double)
    mElectricBoostMotorState: int = _t(ctypes.c_ubyte)
    mLapInvalidated: bool = _t(ctypes.c_bool)
    mABSActive: bool = _t(ctypes.c_bool)
    mTCActive: bool = _t(ctypes.c_bool)
    mSpeedLimiterActive: bool = _t(ctypes.c_bool)
    mWiperState: int = _t(ctypes.c_uint8)
    mTC: int = _t(ctypes.c_uint8)
    mTCMax: int = _t(ctypes.c_uint8)
    mTCSlip: int = _t(ctypes.c_uint8)
    mTCSlipMax: int = _t(ctypes.c_uint8)
    mTCCut: int = _t(ctypes.c_uint8)
    mTCCutMax: int = _t(ctypes.c_uint8)
    mABS: int = _t(ctypes.c_uint8)
    mABSMax: int = _t(ctypes.c_uint8)
    mMotorMap: int = _t(ctypes.c_uint8)
    mMotorMapMax: int = _t(ctypes.c_uint8)
    mMigration: int = _t(ctypes.c_uint8)
    mMigrationMax: int = _t(ctypes.c_uint8)
    mFrontAntiSway: int = _t(ctypes.c_uint8)
    mFrontAntiSwayMax: int = _t(ctypes.c_uint8)
    mRearAntiSway: int = _t(ctypes.c_uint8)
    mRearAntiSwayMax: int = _t(ctypes.c_uint8)
    mLiftAndCoastProgress: int = _t(ctypes.c_uint8)
    mTrackLimitsSteps: int = _t(ctypes.c_uint8)
    mRegen: float = _t(ctypes.c_float)
    mStateOfCharge: float = _t(ctypes.c_float)
    mVirtualEnergy: float = _t(ctypes.c_float)
    mTimeGapCarAhead: float = _t(ctypes.c_float)
    mTimeGapCarBehind: float = _t(ctypes.c_float)
    mTimeGapPlaceAhead: float = _t(ctypes.c_float)
    mTimeGapPlaceBehind: float = _t(ctypes.c_float)
    mVehicleModel: bytes = _t(ctypes.c_char * 30)
    mVehicleClass: int = _t(ctypes.c_uint8)
    mVehicleChampionship: int = _t(ctypes.c_uint8)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 20)
    mWheels: list[LMUWheel] = _t(LMUWheel * 4)


@typedstruct(pack=4)
class LMUVehicleScoring(ctypes.Structure):
    """Mapping of 'VehicleScoringInfoV01' from InternalsPlugin.hpp

    Attributes:
        mID: slot ID (note that it can be re-used in multiplayer after someone leaves)
        mDriverName: driver name
        mVehicleName: vehicle name
        mTotalLaps: laps completed
        mSector: 0=sector3, 1=sector1, 2 = sector2 (don't ask why)
        mFinishStatus: 0=none, 1=finished, 2=dnf, 3 = dq
        mLapDist: current distance around track
        mPathLateral: lateral position with respect to *very approximate* "center" path
        mTrackEdge: track edge (w.r.t. "center" path) on same side of track as vehicle
        mBestSector1: best sector 1
        mBestSector2: best sector 2 (plus sector 1)
        mBestLapTime: best lap time
        mLastSector1: last sector 1
        mLastSector2: last sector 2 (plus sector 1)
        mLastLapTime: last lap time
        mCurSector1: current sector 1 if valid
        mCurSector2: current sector 2 (plus sector 1) if valid
        mNumPitstops: number of pitstops made
        mNumPenalties: number of outstanding penalties
        mIsPlayer: is this the player's vehicle
        mControl: who's in control: -1=nobody (shouldn't get this) 0=local player, 1=local AI, 2=remote, 3 = replay (shouldn't get this)
        mInPits: between pit entrance and pit exit (not always accurate for remote vehicles)
        mPlace: 1-based position
        mVehicleClass: vehicle class
        mTimeBehindNext: time behind vehicle in next higher place
        mLapsBehindNext: laps behind vehicle in next higher place
        mTimeBehindLeader: time behind leader
        mLapsBehindLeader: laps behind leader
        mLapStartET: time this lap was started
        mPos: world position in meters
        mLocalVel: velocity (meters/sec) in local vehicle coordinates
        mLocalAccel: acceleration (meters/sec^2) in local vehicle coordinates
        mOri: rows of orientation matrix (use TelemQuat conversions if desired) also converts local
        mLocalRot: rotation (radians/sec) in local vehicle coordinates
        mLocalRotAccel: rotational acceleration (radians/sec^2) in local vehicle coordinates
        mHeadlights: status of headlights
        mPitState: 0=none, 1=request, 2=entering, 3=stopped, 4=exiting
        mServerScored: whether this vehicle is being scored by server (could be off in qualifying or racing heats)
        mIndividualPhase: game phases (described below) plus 9=after formation, 10=under yellow, 11 = under blue (not used)
        mQualification: 1-based, can be -1 when invalid
        mTimeIntoLap: estimated time into lap
        mEstimatedLapTime: estimated laptime used for "time behind" and "time into lap" (note: this may changed based on vehicle and setup!?)
        mPitGroup: pit group (same as team name unless pit is shared)
        mFlag: primary flag being shown to vehicle (currently only 0=green or 6 = blue)
        mUnderYellow: whether this car has taken a full-course caution flag at the start/finish line
        mCountLapFlag: 0 = do not count lap or time, 1 = count lap but not time, 2 = count lap and time
        mInGarageStall: appears to be within the correct garage stall
        mUpgradePack: Coded upgrades
        mPitLapDist: location of pit in terms of lap distance
        mBestLapSector1: sector 1 time from best lap (not necessarily the best sector 1 time)
        mBestLapSector2: sector 2 time from best lap (not necessarily the best sector 2 time)
        mSteamID: SteamID of the current driver (if any)
        mVehFilename: filename of veh file used to identify this vehicle.
        mAttackMode: FE attack mode state
        mFuelFraction: Percentage of fuel or battery left in vehicle. 0x00 = 0%; 0xFF = 100%
        mDRSState: DRS (RearFlap) state
        mExpansion: for future use
    """

    __slots__ = ()

    mID: int = _t(ctypes.c_int)
    mDriverName: bytes = _t(ctypes.c_char * 32)
    mVehicleName: bytes = _t(ctypes.c_char * 64)
    mTotalLaps: int = _t(ctypes.c_short)
    mSector: int = _t(ctypes.c_byte)
    mFinishStatus: int = _t(ctypes.c_byte)
    mLapDist: float = _t(ctypes.c_double)
    mPathLateral: float = _t(ctypes.c_double)
    mTrackEdge: float = _t(ctypes.c_double)
    mBestSector1: float = _t(ctypes.c_double)
    mBestSector2: float = _t(ctypes.c_double)
    mBestLapTime: float = _t(ctypes.c_double)
    mLastSector1: float = _t(ctypes.c_double)
    mLastSector2: float = _t(ctypes.c_double)
    mLastLapTime: float = _t(ctypes.c_double)
    mCurSector1: float = _t(ctypes.c_double)
    mCurSector2: float = _t(ctypes.c_double)
    mNumPitstops: int = _t(ctypes.c_short)
    mNumPenalties: int = _t(ctypes.c_short)
    mIsPlayer: bool = _t(ctypes.c_bool)
    mControl: int = _t(ctypes.c_byte)
    mInPits: bool = _t(ctypes.c_bool)
    mPlace: int = _t(ctypes.c_ubyte)
    mVehicleClass: bytes = _t(ctypes.c_char * 32)
    mTimeBehindNext: float = _t(ctypes.c_double)
    mLapsBehindNext: int = _t(ctypes.c_int)
    mTimeBehindLeader: float = _t(ctypes.c_double)
    mLapsBehindLeader: int = _t(ctypes.c_int)
    mLapStartET: float = _t(ctypes.c_double)
    mPos: LMUVect3 = _t(LMUVect3)
    mLocalVel: LMUVect3 = _t(LMUVect3)
    mLocalAccel: LMUVect3 = _t(LMUVect3)
    mOri: list[LMUVect3] = _t(LMUVect3 * 3)
    mLocalRot: LMUVect3 = _t(LMUVect3)
    mLocalRotAccel: LMUVect3 = _t(LMUVect3)
    mHeadlights: int = _t(ctypes.c_ubyte)
    mPitState: int = _t(ctypes.c_ubyte)
    mServerScored: int = _t(ctypes.c_ubyte)
    mIndividualPhase: int = _t(ctypes.c_ubyte)
    mQualification: int = _t(ctypes.c_int)
    mTimeIntoLap: float = _t(ctypes.c_double)
    mEstimatedLapTime: float = _t(ctypes.c_double)
    mPitGroup: bytes = _t(ctypes.c_char * 24)
    mFlag: int = _t(ctypes.c_ubyte)
    mUnderYellow: bool = _t(ctypes.c_bool)
    mCountLapFlag: int = _t(ctypes.c_ubyte)
    mInGarageStall: bool = _t(ctypes.c_bool)
    mUpgradePack: list[int] = _t(ctypes.c_ubyte * 16)
    mPitLapDist: float = _t(ctypes.c_float)
    mBestLapSector1: float = _t(ctypes.c_float)
    mBestLapSector2: float = _t(ctypes.c_float)
    mSteamID: int = _t(ctypes.c_ulonglong)
    mVehFilename: bytes = _t(ctypes.c_char * 32)
    mAttackMode: int = _t(ctypes.c_short)
    mFuelFraction: int = _t(ctypes.c_ubyte)
    mDRSState: bool = _t(ctypes.c_bool)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 4)


@typedstruct(pack=4)
class LMUScoringInfo(ctypes.Structure):
    """Mapping of 'ScoringInfoV01' from InternalsPlugin.hpp

    Attributes:
        mTrackName: current track name
        mSession: current session (0=testday 1-4=practice 5-8=qual 9=warmup 10-13=race)
        mCurrentET: current time
        mEndET: ending time
        mMaxLaps: maximum laps
        mLapDist: distance around track
        mResultsStreamPointer: (pointer) results stream additions since last update (newline-delimited and NULL-terminated)
        mNumVehicles: current number of vehicles
        mGamePhase: Game phases:
            - 0 Before session has begun
            - 1 Reconnaissance laps (race only)
            - 2 Grid walk-through (race only)
            - 3 Formation lap (race only)
            - 4 Starting-light countdown has begun (race only)
            - 5 Green flag
            - 6 Full course yellow / safety car
            - 7 Session stopped
            - 8 Session over
            - 9 Paused (tag.2015.09.14 - this is new, and indicates that this is a heartbeat call to the plugin)
        mYellowFlagState: Yellow flag states (applies to full-course only)
            - -1 Invalid
            - 0 None
            - 1 Pending
            - 2 Pits closed
            - 3 Pit lead lap
            - 4 Pits open
            - 5 Last lap
            - 6 Resume
            - 7 Race halt (not currently used)
        mSectorFlag: whether there are any local yellows at the moment in each sector (not sure if sector 0 is first or last, so test)
        mStartLight: start light frame (number depends on track)
        mNumRedLights: number of red lights in start sequence
        mInRealtime: in realtime as opposed to at the monitor
        mPlayerName: player name (including possible multiplayer override)
        mPlrFileName: may be encoded to be a legal filename
        mDarkCloud: cloud darkness? 0.0-1.0
        mRaining: raining severity 0.0-1.0
        mAmbientTemp: temperature (Celsius)
        mTrackTemp: temperature (Celsius)
        mWind: wind speed
        mMinPathWetness: minimum wetness on main path 0.0-1.0
        mMaxPathWetness: maximum wetness on main path 0.0-1.0
        mGameMode: 1 = server, 2 = client, 3 = server and client
        mIsPasswordProtected: is the server password protected
        mServerPort: the port of the server (if on a server)
        mServerPublicIP: the public IP address of the server (if on a server)
        mMaxPlayers: maximum number of vehicles that can be in the session
        mServerName: name of the server
        mStartET: start time (seconds since midnight) of the event
        mAvgPathWetness: average wetness on main path 0.0-1.0
        mSessionTimeRemaining: session time remaining
        mTimeOfDay: time of day (0 to 86400)
        mIsFixedSetup: is fixed setup
        mTrackGripLevel: Track Grip (Rubber) Level (can be washed away in rain):
            - 0 = green
            - 1 = low
            - 2 = medium
            - 3 = high (heavy)
            - 4 = saturated
        mCloudCoverage: Sky type:
            - 0 = clear
            - 1 = light clouds
            - 2 = partially cloudy
            - 3 = mostly cloudy
            - 4 = overcast
            - 5 = cloudy & drizzle
            - 6 = cloudy & light rain
            - 7 = overcast & light rain
            - 8 = overcast & rain
            - 9 = overcast & heavy rain
            - 10 = overcast & storm
        mTrackLimitsStepsPerPenalty: track limits steps per penalty
        mTrackLimitsStepsPerPoint: track limits steps per point
        mExpansion: future use
        mVehiclePointer: (pointer) keeping this at the end of the structure to make it easier to replace in future versions
    """

    __slots__ = ()

    mTrackName: bytes = _t(ctypes.c_char * 64)
    mSession: int = _t(ctypes.c_int)
    mCurrentET: float = _t(ctypes.c_double)
    mEndET: float = _t(ctypes.c_double)
    mMaxLaps: int = _t(ctypes.c_int)
    mLapDist: float = _t(ctypes.c_double)
    mResultsStreamPointer: list[int] = _t(ctypes.c_ubyte * 8)
    mNumVehicles: int = _t(ctypes.c_int)
    mGamePhase: int = _t(ctypes.c_ubyte)
    mYellowFlagState: int = _t(ctypes.c_char)
    mSectorFlag: list[int] = _t(ctypes.c_ubyte * 3)
    mStartLight: int = _t(ctypes.c_ubyte)
    mNumRedLights: int = _t(ctypes.c_ubyte)
    mInRealtime: bool = _t(ctypes.c_bool)
    mPlayerName: bytes = _t(ctypes.c_char * 32)
    mPlrFileName: bytes = _t(ctypes.c_char * 64)
    mDarkCloud: float = _t(ctypes.c_double)
    mRaining: float = _t(ctypes.c_double)
    mAmbientTemp: float = _t(ctypes.c_double)
    mTrackTemp: float = _t(ctypes.c_double)
    mWind: LMUVect3 = _t(LMUVect3)
    mMinPathWetness: float = _t(ctypes.c_double)
    mMaxPathWetness: float = _t(ctypes.c_double)
    mGameMode: int = _t(ctypes.c_ubyte)
    mIsPasswordProtected: bool = _t(ctypes.c_bool)
    mServerPort: int = _t(ctypes.c_ushort)
    mServerPublicIP: int = _t(ctypes.c_uint)
    mMaxPlayers: int = _t(ctypes.c_int)
    mServerName: bytes = _t(ctypes.c_char * 32)
    mStartET: float = _t(ctypes.c_float)
    mAvgPathWetness: float = _t(ctypes.c_double)
    mSessionTimeRemaining: float = _t(ctypes.c_float)
    mTimeOfDay: float = _t(ctypes.c_float)
    mIsFixedSetup: bool = _t(ctypes.c_bool)
    mTrackGripLevel: int = _t(ctypes.c_uint8)
    mCloudCoverage: int = _t(ctypes.c_uint8)
    mTrackLimitsStepsPerPenalty: int = _t(ctypes.c_uint8)
    mTrackLimitsStepsPerPoint: int = _t(ctypes.c_uint8)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 187)
    mVehiclePointer: list[int] = _t(ctypes.c_ubyte * 8)


@typedstruct(pack=4)
class LMUApplicationState(ctypes.Structure):
    """Mapping of 'ApplicationStateV01' from InternalsPlugin.hpp

    Attribute:
        mAppWindow: HWND, application window handle
        mWidth: screen width
        mHeight: screen height
        mRefreshRate: refresh rate
        mWindowed: really just a boolean whether we are in windowed mode
        mOptionsLocation: 0=main UI, 1=track loading, 2=monitor, 3=on track
        mOptionsPage: the name of the options page
        mExpansion: future use
    """

    __slots__ = ()

    mAppWindow: int = _t(ctypes.c_ulonglong)
    mWidth: int = _t(ctypes.c_uint)
    mHeight: int = _t(ctypes.c_uint)
    mRefreshRate: int = _t(ctypes.c_uint)
    mWindowed: int = _t(ctypes.c_uint)
    mOptionsLocation: int = _t(ctypes.c_ubyte)
    mOptionsPage: bytes = _t(ctypes.c_char * 31)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 204)


# SharedMemoryInterface
@typedstruct(pack=4)
class LMUScoringData(ctypes.Structure):
    """Mapping of 'SharedMemoryScoringData' from SharedMemoryInterface.hpp

    Attributes:
        scoringInfo: scoring info
        scoringStreamSize: scoring stream size
        vehScoringInfo: vehicle scoring info
        scoringStream: scoring stream data
    """

    __slots__ = ()

    scoringInfo: LMUScoringInfo = _t(LMUScoringInfo)
    scoringStreamSize: list[int] = _t(ctypes.c_ubyte * 12)
    vehScoringInfo: list[LMUVehicleScoring] = _t(LMUVehicleScoring * LMUConstants.MAX_MAPPED_VEHICLES)
    scoringStream: bytes = _t(ctypes.c_char * 65536)


@typedstruct(pack=4)
class LMUTelemetryData(ctypes.Structure):
    """Mapping of 'SharedMemoryTelemtryData' from SharedMemoryInterface.hpp

    Attributes:
        activeVehicles: active vehicles
        playerVehicleIdx: player vehicle index
        playerHasVehicle: whether player has vehicle
        telemInfo: vehicle telemetry info
    """

    __slots__ = ()

    activeVehicles: int = _t(ctypes.c_uint8)
    playerVehicleIdx: int = _t(ctypes.c_uint8)
    playerHasVehicle: bool = _t(ctypes.c_bool)
    telemInfo: list[LMUVehicleTelemetry] = _t(LMUVehicleTelemetry * LMUConstants.MAX_MAPPED_VEHICLES)


@typedstruct(pack=4)
class LMUPathData(ctypes.Structure):
    """Mapping of 'SharedMemoryPathData' from SharedMemoryInterface.hpp

    Attributes:
        userData: user data path
        customVariables: custom variables path
        stewardResults: steward results path
        playerProfile: player profile path
        pluginsFolder: plugins folder path
    """

    __slots__ = ()

    userData: bytes = _t(ctypes.c_char * LMUConstants.MAX_PATH_LENGTH)
    customVariables: bytes = _t(ctypes.c_char * LMUConstants.MAX_PATH_LENGTH)
    stewardResults: bytes = _t(ctypes.c_char * LMUConstants.MAX_PATH_LENGTH)
    playerProfile: bytes = _t(ctypes.c_char * LMUConstants.MAX_PATH_LENGTH)
    pluginsFolder: bytes = _t(ctypes.c_char * LMUConstants.MAX_PATH_LENGTH)


@typedstruct(pack=4)
class LMUEvent(ctypes.Structure):
    """Remapping of 'SharedMemoryEvent' enum as struct from SharedMemoryInterface.hpp"""

    __slots__ = ()

    SME_ENTER: int = _t(ctypes.c_uint)
    SME_EXIT: int = _t(ctypes.c_uint)
    SME_STARTUP: int = _t(ctypes.c_uint)
    SME_SHUTDOWN: int = _t(ctypes.c_uint)
    SME_LOAD: int = _t(ctypes.c_uint)
    SME_UNLOAD: int = _t(ctypes.c_uint)
    SME_START_SESSION: int = _t(ctypes.c_uint)
    SME_END_SESSION: int = _t(ctypes.c_uint)
    SME_ENTER_REALTIME: int = _t(ctypes.c_uint)
    SME_EXIT_REALTIME: int = _t(ctypes.c_uint)
    SME_UPDATE_SCORING: int = _t(ctypes.c_uint)
    SME_UPDATE_TELEMETRY: int = _t(ctypes.c_uint)
    SME_INIT_APPLICATION: int = _t(ctypes.c_uint)
    SME_UNINIT_APPLICATION: int = _t(ctypes.c_uint)
    SME_SET_ENVIRONMENT: int = _t(ctypes.c_uint)
    SME_FFB: int = _t(ctypes.c_uint)
    # omit "SME_MAX"


@typedstruct(pack=4)
class LMUGeneric(ctypes.Structure):
    """Mapping of 'SharedMemoryGeneric' from SharedMemoryInterface.hpp

    Attributes:
        events: event
        gameVersion: game version
        FFBTorque: force feedback torque
        appInfo: application state
    """

    __slots__ = ()

    events: LMUEvent = _t(LMUEvent)
    gameVersion: int = _t(ctypes.c_int)
    FFBTorque: float = _t(ctypes.c_float)
    appInfo: LMUApplicationState = _t(LMUApplicationState)


@typedstruct(pack=4)
class LMUObjectOut(ctypes.Structure):
    """Mapping of 'SharedMemoryObjectOut' from SharedMemoryInterface.hpp

    Attributes:
        generic: generic data
        paths: path data
        scoring: scoring data
        telemetry: telemetry data
    """

    __slots__ = ()

    generic: LMUGeneric = _t(LMUGeneric)
    paths: LMUPathData = _t(LMUPathData)
    scoring: LMUScoringData = _t(LMUScoringData)
    telemetry: LMUTelemetryData = _t(LMUTelemetryData)


@typedstruct(pack=4)
class LMULayout(ctypes.Structure):
    """Mapping of 'SharedMemoryLayout' from SharedMemoryInterface.hpp"""

    __slots__ = ()

    data: LMUObjectOut = _t(LMUObjectOut)


# Memory map
class SimInfo:
    """Simulation info from shared memory"""

    def __init__(self):
        self._lmu_data = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(LMUObjectOut),
            tagname=LMUConstants.LMU_SHARED_MEMORY_FILE,
        )
        self.LMUData = LMUObjectOut.from_buffer(self._lmu_data)

    def save(self, filename: str):
        """Save buffer data to file"""
        with open(filename, "wb") as output:
            output.write(bytes(self._lmu_data))

    def close(self):
        """Close memory map"""
        self.LMUData = None

        try:  # this did not help with the errors
            self._lmu_data.close()
        except BufferError as e:
            print("Error:", e)

    def __del__(self):
        self.close()

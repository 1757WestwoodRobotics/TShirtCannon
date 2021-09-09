import commands2

import constants

from .drivedistance import DriveDistance

from subsystems.drivesubsystem import DriveSubsystem


class ComplexAuto(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, right, backwards, left.
    """

    def __init__(self, drive: DriveSubsystem):
        super().__init__(
            # Drive forward the specified distance
            DriveDistance(
                constants.kAutoFrontwaysDistance,
                constants.kAutoDriveSpeedFactor,
                DriveDistance.Axis.X,
                drive,
            ),
            # Drive backward the specified distance
            DriveDistance(
                -1 * constants.kAutoSidewaysDistance,
                constants.kAutoDriveSpeedFactor,
                DriveDistance.Axis.Y,
                drive,
            ),
            DriveDistance(
                -1 * constants.kAutoFrontwaysDistance,
                constants.kAutoDriveSpeedFactor,
                DriveDistance.Axis.X,
                drive,
            ),
            # Drive backward the specified distance
            DriveDistance(
                constants.kAutoSidewaysDistance,
                constants.kAutoDriveSpeedFactor,
                DriveDistance.Axis.Y,
                drive,
            ),
        )

import math
import typing
from wpimath.geometry import Rotation2d, Translation2d, Pose2d

number = typing.Union[float, int]


def clamp(inputValue: float, minimum: float, maximum: float) -> float:
    return max(min(inputValue, maximum), minimum)


def normalizeRotation(inputRotation: Rotation2d) -> Rotation2d:
    """
    Normalize the given rotation to the range [-pi, pi)
    """
    inputAngle = inputRotation.radians()
    return Rotation2d(
        inputAngle - 2 * math.pi * math.floor((inputAngle + math.pi) / (2 * math.pi))
    )


def translationFromDistanceAndRotation(
    distance: float, rotation: Rotation2d
) -> Translation2d:
    return Translation2d(distance * rotation.cos(), distance * rotation.sin())


def rotationFromTranslation(translation: Translation2d) -> Rotation2d:
    return Rotation2d(math.atan2(translation.Y(), translation.X()))


def rotateAroundPoint(
    pose: Pose2d, position: Translation2d, rotation: Rotation2d
) -> Pose2d:
    deltaTranslation = pose.translation() - position
    newRotation = rotation + pose.rotation()

    rotatedTranslation = translationFromDistanceAndRotation(
        deltaTranslation.distance(Translation2d()),
        rotationFromTranslation(deltaTranslation) + rotation,
    )

    return Pose2d(rotatedTranslation + position, newRotation)


def map_range(
    value: number,
    inputMin: number,
    inputMax: number,
    outputMin: number,
    outputMax: number,
):
    return (value - inputMin) * (outputMax - outputMin) / (
        inputMax - inputMin
    ) + outputMin

from math import sin, tau, floor, cos
from wpimath.geometry import Rotation2d


def optimizeAngle(currentAngle: Rotation2d, targetAngle: Rotation2d) -> Rotation2d:
    currentAngle = currentAngle.radians()

    closestFullRotation = (
        floor(abs(currentAngle / tau)) * (-1 if currentAngle < 0 else 1) * tau
    )

    currentOptimalAngle = targetAngle.radians() + closestFullRotation - currentAngle

    potentialNewAngles = [
        currentOptimalAngle,
        currentOptimalAngle - tau,
        currentOptimalAngle + tau,
    ]  # closest other options

    deltaAngle = tau  # max possible error, a full rotation!
    for potentialAngle in potentialNewAngles:
        if abs(deltaAngle) > abs(potentialAngle):
            deltaAngle = potentialAngle

    return Rotation2d(deltaAngle + currentAngle)


def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.
    Input
      :param roll: The roll (rotation around x-axis) angle in radians.
      :param pitch: The pitch (rotation around y-axis) angle in radians.
      :param yaw: The yaw (rotation around z-axis) angle in radians.
    Output
      :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) - cos(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)
    qy = cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * cos(
        pitch / 2
    ) * sin(yaw / 2)
    qz = cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) - sin(roll / 2) * sin(
        pitch / 2
    ) * cos(yaw / 2)
    qw = cos(roll / 2) * cos(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)

    return [qx, qy, qz, qw]
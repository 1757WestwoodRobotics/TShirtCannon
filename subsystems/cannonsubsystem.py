from enum import Enum, auto
from commands2 import SubsystemBase
from ctre import WPI_TalonSRX
from wpilib import Relay, Solenoid, PneumaticsModuleType, AnalogInput, SmartDashboard
import constants, typing


number = typing.Union[float, int]


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


class CannonSubsystem(SubsystemBase):
    class State(Enum):
        Closed = auto()
        Filling = auto()
        Launching = auto()

    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.launchSolonoid = WPI_TalonSRX(constants.kCannonLaunchVictorDeviceID)
        self.fillSolonoid = Solenoid(
            constants.kPCMCannonCanID,
            PneumaticsModuleType.CTREPCM,
            constants.kCannonFillPCMID,
        )
        self.compresser = Relay(0,direction=Relay.Direction.kForwardOnly)
        self.pressure = AnalogInput(constants.kCannonPressureAnalogInput)
        self.launchSolonoid.configFactoryDefault()

        self.fillSolonoid.set(False)
        self.launchSolonoid.set(0.0)
        self.state = CannonSubsystem.State.Closed

        self.compresser.set(Relay.Value.kOn)

    def periodic(self) -> None:
        self.compresser.set(Relay.Value.kOn)
        SmartDashboard.putNumber(constants.kCannonStateKey, self.state.value)
        SmartDashboard.putNumber(constants.kPressureKey, self.getPressure())

    def getPressure(self) -> float:
        return map_range(
            self.pressure.getVoltage(),
            constants.kVoltageOutMin,
            constants.kVoltageOutMax,
            constants.kPressureInMin,
            constants.kPressureInMax,
        )

    def close(self) -> None:
        """close all the solonoids"""
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(0.0)
        self.state = CannonSubsystem.State.Closed
        print("CLOSING")

    def fill(self) -> None:
        """begins filling staging tank"""
        print("FILLING")
        self.launchSolonoid.set(0.0)
        self.fillSolonoid.set(True)
        print(self.fillSolonoid.get())
        self.state = CannonSubsystem.State.Filling

    def launch(self) -> None:
        """lets air escape through the end of the cannon"""
        print("LAUNCHING")
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(1.0)
        print(self.launchSolonoid.get())
        self.state = CannonSubsystem.State.Launching

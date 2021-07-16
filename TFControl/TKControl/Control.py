
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_stepper import BrickStepper
from tinkerforge.bricklet_io4 import BrickletIO4

from time import sleep

class TFStepper(BrickStepper):

    def __init__(self, stepperUID, ioUID, ioPort, ipcon): 
        """
        This constructor is mostly just a wrapper for the proper
        BrickStepper constructor, but it also instantiates the IO brick,
        which is used to ensure the steppers stays within it's range of motion
       
        Parameters
        ----------

        stepperUID : The UID of the stepper brick

        ioUID : The UID of the IO bricklet

        ioPort : The port number that the stepper is connected to the IO bricklet
            with (should be 0, 1, 2, or 3)

        ipcon : The IP connection used to connect to the bricks

        """
        self._stepperUID = stepperUID
        self._ioUID = ioUID
        self._ioPort = ioPort
        self._ipcon = ipcon

        super().__init__(stepperUID, ipcon)

        self._ioBricklet = BrickletIO4(ioUID, ipcon)


    def isInBounds(self):
        return bool(format(self._ioBricklet.get_value(), "04b")[3 - self._ioPort])

    def resetPosition(self):
        """
        Move the stepper all the way to the edge of the range of motion
        and set that position to be 0
        """

        def callback_func(stepper):
            stepper.set_steps(-1)

        stepper.register_callback(stepper.CALLBACK_POSITION_REACHED,
                lambda x: callback_func(x, stepper))
        stepper.set_steps(-1)

        # Wait for the stage to get to the edge of the range of motion
        while self.isInBounds():
            pass

        stepper.stop()
        sleep(.5)

        # Now move some amount back to the center
        stepper.set_steps(25000)
        while abs(stepper.get_remaining_steps()) > 0:
            pass

        sleep(.5)
        stepper.disable()


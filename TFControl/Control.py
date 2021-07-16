
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
        return bool(int(format(self._ioBricklet.get_value(), "04b")[3 - self._ioPort]))

    def resetPosition(self):
        """
        Move the stepper all the way to the edge of the range of motion
        and set that position to be 0
        """
        self.enable()

        def callback_func(position, stepper):
            stepper.set_steps(-1)

        self.register_callback(self.CALLBACK_POSITION_REACHED,
                lambda x: callback_func(x, self))
        self.set_steps(-1)

        # Wait for the stage to get to the edge of the range of motion
        while self.isInBounds():
            pass

        self.stop()
        sleep(.5)

        # Reset the callback function
        def callback_func(position, stepper):
            pass

        self.register_callback(self.CALLBACK_POSITION_REACHED,
                lambda x: callback_func(x, self))

        # Now move some amount back to the center
        self.set_steps(25000)
        while abs(self.get_remaining_steps()) > 0:
            pass

        sleep(.5)
        self.disable()


import sys
import clr
import os

ASSEMBLY_FILE = 'ESP301_CommandInterface'
CURR_DIR = os.path.dirname(__file__)

# Constants for the motion controller
BAUD_RATE = 921600

# Add the reference to the .Net library so we can use it
sys.path.append(CURR_DIR)
clr.AddReference(ASSEMBLY_FILE)

from CommandInterfaceESP301 import *

# A very small wrapper just to make the calling of methods a little more verbose
class RotationStage():

    def __init__(self, comPort='COM4', axisNum=1):
        self._espDev = ESP301()
        self._axisNum = axisNum # Where the stage is plugged into the motion controller
        self._comPort = comPort
        pass

    def connect(self):
        """
        Establish the connection to the motion controller. Must be run before using any other commands.
        """
        return self._espDev.OpenInstrument(self._comPort, BAUD_RATE)

    def disconnect(self):
        """
        Disconnect from the motion controller, preventing any further commands from being issued.
        """
        return self._espDev.CloseInstrument()

    def getAngle(self):
        """
        Get the current angle reading of the stage. Note that this is the *actual* angle,
        which may differ slightly from what the angle is supposed to be.
        """
        errorMsg = ''
        angle = 0
        status, angle, errorMsg = self._espDev.TP(self._axisNum, angle, errorMsg)

        if status == 0:
            return angle

        else:
            raise Exception('Error reading angle: ' + errorMsg)

    def moveRelative(self, deltaTheta, wait=True):
        """
        Move the rotation stage by some number of degrees relative to the current position.
        """
        errorMsg = ''
        status, errorMsg = self._espDev.PR(self._axisNum, deltaTheta, errorMsg)

        if wait:
            while True:
                # The 0 is passed in as 'delay' but I don't really know what it does
                ret, done, errorMsg = self._espDev.MD(self._axisNum, 0, errorMsg)

                if done:
                    break

        return status

    def moveAbsolute(self, theta, wait=True):
        """
        Move the rotation stage to some angle, relative to 0 position.

        For large numbers of small movements, it is more accurate to calculate the angles
        beforehand and move absolutely, as opposed to moving by a fixed relative angle.
        """
        errorMsg = ''
        status, errorMsg = self._espDev.PA_Set(self._axisNum, theta, errorMsg)

        if wait:
            while True:
                # The 0 is passed in as 'delay' but I don't really know what it does
                ret, done, errorMsg = self._espDev.MD(self._axisNum, 0, errorMsg)

                if done:
                    break

        return status

    def stop(self):
        """
        Stop the stage from moving.
        """
        errorMsg = ''
        return self._espDev.ST(errorMsg)

    def setVelocity(self, velocity):
        """
        Set the velocity that the stage rotates with, in degrees/second. Note that this
        is not setting the *current* velocity.
        """
        errorMsg = ''
        status, errorMsg = self._espDev.VA_Set(self._axisNum, velocity, errorMsg)
        return status

    def getVelocity(self):
        """
        Get the velocity that the stage rotates with, in degrees/second. Note that this is
        not the current velocity of the stage.
        """
        errorMsg = ''
        status, velocity, errorMsg = self._espDev.VA_Get(self._axisNum, 0, errorMsg)
        if status == 0:
            return velocity
        return None 

    def isMoving(self):
        """
        Returns whether or not the stage is currently moving to a new position.
        """
        errorMsg = ''
        ret, done, errorMsg = self._espDev.MD(self._axisNum, 0, errorMsg)

        return bool(done)
        
       
    def resetToHome(self):
        """
        Return the the position denoted as "home", which is persistent as the device is
        turned off/unplugged/etc.
        """
        errorMsg = ''
        status, errorMsg = self._espDev.OR(self._axisNum, 0, errorMsg)
        return status

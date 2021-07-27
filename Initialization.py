
# Various serial numbers and things
from Utils import timeout
import Settings

def fastInitialization(printInfo=True):
    """
    Determine which components are available without giving any diagnostic advice.

    Returns
    -------

    True : All components available
    False : Not all components available
    """
    failed = False

    def printif(msg, **kwargs):
        if printInfo:
            print(msg, **kwargs)

    # Make sure the imports are all set
    try:
        import TLBP2Control
        import ESP301Control

        from tinkerforge.ip_connection import IPConnection
        from tinkerforge.bricklet_humidity import BrickletHumidity
        from tinkerforge.bricklet_temperature import BrickletTemperature

    except Exception as e:
        printif("Not all imports are available: {e}")
        return False

    # First, check the rotation stage

    printif('Rotation stage' + '.'*20, end='')
    try:
        rotStage = ESP301Control.RotationStage(Settings.MOTION_CONTROLLER_PORT, Settings.ROTATION_STAGE_AXIS_NUM)
        # Have to have a timeout, so it doesn't hang forever
        # This one should be pretty instant if it is working correctly, so
        # the timeout doesn't need to be that long
        @timeout(2) 
        def testStage():
            return rotStage.connect()

        testStage()
        printif('Working')

        rotStage.disconnect()
    except:
        printif('Error')
        failed = True

    # Next, check the beam profiler

    printif('Beam profiler' + '.'*21, end='')
    try:
        bpDevice = TLBP2Control.TLBP2()

        # It can take a moment to get the pipe working, so this timeout is a little longer
        # The drum also has to run up to speed, which can take ~10 seconds
        @timeout(20)
        def testBP():
            return bpDevice.connect()
        status = testBP()

        # Measure just to make sure it doesn't throw an error
        measure = bpDevice.getMeasurement()

        if status == 0:
            printif('Working')
        else:
            printif('Error')
            failed = True
        
        bpDevice.disconnect()
    except:
        printif('Error')
        failed = True

    # Next, the tinkerforge stuff
    printif('Tinkerforge brick' + '.'*17, end='')
    try:
        ipcon = IPConnection()
        humidity = BrickletHumidity(Settings.TF_HUMIDITY_UID, ipcon)
        temperature = BrickletTemperature(Settings.TF_TEMP_UID, ipcon)

        ipcon.connect(TF_HOST, TF_PORT)

        # Try each one to check

        printif(5 * ' ' + 'Humidity sensor' + '.'*14, end='')
        try:
            humidity.get_humidity()
            printif('Working')
        except:
            printif('Error')
            failed = True

        printif(5 * ' ' + 'Temperature sensor' + '.'*11, end='')
        try:
            temperature.get_temperature()
            printif('Working')
        except:
            printif('Error')
            failed = True

        ipcon.disconnect()
    except:
        printif('Error')
        failed = True

    printif('Initialization complete!')
    return not failed


def fullInitialization():
    """
    Determine which components are available, including diagnostic information and
    hints/tips to get everything working.
    """

    print('='*50)
    print(' '*15 + 'COMPONENT INITIALIZATION')
    print('='*50)
    
    print("Howdy!\n")
    print("This procedure will ensure that all of the components for the index of refraction" +
            "\nmeasurement are available and ready to control from other Python scripts." +
            "\n\nThis will address issues relating to software installations, hardware connections," +
            "\nand whatever else might be wrong."
            )

    print("\nThe program will often ask for user input if there are any issues. Usually, pressing" + 
            "\nenter will retry that check, giving you a chance to fix any issues that were brought" + 
            "\nup. You may also type \"skip\" to skip that initialization check, though of course it may" +
            "\nresult in that component not working later on."
            )

    componentsToCheck = ['Rotation stage', 'Beam profiler',
            'Tinkerforge humidity sensor', 'Tinkerforge temperature sensor']

    print(f"There are {len(componentsToCheck)} components that will be checked as a part of this process:")
    for c in componentsToCheck:
        print(5*' ' + c)

    print("\n\nPress enter to continue on to checking that all libraries are available!")
    print(">>> ", end='')
    key = input()

    print('='*50)
    print(' '*15 + 'LIBRARY INITIALIZATION')
    print('='*50)

    #librariesToCheck = ["pythonnet", "pywin32", "tinkerforge", "ESP301Control", "TLBP2Control"]
    librariesToCheck = []

    if key != "skip":
        # Check the stock libraries first

        print(5*' ' + 'pythonnet' + '.'*17, end='')
        try:
            import clr
            print('Working')
        except:
            print('Error')
            librariesToCheck.append("pythonnet")

        print(5*' ' + 'pywin32' + '.'*19, end='')
        try:
            import win32pipe, win32file
            print('Working')
        except:
            print('Error')
            librariesToCheck.append("pywin32")

        print(5*' ' + 'tinkerforge' + '.'*15, end='')
        try:
            import tinkerforge
            print('Working')
        except:
            print('Error')
            librariesToCheck.append("tinkerforge")

        # Now the custom libraries

        print(5*' ' + 'ESP301Control' + '.'*13, end='')
        try:
            import ESP301Control
            print('Working')
        except:
            print('Error')
            librariesToCheck.append("ESP301Control")


        print(5*' ' + 'TLBP2Control' + '.'*14, end='')
        try:
            import TLBP2Control
            print('Working')
        except:
            print('Error')
            librariesToCheck.append("TLBP2Control")


        # Now give some advice on how to fix any of the issues (if there are any)

        if "pythonnet" in librariesToCheck:
            print("\npythonnet can be installed via pip as:\n" + ' '*5 + "pip install pythonnet.")
            print("\nMake sure that you have .NETCore v3.1 installed, and you may also need .NET v5.0:")
            print(' '*5 + "https://dotnet.microsoft.com/download/dotnet/3.1")
            print(' '*5 + "https://dotnet.microsoft.com/download/dotnet/5.0")

        if "pywin32" in librariesToCheck:
            print("\n\npywin32 can be installed via pip as:\n" + ' '*5 + "pip install pywin32")

        if "tinkerforge" in librariesToCheck:
            print("\n\ntinkerforge can be installed via pip as:\n" + ' '*5 + "pip install tinkerforge.")
            print("\nMake sure that you have the brick daemon installed and running:")
            print(' '*5 + "https://www.tinkerforge.com/en/doc/Downloads.html#downloads-tools")

        if "ESP301Control" in librariesToCheck:
            print("\n\nESP301Control cannot be installed via pip as it is my custom interface to work with" + 
                    "\nthe motion controller and rotational stage. It should be included in this repo, " + 
                    "\nbut in the case that it is missing, it can be downloaded from the source:")
            print(' '*5 + "link")
            print("\nThe library will require that you have .NETCore installed, as it makes use of a managed" + 
                    "\nassembly from Newport:")
            print(' '*5 + "https://dotnet.microsoft.com/download/dotnet/3.1")
            print("\nSee the README file in the source folder for more information about this library.")

        if "TLBP2Control" in librariesToCheck:
            print("\n\nTLBP2Control cannot be installed via pip as it is my custom interface to work with" + 
                    "\nthe Thorlabs beam profiler. It should be included in this repo, " + 
                    "\nbut in the case that it is missing, it can be downloaded from the source:")
            print(' '*5 + "link")
            print("\nThe library will require that you have .NETCore installed, as it runs a C# server in the" + 
                    "\nbackground to control the beam profiler:")
            print(' '*5 + "https://dotnet.microsoft.com/download/dotnet/3.1")
            print("\nSee the README file in the source folder for more information about this library.")

            # None of the hardware stuff will work if the libraries aren't there, so we have to exit
            if len(librariesToCheck) > 0:
                print("\n\nLibrary issues must be resolved before continuing on to hardware initialization!" +
                        "\n\nPlease follow the directions above and rerun this script once any issues have been resolved.")
                return

    else:
        print("Skipped")

    print("\n\nPress enter to continue on to checking the rotation stage!")
    print(">>> ", end='')
    key = input()

    print('='*50)
    print(' '*15 + 'ROTATION STAGE INITIALIZATION')
    print('='*50)

    if key != "skip":
        
        while True:
            try:

                print("Attempting to connect to the motion controller...", end='')
                # Library step may have been skipped, so import again just in case
                import ESP301Control

                rotStage = ESP301Control.RotationStage(Settings.MOTION_CONTROLLER_PORT, Settings.ROTATION_STAGE_AXIS_NUM)
                # Have to have a timeout, so it doesn't hang forever
                # This one should be pretty instant if it is working correctly, so
                # the timeout doesn't need to be that long
                @timeout(4) 
                def testStage():
                    return rotStage.connect()

                status = testStage()
                if status != 0:
                    raise Exception()

                print('connection successful!')
                
                rotStage.disconnect()
                
                break
            except:
                print('connection failed!')

                print('(A window may have opened saying that the COM port couldn\'t be found; feel free to close it)')

                print('\nSince the rotational stage could not be found, please follow these diagnostic steps:')
                print(' '*5 + '1. Make sure that the motion controller is plugged in and powered on')
                print(' '*5 + f'2. Make sure that the rotation stage is plugged into the motion controller in slot {Settings.ROTATION_STAGE_AXIS_NUM}')
                print(' '*10 + 'If you would like to change this slot number, see the Settings.py file')
                print(' '*5 + f'3. Make sure that the motion controller is plugged into the computer via USB and is detected on the port {Settings.MOTION_CONTROLLER_PORT}')
                print(' '*10 + 'If you would like to change this port number, see the Settings.py file')
                print(' '*10 + 'If it is not detected by the computer, use the manufacturer provided software to troubleshoot:')
                print(' '*10 + 'https://www.newport.com/p/ESP301-3N')
                print(' '*10 + 'You will likely need to install the driver which can be found at (after installing the above software)')
                print(' '*10 + r'C:\Newport\Motion Control\ESP301\Bin\USB Driver\64-bit')

                print('\nOnce you have gone through these steps, you may type \'retry\' to attempt connection again, \'skip\' to skip to the next' +
                        '\npart, or \'exit\' to exit the initialization procedure (possibly to edit the Settings.py file).')

                print('>>> ', end='')
                key = input()

                if key == 'retry':
                    continue
                elif key == 'exit':
                    return
                elif key == 'skip':
                    break
    else:
        print("Skipped")

    print("\n\nPress enter to continue on to checking the beam profiler!")
    print(">>> ", end='')
    key = input()

    print('='*50)
    print(' '*15 + 'BEAM PROFILER INITIALIZATION')
    print('='*50)

    if key != 'skip':
        while True:
            try:

                print("Attempting to connect to the beam profiler...", end='')
                import TLBP2Control

                bpDevice = TLBP2Control.TLBP2()

                # It can take a moment to get the pipe working, so this timeout is a little longer
                @timeout(20)
                def testBP():
                    return bpDevice.connect()
                status = testBP()

                # Measure just to make sure it doesn't throw an error
                measure = bpDevice.getMeasurement()

                if status == 0:
                    print('connection successful!')
                else:
                    raise Exception()

                bpDevice.disconnect()

                break

            except:
                print('connection failed!')

                print('\nSince the beam profiler could not be found, please follow these diagnostic steps:')
                print(' '*5 + '1. Make sure that the beam profiler is plugged into the computer')
                print(' '*5 + '2. Make sure that the beam profiler is detected by the manufacturer software:')
                print(' '*10 + 'https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Beam')

                print('\nOnce you have gone through these steps, you may type \'retry\' to attempt connection again, \'skip\' to skip to the next' +
                        '\npart, or \'exit\' to exit the initialization procedure.')

                print('>>> ', end='')
                key = input()

                if key == 'retry':
                    continue
                elif key == 'exit':
                    return
                elif key == 'skip':
                    break
    else:
        print('Skipped')

    print("\n\nPress enter to continue on to checking the tinkerforge components!")
    print(">>> ", end='')
    key = input()

    print('='*50)
    print(' '*15 + 'TINKERFORGE INITIALIZATION')
    print('='*50)

    if key != 'skip':

        while True:
            try:
                print("Attempting to connect to tinkerforge bricks...", end='')

                from tinkerforge.ip_connection import IPConnection
                from tinkerforge.bricklet_humidity import BrickletHumidity
                from tinkerforge.bricklet_temperature import BrickletTemperature

                ipcon = IPConnection()
                humidity = BrickletHumidity(Settings.TF_HUMIDITY_UID, ipcon)
                temperature = BrickletTemperature(Settings.TF_TEMP_UID, ipcon)

                ipcon.connect(Settings.TF_HOST, Settings.TF_PORT)

                # Try each one to check
                failed = False

                print(5 * ' ' + 'Humidity sensor' + '.'*14, end='')
                try:
                    humidity.get_humidity()
                    print('Working')
                except:
                    print('Error')
                    failed = True

                print(5 * ' ' + 'Temperature sensor' + '.'*11, end='')
                try:
                    temperature.get_temperature()
                    print('Working')
                except:
                    print('Error')
                    failed = True
 
                ipcon.disconnect()

                if failed:
                    raise Exception()

                print('connection successful!')
                break

            except Exception as e:
                print('connection failed!')

                print('\nSince at least one of the tinkerforge bricks could be found, please follow these diagnostic steps:')
                print(' '*5 + '1. Make sure that the tinkerforge brick is plugged into the computer (there should be an active LED on the board)')
                print(' '*5 + '2. Make sure that the brick daemon is installed and currently running:')
                print(' '*10 + "https://www.tinkerforge.com/en/doc/Downloads.html#downloads-tools")
                print(' '*5 + '3. Ensure that there is no other process running on the following host:port combination:')
                print(' '*10 + f'{Settings.TF_HOST}:{Settings.TF_PORT}')
                print(' '*5 + '4. Ensure that the following UIDs are correct. This can be seen in the BrickViewer program,')
                print(' '*5 + 'and any changes should be made in the Settings.py file:')
                print(' '*10 + f'Humidity: {Settings.TF_HUMIDITY_UID}')
                print(' '*10 + f'Temperature: {Settings.TF_TEMP_UID}')

                print('\nOnce you have gone through these steps, you may type \'retry\' to attempt connection again, \'skip\' to skip to the next' +
                        '\npart, or \'exit\' to exit the initialization procedure.')

                print('>>> ', end='')
                key = input()

                if key == 'retry':
                    continue
                elif key == 'exit':
                    return
                elif key == 'skip':
                    break
    else:
        print('Skipped')

    print('Initialization complete!')

# So that the file can be run from the command line
if __name__ == "__main__":
    fullInitialization()


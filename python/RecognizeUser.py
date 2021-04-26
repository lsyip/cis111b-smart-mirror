# Import necessary modules
import face_recognition # Facial Recognition API
import picamera    # PiCamera module
import numpy as np
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint     # pyfingerprint API
import RPi.GPIO as GPIO    # Needed for controlling GPIO Pins

# Create a reference to the camera
camera = picamera.PiCamera()
camera.resolution = (352, 240)    # Define the camera resolution
output = np.empty((240, 352, 3), dtype=np.uint8) # Creates an array  of given dimensions

# Load the picture of the user.
userImage = face_recognition.load_image_file("alex1.png")
userFaceEncoding = face_recognition.face_encodings(userImage)[0]

# Create a reference to the fingerprint scanner
fingerScanner = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

# Specify GPIO PIN numbering mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up the pin being used for activating the solenoid
GPIO.setup(7, GPIO.OUT, initial - GPIO.LOW)

# Initialize 2 lists for storing face details and encodings
faceLocations = []
faceEncodings = []

# Get a picture of the user currently in front of the mirror
camera.capture(output, format = "rgb")

# Define the face and face encoding in the current frame
faceLocations = face_recognition.face_locations(output)

# If you can't read the face, notify the user
if(len(faceLocations) == 0):
    print("No Face Detected")

# Encode the face found in frame
faceEncodings = face_recognition.face_encodings(output, faceLocations)

# compare the current user face encoding with the user encoding in the database
for faceEncoding in faceEncodings:
    match = face_recognition.compare_faces([userFaceEncoding], faceEncoding)
    name = ""

    """
    Validate that the user is in the frame and grant access to the compartment
    If it's not the correct user, validate identity through fingerprint
    scanner, otherwise, deny access.
    """
    if match[0]:
        print("Access Granted. \nHello Alex!")
        GPIO.output(7, GPIO.HIGH)
    else:
        print("Access Denied.\nPlease Validate Fingerprint.")
        
        # Read the given fingerprint image and store it in the image buffer
        while (fingerScanner.readImage() == False):
            pass
        
        """
        Convert the image in the image buffer and store it in the specified
        char buffer
        """
        fingerScanner.convertImage(0x01)

        """
        Search the database for the characteristics in the image buffer and
        create a reference to the tuple being returned
        """
        result = fingerScanner.searchTemplate()

        """
        Get the value stored in the first index of the template search results
        which indicates in which position of the database the given image was
        found. -1,  if the fingerprint is not in the database.
        """
        positionNumber = result[0]

        """
        If invalid fingerprint given, Deny access and exit.
        Otherwise, grant access and activate solenoid to open
        secret compartment
        """
        if (positionNumber == -1):
            print('Access Denied.')
            exit(0)
        else:
            print("Access Granted. \nHello Alex!")
            GPIO.output(7, GPIO.HIGH)
    
    

#!/usr/bin/python3

# Import necessary modules
import face_recognition
import picamera
import numpy as np
#from .userSetup import getEncodings

# Create a reference to our camera
camera = picamera.PiCamera()
camera.resolution = (352, 240)
output = np.empty((240, 352, 3), dtype=np.uint8)  # Creates an array  of given dimensions

def main():
    # Load the picture of the user and learn to recognize it
    # You must use the absolute path or else the program can't find it.
    user_image = face_recognition.load_image_file("/home/pi/MagicMirror/modules/face-rec-module/python/images/lynn_yip.jpg")
    userFaceEncoding = face_recognition.face_encodings(user_image)[0]

    # Initialize 2 lists for storing face details and encodings
    face_locations = []
    face_encodings = []

    # Get a picture of the user currently in front of mirror
    camera.capture(output, format = "rgb")

    # Find the face and face encoding in the current frame
    face_locations = face_recognition.face_locations(output)

    # If you can't read the face, notify the user
    if len(face_locations) == 0:
        print("No Face Detected")
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Variable for unlocking solenoid
    checkLock = 0
    match = []
    
    # Check to see if the current person in the frame is the user
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([userFaceEncoding], face_encoding)
        name = ""

    """
    Validate that the user is in the frame and grand access to the compartment.
    If it's not the user, validate the identity through the fingerprint scanner,
    otherwise deny access.
    """
    if match:
        name = "Lynn"
        print("Access Granted. \nHello {}!".format(name))
        checkLock = 1
    else:
        print("Access Denied.\nPlease Validate Fingerprint.")
        
    camera.close()

if __name__ == '__main__':
    main()

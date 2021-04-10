import face_recognition

# Loads image as numpy array (turns image into a bunch of numbers)
yen1 = face_recognition.load_image_file("donnie_yen.jpg")

# Encodes face (learns how to recognize it - i have no idea how this works)
yen1_face_encoding = face_recognition.face_encodings(yen1)[0]

# Load more images for fun and encode them
yen2 = face_recognition.load_image_file("donnie_yen1.jpg")
yen2_face_encoding = face_recognition.face_encodings(yen2)[0]

obama1 = face_recognition.load_image_file("barack_obama.jpg")
obama1_face_encoding = face_recognition.face_encodings(obama1)[0]

obama2 = face_recognition.load_image_file("barack_obama1.jpg")
obama2_face_encoding = face_recognition.face_encodings(obama2)[0]

# List of known people's names - the people we want to identify
names = ["Donnie Yen", "Barack Obama"]

# List of face encodings
encodings = [yen1_face_encoding, yen2_face_encoding, obama1_face_encoding, obama2_face_encoding]

# Compare each encoding to the obama picture
for encoding in encodings:
    # compare_faces returns true or false
    match = face_recognition.compare_faces(encodings, obama1_face_encoding)

# Variable to hold match name
name = "Unknown"

# If a match was found in encodings list, get that index number (very janky, I know)
if True in match:
    # Return the index of the match that returned True
    first_match_index = match.index(True)

    # Retrieve the correct name since we have more encodings than names
    if first_match_index > 1:
        first_match_index = 1
    else:
        first_match_index = 0
    name = names[first_match_index]

    # Print result
    print("Match! " + name)

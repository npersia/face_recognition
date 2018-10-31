import face_recognition
import cv2
from PIL import Image
import os


class Face():

    contador = 0


    def __init__(self, frame, face_location):
        self.name = "Unknown-" + str(Face.contador)
        self.file = "faces/Unknown-" + str(Face.contador) + ".jpg"

        Face.contador += 1


        top, right, bottom, left = face_location
        face_image = frame[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(self.file, "JPEG")

        self.encoded = face_recognition.face_encodings(face_recognition.load_image_file(self.file))[0]





class Faces():
    def __init__(self):
        self.arr_faces = []

    def addFace(self, face):
        self.arr_faces.append(face)

    def getFaceName(self, name):
        for f in self.arr_faces:
            if f.name == name:
                return f
        return None

    def existFaceName(self,name):
        if self.getFaceName(name) != None:
            return True
        else:
            return False

    def saveFaces(self,frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_location in face_locations:
            self.addFace(Face(frame, face_location))


    def getFacesEncoding(self):
        enc = []
        for f in self.arr_faces:
            enc.append(f.encoded)





    def compareFaces(self,face_encoding):
        return face_recognition.compare_faces(self.getFacesEncoding(), face_encoding)




def save_faces(image,file_name):
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        #print(
        #    "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
        #                                                                                          right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(file_name + ".jpg", "JPEG")












# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


known_face_encodings = []
known_face_names = []


def load_faces():
    images = os.listdir("faces")
    for image in images:
        if (image not in known_face_names):



            b = face_recognition.load_image_file("faces/" + image)
            try:
                a = face_recognition.face_encodings(b)[0]

                known_face_encodings.append(a)
            except:
                pass
            known_face_names.append(image)
    return known_face_encodings,known_face_names










# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


#esto es lo que uso para evitar que encodee en cada vuelta del while
while_counter = 0

#esto es lo que va a setear el codigo de las personas que va leyendo
user_code = 0



faces = Faces()




while True:
    while_counter += 1
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if (process_this_frame) and (while_counter > 15):
        while_counter = 0






        face_locations = face_recognition.face_locations(rgb_small_frame)



        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            print(matches)


            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                print(first_match_index)
                name = known_face_names[first_match_index]


            if name == "Unknown":
                save_faces(rgb_small_frame, "faces/Unknown-" + str(user_code))
                user_code += 1
                known_face_encodings, known_face_names = load_faces()

            face_names.append(name)


    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
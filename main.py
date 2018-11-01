import face_recognition
import cv2
from PIL import Image
import os


class Face():

    contador = 0

    def __init__(self, face_encoding, face_location):
        self.name = "Unknown-" + str(Face.contador)
        self.file = "faces/Unknown-" + str(Face.contador) + ".jpg"

        Face.contador += 1
        self.face_location = face_location

        self.encoded = face_encoding
        self.on_screen = False

    def save_face(self, frame):
        top, right, bottom, left = self.face_location
        face_image = frame[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(self.file, "JPEG")



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

    def locateFaces(self, frame):
        self.frame = frame
        self.arr_face_locations = face_recognition.face_locations(frame)


    def encodeFaces(self):
        self.arr_encode_faces = face_recognition.face_encodings(self.frame, self.arr_face_locations)


    def saveFaces(self):

        for f in self.arr_faces:
            f.on_screen = False

        i = 0
        for face_encoding in self.arr_encode_faces:
            matches = face_recognition.compare_faces(self.getFacesEncoding(), face_encoding)

            #indices = [i for i, x in enumerate(my_list) if x == "whatever"]

            indices = [i for i, x in enumerate(matches) if x == True]

            for x in indices:
                self.arr_faces[x].on_screen = True

            if True not in matches:
                for face_location in self.arr_face_locations:
                    a_face = Face(face_encoding, face_location)
                    a_face.save_face(self.frame)
                    self.addFace(a_face)


            else:
                first_match_index = matches.index(True)
                loc_match_index = i

                a = self.arr_face_locations[loc_match_index]

                self.arr_faces[first_match_index].face_location = a
            i += 1



    def getFacesEncoding(self):
        """estos son los faces conocidos
        TODO cambiar nombre"""
        enc = []
        for f in self.arr_faces:
            enc.append(f.encoded)
        return enc



    def getFacesNames(self):
        """estos son los faces conocidos por nombre
        TODO cambiar nombre"""
        nom = []
        for f in self.arr_faces:
            nom.append(f.name)
        return nom


    def displayNames(self,frame):
        for face in self.arr_faces:
            if face.on_screen:
                top, right, bottom, left = face.face_location
                top *= 1
                right *= 1
                bottom *= 1
                left *= 1

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, face.name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def compareFaces(self,face_encoding):
        return face_recognition.compare_faces(self.getFacesEncoding(), face_encoding)

    def loadFaces(self, path):
        images = os.listdir(path)

        for image in images:

            b = face_recognition.load_image_file(path + "/" + image)
            face_encoding = face_recognition.face_encodings(b)[0]
            a_face = Face(face_encoding, None)
            self.addFace(a_face)


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# esto es lo que uso para evitar que encodee en cada vuelta del while
while_counter = 0


faces = Faces()
faces.loadFaces("faces")

while True:
    while_counter += 1
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if while_counter > 15:
        while_counter = 0

        faces.locateFaces(rgb_small_frame)
        faces.encodeFaces()
        faces.saveFaces()

    faces.displayNames(frame)
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

import face_recognition
import cv2
from PIL import Image
import os

import threading


class Face:

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


class Faces:
    def __init__(self):
        self.arr_faces = []
        self.frame = None
        self.arr_face_locations = []
        self.arr_encode_faces = []

    def add_face(self, face):
        self.arr_faces.append(face)

    def locate_faces(self, frame):
        self.frame = frame
        self.arr_face_locations = face_recognition.face_locations(self.frame)

    def encode_faces(self):
        self.arr_encode_faces = face_recognition.face_encodings(self.frame, self.arr_face_locations)

    def save_faces(self):

        for f in self.arr_faces:
            f.on_screen = False

        i = 0
        for face_encoding in self.arr_encode_faces:
            matches = face_recognition.compare_faces(self.get_faces_encoding(), face_encoding)

            indices = [i for i, x in enumerate(matches) if x == True]

            for x in indices:
                self.arr_faces[x].on_screen = True

            if True not in matches:
                for face_location in self.arr_face_locations:
                    a_face = Face(face_encoding, face_location)
                    a_face.save_face(self.frame)
                    self.add_face(a_face)
            else:
                first_match_index = matches.index(True)
                loc_match_index = i

                a = self.arr_face_locations[loc_match_index]

                self.arr_faces[first_match_index].face_location = a
            i += 1

    def get_faces_encoding(self):
        """estos son los faces conocidos
        TODO cambiar nombre"""
        enc = []
        for f in self.arr_faces:
            enc.append(f.encoded)
        return enc

    def display_names(self, frame):
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

    def load_faces(self, path):
        images = os.listdir(path)

        for image in images:

            b = face_recognition.load_image_file(path + "/" + image)
            face_encoding = face_recognition.face_encodings(b)[0]
            a_face = Face(face_encoding, None)
            self.add_face(a_face)


def process_video():
    faces = Faces()
    faces.load_faces("faces")

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # esto es lo que uso para evitar que encodee en cada vuelta del while
    while_counter = 0

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

            faces.locate_faces(rgb_small_frame)
            faces.encode_faces()
            faces.save_faces()

        faces.display_names(frame)
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()







process_video()
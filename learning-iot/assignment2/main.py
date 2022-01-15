import functools
import math
import sys
import serial

import numpy as np
import cv2 as cv
import face_recognition


INPUTS = [
    ("./reference/olgierd.jpg", "Olgierd"),
    # the label differ for diagnostic purposes
    # in reality they'd be the same to aid with accuracy of the recognition
    # and deduplicated from the final output
    ("./reference/olgierd2.jpg", "also Olgierd"),
]
EVERY_X_FRAME = 2
DOWNSCALE_RATIO = 2
AGREEMENT_PERCENT_THRESHOLD = 85
IMAGE = sys.argv[1] if len(sys.argv) > 1 else ""


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascPath)
video_capture = cv.VideoCapture(0)
known_data = [(face_recognition.face_encodings(face_recognition.load_image_file(i[0]))[0], i[1]) for i in INPUTS]
known_face_encodings, known_face_names = list(zip(*known_data))
escape_ascii = 27


def main():
    face_detected = False
    frame_counter = 0
    faces = []
    _faces = []

    try:
        ser = serial.Serial('/dev/ttyUSB0')
    except serial.serialutil.SerialException:
        print("Using mock serial implementation!")
        class MockSerial():
            def write(*args, **kwargs):
                print("Sending data via MockSerial!")

            def close(*args, **kwargs):
                pass
        ser = MockSerial()

    while True:
        if frame_counter >= 30000:
            frame_counter = 0

        if not IMAGE:
            _, frame = video_capture.read()
        else:
            frame = cv.imread(IMAGE)

        if frame_counter % EVERY_X_FRAME == 0:
            faces, _faces, _, names = process_frame(frame)

            # can't use idiom, because it's an np array
            if len(faces) > 0 and not face_detected:
                face_detected = True

                print(f"face[s] detected, known faces: {', '.join(names) or 'nope'}!")

                if names:
                    do_the_thing(ser)
            elif len(faces) <= 0 and face_detected:
                face_detected = False
                print("no face detected!")

        for face in faces:
            rect = box_to_rectangle(face) 
            x, y, xp, yp = rect
            cv.rectangle(frame, (x, y), (xp, yp), (0, 255, 0), 2)

        for face in _faces:
            rect = fr_to_full_size_rectangle(face)
            x, y, xp, yp = rect
            cv.rectangle(frame, (x, y), (xp, yp), (255, 0, 0), 2)

        cv.imshow("A", frame)

        if IMAGE:
            cv.imwrite("/tmp/ble.jpg", frame)
            break

        if any(cv.waitKey(1) & 0xFF == ord('q') for k in [ord("q"), escape_ascii]):
            ser.close()
            break


        frame_counter += 1


def process_frame(frame):
    # process in grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    if len(faces) > 0:
        small_frame = cv.resize(frame, (0, 0), fx=1 / DOWNSCALE_RATIO, fy=1 / DOWNSCALE_RATIO)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)

        faces_to_be_processed = []
        for face in faces:
            a = box_to_rectangle(face)
            for _face in face_locations:
                b = fr_to_full_size_rectangle(_face)

                try:
                    agreement_percent = rectangle_intersection_area(a,b) / min(rectangle_area(a), rectangle_area(b)) * 100
                except ZeroDivisionError:
                    continue

                if agreement_percent >= AGREEMENT_PERCENT_THRESHOLD:
                    faces_to_be_processed.append(_face)

        face_encodings = face_recognition.face_encodings(rgb_small_frame, faces_to_be_processed)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                face_names.append(known_face_names[best_match_index])

        assert len(face_names) == len(set(face_names)), "duplicated names in a match-set, something went terribly wrong!"

        return faces, face_locations, faces_to_be_processed, face_names

    return [], [], [], []


def box_to_rectangle(b):
    return (b[0], b[1], b[0] + b[2], b[1] + b[3])


def fr_to_full_size_rectangle(b):
    return (b[3] * DOWNSCALE_RATIO, b[0] * DOWNSCALE_RATIO, b[1] * DOWNSCALE_RATIO, b[2] * DOWNSCALE_RATIO)


def rectangle_area(a):
    return abs(a[0] - a[2]) * abs(a[1] - a[2])


# inspired by: https://stackoverflow.com/a/25068722
def rectangle_intersection_area(a, b):
    x1 = max(min(a[0], a[2]), min(b[0], b[2]))
    y1 = max(min(a[1], a[3]), min(b[1], b[3]))
    x2 = min(max(a[0], a[2]), max(b[0], b[2]))
    y2 = min(max(a[1], a[3]), max(b[1], b[3]))

    if x1 < x2 and y1 < y2:
        return rectangle_area((x1, y1, x2, y2))
    else:
        return 0


def do_the_thing(ser):
    ser.write(b'x')


if __name__ == "__main__":
    main()
    video_capture.release()
    cv.destroyAllWindows() 

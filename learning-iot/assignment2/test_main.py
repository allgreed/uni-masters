import pytest
import cv2 as cv
import face_recognition

from main import process_frame


@pytest.mark.parametrize("filename, final_faces_threshold, names", [
    ("./testset/olgierd_with_people.jpg", 2, ["Olgierd"]),
    ("./testset/olgierd_no_glasses_masked_hat.jpg", 1, ["Olgierd"]),
    ("./testset/easter_island.jpg", 0, []),
    ("./testset/kubecon.jpg", 10, []),
])
def test_detection(filename, final_faces_threshold, names):
    frame = cv.imread(filename)
    _, _, final_faces, names = process_frame(frame)

    assert(names) == names
    assert len(final_faces) >= final_faces_threshold

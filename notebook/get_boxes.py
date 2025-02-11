from ultralytics import YOLO
# from utils.codeCarboneWrapper import codecarbone_fr
import os
import cv2
import numpy as np


def inference_yolo_from_path(model, path):
    # Load image
    img = cv2.imread(path)

    return inference_yolo_from_image(model, img)

def inference_yolo_from_image(model, img):
    # Inference
    results = model(img)

    # Get boxes
    boxes = results[0].obb.xyxyxyxy.cpu().numpy()

    print(boxes)

    return boxes 


def show_boxes_on_images(image: np.ndarray, boxes):

    for box in boxes:
        p1,p2,p3,p4 = box

        x1, y1, x2, y2, x3, y3, x4, y4 = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1]
        x1, y1, x2, y2, x3, y3, x4, y4 = int(x1), int(y1), int(x2), int(y2), int(x3), int(y3), int(x4), int(y4)

        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.line(image, (x2, y2), (x3, y3), (0, 255, 0), 2)
        cv2.line(image, (x3, y3), (x4, y4), (0, 255, 0), 2)
        cv2.line(image, (x4, y4), (x1, y1), (0, 255, 0), 2)

        # cv2.putText(image, f'{int(class_id)}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return image


if __name__ == '__main__':
    # Load model
    model = YOLO("../runs/kaggle/runs/obb/yolo11m.pt/weights/best.pt")

    # Load image
    path = "../test_images/test_proche.jpg"
    img = cv2.imread(path)

    # Inference
    boxes = inference_yolo_from_image(model, img)

    if 0 == 1:
        boxes = [
                [[     1140.6,      751.09],
                 [       1162,       752.1],
                 [     1175.7,      464.39],
                 [     1154.3,      463.37]],

                [[     1115.1,      756.32],
                 [     1140.1,      757.66],
                 [     1156.9,      445.22],
                 [       1132,      443.88]],

                [[     85.344,      725.23],
                 [      108.6,      724.48],
                 [     99.673,      446.77],
                 [     76.415,      447.52]],

                [[     2.8571,      349.47],
                 [     27.479,      348.66],
                 [     16.564,        15.2],
                 [    -8.0577,      16.006]]
                ]

    # Show boxes
    img_with_boxes = show_boxes_on_images(img, boxes)

    # Display
    cv2.imshow("Image", img_with_boxes)
    cv2.imwrite("test.jpg", img_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

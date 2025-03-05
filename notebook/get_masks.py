import cv2
import numpy as np
from ultralytics import YOLO
import os

from get_boxes import get_boxes

def get_book_masks(img, boxes):
    book_masks = []

    ## coordinates of box are to be top left -> top right -> bottom right -> bottom left

    for box in boxes:
        # for each box, we compute its width and height
        # distance between (x1,y1) and (x2,y2)  = sqrt( (x1-x2)² + (y1-y2)² )
        p1, p2, p3, p4 = box[0], box[1], box[2], box[3]
        width = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        height = np.sqrt((p3[0]-p2[0])**2 + (p3[1]-p2[1])**2)

        if width > height:
            # if points order was not right
            width, height = height, width
            input_points = np.float32([p4, p1, p2, p3])
        else:
            input_points = np.float32([p1, p2, p3, p4])

        # points in the same order as in the box
        output_points = np.float32([[0, height],  [width, height], [width, 0], [0, 0]])

        # https://theailearner.com/tag/cv2-getperspectivetransform/
        matrix_transform = cv2.getPerspectiveTransform(input_points,output_points)
        # transorm original image to just the book mask with the matrix 
        mask = cv2.warpPerspective(img, matrix_transform, (int(width), int(height)))
        mask = cv2.rotate(mask, cv2.ROTATE_90_COUNTERCLOCKWISE) # to make the book horizontal

        book_masks.append(mask)

    return book_masks

def save_book_masks(book_masks, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, book in enumerate(book_masks):
        cv2.imwrite(os.path.join(output_folder, f"book_{i}.jpg"), book)


model = YOLO("runs/kaggle/runs/obb/yolo11m.pt/weights/best.pt")
path = "test_images/test_proche.jpg"
img = cv2.imread(path)
boxes = get_boxes(model, img)
book_masks = get_book_masks(img, boxes)

output_folder = "book_masks/"
save_book_masks(book_masks, output_folder)



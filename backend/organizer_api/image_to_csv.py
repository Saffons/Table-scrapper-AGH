import cv2
import numpy
import pytesseract
from pytesseract.pytesseract import Output
from cropped_image import cropped_image
from find_cells import find_cells
from find_cells import group_cells_into_rows
from sys import platform

if platform == "win32":
    pytesseract.pytesseract.tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def cells_to_csv(image, cells, cell_expansion=4, confidence=35):
    avg_width = sum(cell[2] for cell in cells) / len(cells)
    avg_height = sum(cell[3] for cell in cells) / len(cells)

    csv = ""
    rows = group_cells_into_rows(cells)
    for row in rows:
        for cell in row:
            x, y, w, h = cell + numpy.array([-cell_expansion, -cell_expansion, cell_expansion * 2, cell_expansion * 2])
            cell_image = image[y:y + h, x:x + w]

            if avg_width > w and avg_height > h:
                config = "--psm 7"
            else:
                config = "--psm 11"

            cell_text = ""
            tess = pytesseract.image_to_data(cell_image, config=config, output_type=Output.DICT)
            for j in range(len(tess['text'])):
                if float(tess['conf'][j]) > confidence:
                    cell_text += tess['text'][j] + " "
            csv += cell_text + "\t"
        csv += "\n"
    return csv


def image_to_csv(image):
    cropped = cropped_image(image)
    cells = find_cells(cropped)
    return cells_to_csv(cropped, cells)


def main():
    image = cv2.imread("../../db/test_image6.png")
    # image = cv2.imread("test_image7.jpg")

    csv = image_to_csv(image)
    print(csv)
    
    return 0

if __name__ == '__main__':
    main()

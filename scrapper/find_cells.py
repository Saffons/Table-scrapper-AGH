from cropped_image import cropped_image
import cv2
import numpy as np


def cleared_canny(canny):
    cleared = canny.copy()

    cleared[0, :] = 255
    cleared[-1, :] = 255
    cleared[:, 0] = 255
    cleared[:, -1] = 255

    contours, _ = cv2.findContours(cleared, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 800:
            bounding_rect = cv2.boundingRect(contour)
            if (bounding_rect[2] <= 20 and bounding_rect[3] <= 20) or 0.125 < bounding_rect[2] / bounding_rect[
                3] < 8:
                cv2.drawContours(cleared, [contour], -1, (0, 0, 0), thickness=-1)
    contours, _ = cv2.findContours(cleared, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        bounding_rect = cv2.boundingRect(contour)
        if bounding_rect[2] <= 20 and bounding_rect[3] <= 20:
            cv2.drawContours(cleared, [contour], -1, (0, 0, 0), thickness=-1)
    return cleared


def estimate_font_height(canny):
    canny_copy = canny.copy()

    horizontally_closed = cv2.morphologyEx(canny_copy, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (16, 1)))
    vertically_closed = cv2.morphologyEx(canny_copy, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20)))
    transformed_image = cv2.bitwise_and(horizontally_closed, vertically_closed)
    transformed_image = cv2.morphologyEx(transformed_image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))

    contours, _ = cv2.findContours(transformed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bounding_rects = [cv2.boundingRect(contour) for contour in contours]
    median_height = np.median(np.array([rect[3] for rect in bounding_rects]))
    return median_height - 2


def remove_holes(image, font_height):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < font_height ** 2 * 1.618 and cv2.boundingRect(contour)[3] < font_height:
            cv2.drawContours(image, [contour], -1, (255, 255, 255), thickness=-1)
    return image


def remove_cell_borders(image, canny):
    cleared = cleared_canny(canny)
    cleared = cv2.dilate(cleared, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    return cv2.bitwise_and(image, cv2.bitwise_not(cleared))


def image_canny(image):
    transformed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    transformed_image = cv2.GaussianBlur(transformed_image, (5, 5), 1)

    median_pixel = np.median(transformed_image)
    canny = cv2.Canny(transformed_image, max(0, 0.5 * median_pixel), min(255, 1.5 * median_pixel), apertureSize=3)
    return canny


def close_canny(canny, font_height):
    horizontally_closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (round(font_height), 1)))
    vertically_dilated = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, round(font_height * 1.5))))
    transformed_image = cv2.bitwise_and(horizontally_closed, vertically_dilated)
    transformed_image = cv2.morphologyEx(transformed_image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (round(font_height), round(font_height / 2))))
    return remove_holes(transformed_image, font_height)


def find_cells(image):
    canny = image_canny(image)
    font_height = max(estimate_font_height(canny), 14)
    closed = close_canny(canny, font_height)

    transformed_image = cv2.morphologyEx(closed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (round(font_height * 0.3), round(font_height * 0.6))))
    transformed_image = cv2.dilate(transformed_image, cv2.getStructuringElement(cv2.MORPH_RECT, (round(font_height * 1.2), round(font_height * 1.25))))
    transformed_image = remove_cell_borders(transformed_image, canny)
    transformed_image = cv2.morphologyEx(transformed_image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (round(font_height), round(font_height * 1.5))))

    cells = []
    contours, _ = cv2.findContours(transformed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    min_area = font_height ** 2 * 1.618
    for contour in contours:
        bounding_rect = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > min_area and bounding_rect[3] > 12 and bounding_rect[2] >= 8:
            cells.append(bounding_rect)

    return cells


def group_cells_into_rows(cells):
    def cells_in_same_row(base_cell, cells):
        top = base_cell[1]
        bottom = base_cell[1] + base_cell[3]
        return [cell for cell in cells if bottom >= cell[1] + 0.5 * cell[3] >= top]

    cells = sorted(cells, key=lambda x: x[3], reverse=True)

    rows = []
    while cells:
        row = cells_in_same_row(cells[0], cells)
        rows.append(row)
        cells = [cell for cell in cells if cell not in row]

    rows.sort(key=lambda x: x[0][1] + 0.5 * x[0][3])
    for row in rows:
        row.sort(key=lambda x: x[0])

    return rows


def main():
    # image = cv2.imread("test_image6.png")
    # image = cv2.imread("test_image7.jpg")
    image = cv2.imread("test_image8.png")
    # image = cv2.imread("test_image9.png")

    cropped = cropped_image(image)
    cv2.imshow("cropped image", cropped)

    cells = find_cells(cropped)
    rows = group_cells_into_rows(cells)

    cells_image = cropped.copy()
    for cell in cells:
        cv2.rectangle(cells_image, cell, (0, 255, 0), thickness=4)
    cv2.imshow("cells", cells_image)

    while True:
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

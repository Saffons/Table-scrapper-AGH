import cv2
import numpy as np


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def quad_contour(contour):
    def edge(a, b):
        return [[a[0], a[1]], [b[0], b[1]], distance(a, b)]

    def extrapolated_cross_point(edge_a, edge_b):
        def line_equation(edge):
            a = edge[1][1] - edge[0][1]
            b = edge[0][0] - edge[1][0]
            c = edge[0][1] * edge[1][0] - edge[0][0] * edge[1][1]
            return a, b, c

        a, b, c = line_equation(edge_a)
        dist = abs(a * edge_b[0][0] + b * edge_b[0][1] + c) / (a**2 + b**2)**0.5

        delta_x = edge_b[0][0] - edge_b[1][0]
        delta_y = edge_b[0][1] - edge_b[1][1]
        delta_length = (delta_x**2 + delta_y**2)**0.5
        cross_x = edge_b[0][0] + delta_x / delta_length * dist
        cross_y = edge_b[0][1] + delta_y / delta_length * dist
        return [round(cross_x), round(cross_y)]

    perimeter = cv2.arcLength(contour, True)
    simplified_contour = cv2.approxPolyDP(contour, 0.002 * perimeter, True)
    if simplified_contour.shape[0] == 4:
        return simplified_contour

    simplified_contour = np.reshape(simplified_contour, (simplified_contour.shape[0], 2))

    edges = []
    for i in range(-1, simplified_contour.shape[0] - 1):
        edges.append(edge(simplified_contour[i], simplified_contour[i + 1]))

    longest_edges = sorted(edges, key=lambda x: x[2], reverse=True)[:4]
    edges = [edge for edge in edges if edge in longest_edges]

    for i in range(-1, len(edges) - 1):
        edge_a = edges[i]
        edge_b = edges[i + 1]

        if edge_a[1] == edge_b[0]:
            continue

        cross_point = extrapolated_cross_point(edge_a, edge_b)
        edge_a[1] = cross_point
        edge_b[0] = cross_point

    quad = np.empty(len(edges) * 2, dtype=contour.dtype)
    for i in range(len(edges)):
        quad[2 * i] = edges[i][0][0]
        quad[2 * i + 1] = edges[i][0][1]
    return quad.reshape((len(edges), 1, 2))


def reordered_quad_contour_vertices(contour):
    def closes_vertex(target, vertices):
        min_distance = distance(target, vertices[0])
        closest = vertices[0]
        for vertex in vertices:
            dist = distance(target, vertex)
            if dist < min_distance:
                min_distance = dist
                closest = vertex
        return closest

    contour = contour.reshape(4, 2)

    x_max = np.amax(contour[:, 0])
    y_max = np.amax(contour[:, 1])

    up_left = closes_vertex(np.array([0, 0]), contour)
    up_right = closes_vertex(np.array([x_max, 0]), contour)
    down_left = closes_vertex(np.array([0, y_max]), contour)
    down_right = closes_vertex(np.array([x_max, y_max]), contour)

    return np.array([up_left, up_right, down_left, down_right]).reshape(4, 2)


def perspective_target_quad_vertices(quad_vertices):
    delta_x = max(quad_vertices[1][0] - quad_vertices[0][0], quad_vertices[3][0] - quad_vertices[2][0])
    horizontal_dist = max(distance(quad_vertices[1], quad_vertices[0]), distance(quad_vertices[3], quad_vertices[2]))
    width = round(horizontal_dist ** 2 / delta_x)

    delta_y = max(quad_vertices[2][1] - quad_vertices[0][1], quad_vertices[3][1] - quad_vertices[1][1])
    vertical_dist = max(distance(quad_vertices[2], quad_vertices[0]), distance(quad_vertices[3], quad_vertices[1]))
    height = round(vertical_dist ** 2 / delta_y)

    return np.array([[0, 0], [width, 0], [0, height], [width, height]])


def biggest_contour(contours):
    biggest = None
    biggest_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > biggest_area:
            biggest = contour
            biggest_area = area
    return biggest


def cropped_image(image):
    if image.shape[0] > image.shape[1]:
        new_height = 1000
        new_width = round(image.shape[1] / image.shape[0] * new_height)
    else:
        new_width = 1000
        new_height = round(image.shape[0] / image.shape[1] * new_width)
    transformed_image = cv2.resize(image, np.array([new_width, new_height]))
    transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
    transformed_image = cv2.GaussianBlur(transformed_image, (5, 5), 1)

    median_pixel = np.median(transformed_image)
    image_canny = cv2.Canny(transformed_image, max(0, 0.25 * median_pixel), min(255, 1.5 * median_pixel), apertureSize=3)

    contours, _ = cv2.findContours(image_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_height, image_width = image_canny.shape
    contours = [contour for contour in contours if cv2.contourArea(contour) >= 0.1 * image_width * image_height]

    biggest = biggest_contour(contours)
    if biggest is None or biggest.shape[0] < 4:
        return image

    perimeter = cv2.arcLength(biggest, True)
    simplified_contour = cv2.approxPolyDP(biggest, 0.002 * perimeter, True)
    quad = quad_contour(simplified_contour)

    quad_vertices = reordered_quad_contour_vertices(quad)
    quad_vertices[:, 0] = quad_vertices[:, 0] * (image.shape[1] / new_width)
    quad_vertices[:, 1] = quad_vertices[:, 1] * (image.shape[0] / new_height)
    target_quad_vertices = perspective_target_quad_vertices(quad_vertices)
    perspective_matrix = cv2.getPerspectiveTransform(quad_vertices.astype(np.float32), target_quad_vertices.astype(np.float32))
    image_width = target_quad_vertices[3, 0]
    image_height = target_quad_vertices[3, 1]
    return cv2.warpPerspective(image, perspective_matrix, (image_width, image_height))


def main():
    image = cv2.imread("test_image7.jpg")
    cv2.imshow("original image", image)
    cropped = cropped_image(image)

    cv2.imshow("cropped image", cropped)

    while True:
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

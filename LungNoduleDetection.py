import cv2 as cv
import numpy as np
import os

def image_to_array(imagen):
    if not os.path.exists(imagen):
        print(f"Error: El archivo '{imagen}' no se encuentra en la ruta especificada.")
        return None
    return cv.imread(imagen, cv.IMREAD_GRAYSCALE)

def threshold_without_bronchi(threshold, img):
    img = np.where((img > threshold) & (img < 200), 255, 0).astype(np.uint8)
    return img

def threshold_a_array(threshold, img):
    return np.where(img > threshold, 0, 1).astype(np.uint8)

def first_method_contour(img, threshold, img_name):
    if img is None:
        print("Error: Imagen no cargada correctamente en first_method_contour.")
        return

    eq_img = cv.equalizeHist(img)
    img_smooth = cv.GaussianBlur(eq_img, (7, 7), 0.3)
    cv.imshow(f"{img_name} - Imagen Suavizada", img_smooth)

    _, thresh = cv.threshold(img_smooth, threshold, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    img_copy_contours = np.copy(eq_img)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if 11000 < area < 35000:
            cv.drawContours(img_copy_contours, [cnt], -1, (0, 255, 0), 1)

    cv.imshow(f"{img_name} - Contornos Método 1", img_copy_contours)

def second_method_contour(img, threshold_bronchi, threshold_lung, img_name):
    if img is None:
        print("Error: Imagen no cargada correctamente en second_method_contour.")
        return

    eq_img = cv.equalizeHist(img)
    img_binary = threshold_a_array(threshold_bronchi, eq_img / 255)

    se_bronchi = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    bronchi_img = cv.erode(img_binary, se_bronchi)
    bronchi_img = cv.dilate(bronchi_img, cv.getStructuringElement(cv.MORPH_RECT, (8, 8)))

    contours, _ = cv.findContours((img_binary * 255).astype('uint8'), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    img_copy_contours = np.copy(eq_img)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if 300 < area < 400:
            cv.drawContours(img_copy_contours, [cnt], -1, (0, 255, 0), 1)

    se_opening1 = cv.getStructuringElement(cv.MORPH_RECT, (15, 15))
    se_opening2 = cv.getStructuringElement(cv.MORPH_RECT, (10, 10))
    se_opening3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (6, 6))
    img_smooth = cv.medianBlur(eq_img, 5)

    _, thresh = cv.threshold(img_smooth, threshold_lung, 255, cv.THRESH_BINARY)
    sum_thresh = ((bronchi_img * 255) + thresh).astype('uint8')

    opening = cv.erode(sum_thresh, se_opening1)
    opening = cv.dilate(opening, se_opening2)
    opening = cv.dilate(opening, se_opening1)
    opening = cv.erode(opening, se_opening3)

    contours, _ = cv.findContours(opening, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    img_copy_contours = np.copy(eq_img)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if 11000 < area < 35000:
            cv.drawContours(img_copy_contours, [cnt], -1, (0, 255, 0), 1)

    cv.imshow(f"{img_name} - Contornos Método 2", img_copy_contours)

# Directorio de imágenes
data_dir = 'data'
image_files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'))]

# Procesar cada imagen en el directorio
for image_file in image_files:
    img_path = os.path.join(data_dir, image_file)
    img = image_to_array(img_path)
    if img is not None:
        print(f"Procesando {image_file} con el primer método")
        first_method_contour(img, 146, image_file)
        print(f"Procesando {image_file} con el segundo método")
        second_method_contour(img, 0.365, 141, image_file)
        cv.waitKey(0) 
        cv.destroyAllWindows()

def process_img(image):
        import cv2
        import os
        img = cv2.imread(image)
        inverted_image = cv2.bitwise_not(img)
        cv2.imwrite("temp/inverted.jpg", inverted_image)
        def grayscale(image):
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = grayscale(img)
        cv2.imwrite("temp/gray.jpg", gray_image)
        thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
        cv2.imwrite("temp/bw_image.jpg", im_bw)
        def noise_removal(image):
            import numpy as np
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.erode(image, kernel, iterations=1)
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            image = cv2.medianBlur(image, 3)
            return (image)
        no_noise = noise_removal(im_bw)
        cv2.imwrite("temp/no_noise.jpg", no_noise)
        def thin_font(image):
            import numpy as np
            image = cv2.bitwise_not(image)
            kernel = np.ones((2,2),np.uint8)
            image = cv2.erode(image, kernel, iterations=1)
            image = cv2.bitwise_not(image)
            return (image)
        eroded_image = thin_font(no_noise)
        cv2.imwrite("temp/eroded_image.jpg", eroded_image)
        def thick_font(image):
            import numpy as np
            image = cv2.bitwise_not(image)
            kernel = np.ones((2,2),np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            image = cv2.bitwise_not(image)
            return (image)
        dilated_image = thick_font(no_noise)
        cv2.imwrite("temp/dilated_image.jpg", dilated_image)
        import numpy as np
        def remove_borders(image):
            contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
            cnt = cntsSorted[-1]
            x, y, w, h = cv2.boundingRect(cnt)
            crop = image[y:y+h, x:x+w]
            return (crop)
        no_borders = remove_borders(no_noise)
        cv2.imwrite("temp/no_borders.jpg", no_borders)
        color = [255, 255, 255]
        top, bottom, left, right = [150]*4
        image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        cv2.imwrite("temp/image_with_border.jpg", image_with_border)
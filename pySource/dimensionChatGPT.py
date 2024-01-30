import cv2
import

# Load the image
img = cv2.imread('boxM.jpeg')
# Define the dictionary and parameters for the marker detection
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
parameters = cv2.aruco.DetectorParameters_create()

# Detect the marker in the image and extract its corners
corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
# Define the length of the marker's side in millimeters
marker_length_mm = 50

# Define the camera matrix and distortion coefficients
camera_matrix = np.array([[focal_length, 0, center_x], [0, focal_length, center_y], [0, 0, 1]])
dist_coeffs = np.array([k1, k2, p1, p2, k3])

# Estimate the pose of the marker
rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length_mm, camera_matrix, dist_coeffs)
# Draw the axes of the estimated pose on the image
img_with_axes = cv2.aruco.drawAxis(img, camera_matrix, dist_coeffs, rvec, tvec, marker_length_mm)


# Draw the detected marker on the image
cv2.aruco.drawDetectedMarkers(img, corners, ids)
# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a threshold to the image to separate the object from the background
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find the contours of the object in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Select the largest contour as the object
object_contour = max(contours, key=cv2.contourArea)
# Draw the detected object on the image
cv2.drawContours(img, [object_contour], 0, (0, 255, 0), 2)
# Calculate the area of the object contour
object_area = cv2.contourArea(object_contour)

# Print the size of the object in pixels
print("Object size in pixels:", object_area)
# Calculate the size of the object in millimeters
object_size = object_area / 20

# Print the size of the object in millimeters
print("Object size in millimeters:", object_size)

# Display the resulting image
cv2.imshow('Pose estimation', img_with_axes)
cv2.waitKey(0)
cv2.destroyAllWindows()


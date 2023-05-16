# rain_visualisation_india

![map 1]("https://raw.githubusercontent.com/jashanpreet-singh-99/rain_visualisation_india/main/map_created/demo_1.png")

## indian_map_image_clor

This Python code provides functions for converting RGB values to hexadecimal format and generating a state map of India. The rgb2hex() function takes three integers representing the red, green, and blue color channels and returns the corresponding hexadecimal color code.

The create_map_india_with_state() function creates a map of India with state boundaries. It uses a default color list or accepts a custom color list as input. The function reads a base map image file, applies thresholding to remove noise, identifies the possible regions of interest (ROI) using contour detection, and selects the top 28 contours based on their area. It then fixes subdivisions for specific states and generates a new blank image. The required colors are filled in for each state using the selected contours and color list. The resulting map image is saved in the "map_created" folder.

The get_state_indexes() function returns a dictionary mapping state names to their corresponding contour indexes from the top list.

To use this code, ensure that the required dependencies (OpenCV and NumPy) are installed. You can call the create_map_india_with_state() function to generate the map and obtain the file path of the created image. The get_state_indexes() function provides the contour indexes for each state, which can be useful for further processing or analysis.

Note: It is recommended to review and modify the code as per specific project requirements or additional functionalities.

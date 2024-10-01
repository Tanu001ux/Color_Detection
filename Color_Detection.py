import cv2
import pandas as pd

# Reading the image
img = cv2.imread('image.jpg')  # replace 'image.jpg' with the path to your image

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Reading the CSV file with color names
# Download the CSV file from: https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to get the color name based on RGB values
def get_color_name(R, G, B):
    minimum = 10000
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to handle mouse events
def draw_function(event, x, y, flags, param):
    global clicked, r, g, b, xpos, ypos
    if event == cv2.EVENT_LBUTTONDBLCLK:  # Detect double-click
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]  # Extract the RGB values
        b = int(b)
        g = int(g)
        r = int(r)

# Create a window and bind the function to the window
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_function)

while True:
    cv2.imshow("Image", img)
    if clicked:
        # Draw rectangle and display color information
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Text to display color name and RGB values
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when 'q' is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

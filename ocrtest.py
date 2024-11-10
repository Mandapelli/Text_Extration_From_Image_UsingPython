from PIL import Image
import pytesseract
#import cv2
# Path to Tesseract executable (for Windows users)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\shaik\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load the image and preprocess
#img = cv2.imread('test_3.png')
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
#thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]  # Apply threshold

# Load an image file
image = Image.open(r'test_4.png')

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print("Extracted Text: ", text)
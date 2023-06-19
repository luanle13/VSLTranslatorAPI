# # from PIL import Image
# # import io
# import imutils

# # # Create a new image with the given size
# # width = 720
# # height = 1440
# # image = Image.new('RGB', (width, height))

# # # Create an in-memory buffer
# # buffer = io.BytesIO()

# # # Save the image to the buffer as JPEG
# # image.save(buffer, format='PNG')

# # # Get the buffer content as bytes
# # buffer_bytes = buffer.getvalue()

# # # Print the size of the buffer in bytes
# # print(len(buffer_bytes))

# import cv2

# # Open video capture
# cap = cv2.VideoCapture(0)


# # Read and display frames
# ret, frame = cap.read()
# frame = imutils.resize(frame, height=1440, width=720)
# print('Image shape:', frame.shape)
# print('Image data type:', frame.dtype)

# # Release video capture
# cap.release()
# cv2.destroyAllWindows()

from queue import Queue

qu = []
qu.clear()
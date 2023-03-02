import numpy as np
import cv2


df = cv2.imread('C:/Users/mayij/Desktop/coworkers-first-time-meeting.JPG')
# df = cv2.cvtColor(df, cv2.COLOR_BGR2RGB)


face_detect = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_profileface.xml')
# face_detect = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_alt.xml')
face_data = face_detect.detectMultiScale(df,scaleFactor=1.3,minNeighbors=3)


for (x, y, w, h) in face_data:
    print(x)
    cv2.rectangle(df, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi = df[y:y+h, x:x+w]
    # applying a gaussian blur over this new rectangle area
    roi = cv2.GaussianBlur(roi, (23, 23), 30)
    # impose this blurred image on original image to get final image
    df[y:y+roi.shape[0], x:x+roi.shape[1]] = roi



resized=cv2.resize(df,(800,600),interpolation=cv2.INTER_CUBIC)

cv2.imshow('test',resized)

cv2.waitKey(0)

# Destroy all windows
cv2.destroyAllWindows()




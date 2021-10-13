import cv2
import numpy as np
import face_recognition

image_lebron = face_recognition.load_image_file('lebron_train.png')
image_lebron = cv2.cvtColor(image_lebron, cv2.COLOR_BGR2RGB)

image_lebron_test = face_recognition.load_image_file('lebron_test.jpeg')
image_lebron_test = cv2.cvtColor(image_lebron_test, cv2.COLOR_BGR2RGB)

face_loc = face_recognition.face_locations(image_lebron)[0]
encode_lebron = face_recognition.face_encodings(image_lebron)[0]
cv2.rectangle(image_lebron, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (255, 0, 255), 2)

face_loc_test = face_recognition.face_locations(image_lebron_test)[0]
encode_lebron_test = face_recognition.face_encodings(image_lebron_test)[0]
cv2.rectangle(image_lebron_test, (face_loc_test[3], face_loc_test[0]), (face_loc_test[1], face_loc_test[2]),
              (255, 0, 255), 2)

# Will contain a bolean value if the faces match
result = face_recognition.compare_faces([encode_lebron], encode_lebron_test)

# Will tell us how different each of the two faces are. Lesser the better
result_distance = face_recognition.face_distance([encode_lebron], encode_lebron_test)

print(result)
print(result_distance)

# cv2.imshow('Lebron', image_lebron)

cv2.putText(image_lebron_test, '{}, {}'.format(result[0], round(result_distance[0], 1)),
            (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
cv2.imshow('Lebron Test', image_lebron_test)

cv2.waitKey(0)

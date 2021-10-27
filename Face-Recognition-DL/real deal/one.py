import cv2
import face_recognition
import os
from datetime import datetime


class DoorLock():
    def __init__(self):
        self.initialize_data_base()

    def initialize_data_base(self):
        path = 'superusers'
        self.images = []
        self.classNames = []

        my_list = os.listdir(path)

        for cl in my_list:
            currImage = cv2.imread("{}/{}".format(path, cl))
            self.images.append(currImage)
            self.classNames.append(os.path.splitext(cl)[0])

        self.encodeListknown = self.findencodings(self.images)
        print("Encoding Complete")
        self.run_cam()

    def findencodings(self, images):
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)

        return encodeList

    def markLogs(self, name):
        with open('logs.csv', 'r+') as f:
            myDatalist = f.readlines()

            name_list = []

            for line in myDatalist:
                entry = line.split(',')
                name_list.append(entry[0])

            if name not in name_list:
                print("Door open for {}.".format(name))

                now = datetime.now()
                dstring = now.strftime('%H:%M:%S')
                f.writelines('\n{}, {}'.format(name, dstring))

    def takepicture(self):
        admin_password = input("Enter admin Password: ")
        if admin_password != "0000":
            print("Failed- Wrong passowrd")

            try_again = input("Try again? (y/n): ")

            if try_again == "y":
                self.takepicture()
            else:
                return

        name = input("Enter your name ")

        cam = cv2.VideoCapture(0)

        while True:
            ret, frame = cam.read()

            if not ret:
                print("Failed to grab Frame")
                break

            cv2.imshow('Creating New Superuser', frame)
            k = cv2.waitKey(1)

            if k % 256 == 27:
                print("Closing")
                break

            # Press Space Bar to to take the picture
            elif k % 256 == 32:
                img_name = 'superusers/{}.jpg'.format(name)
                cv2.imwrite(img_name, frame)
                break

        cam.release()
        cv2.destroyAllWindows()

        self.initialize_data_base()

    def run_cam(self):
        print("Security cam Active")
        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurrFrame = face_recognition.face_locations(imgS)
            encodesCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)

            # print(facesCurrFrame)

            for faceEncode, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
                matches = face_recognition.compare_faces(self.encodeListknown, faceEncode)
                # faceDistance = face_recognition.face_distance(self.encodeListknown, faceEncode)
                # print(matches)
                for i in range(len(matches)):
                    if matches[i]:
                        name = self.classNames[i]
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        self.markLogs(name)

            cv2.imshow('Security cam', img)
            temp = cv2.waitKey(1)

            # Press Space Bar to add a user to the database
            if temp % 256 == 32:
                self.takepicture()


x = DoorLock()

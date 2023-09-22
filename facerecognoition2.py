import cv2
import os
import face_recognition


# Function to capture and save a user image
def capture_and_save_image(user_name):
    capture = cv2.VideoCapture(0)  # Open the default camera (usually the webcam)

    if not os.path.exists("user_images"):
        os.makedirs("user_images")

    while True:
        ret, frame = capture.read()  # Read a frame from the camera

        cv2.imshow("Capture Image", frame)

        key = cv2.waitKey(1)
        if key == ord("c"):  # Press 'c' to capture the image
            image_path = os.path.join("user_images", f"{user_name}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved as {user_name}.jpg")
            break
        elif key == 27:  # Press Esc to exit without saving
            cv2.destroyAllWindows()
            break
    capture.release()

# Function to verify a user's identity
def verify_user():
    capture = cv2.VideoCapture(0)  # Open the default camera (usually the webcam)

    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir("user_images"):
        if filename.endswith(".jpg"):
            name = os.path.splitext(filename)[0]
            image_path = os.path.join("user_images", filename)
            known_image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(known_image)

            if len(face_encodings) > 0.6:
                encoding = face_encodings[0]  # Take the first face encoding if found
                known_face_encodings.append(encoding)
                known_face_names.append(name)
            else:
                print(f"No face found in the image: {image_path}")

    while True:
        ret, frame = capture.read()  # Read a frame from the camera

        # Convert the frame from BGR to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imshow("Verify Image", frame)

        key = cv2.waitKey(1)
        if key == ord("v"):  # Press 'v' to verify the user
            user_face_encodings = face_recognition.face_encodings(rgb_frame)

            if len(user_face_encodings) > 0.6:
                user_face_encoding = user_face_encodings[0]  # Take the first face encoding if found
                matches = face_recognition.compare_faces(known_face_encodings, user_face_encoding)

                if True in matches:
                    matched_name = known_face_names[matches.index(True)]
                    print(f"Welcome, {matched_name}!")
                    cv2.imshow(f"{matched_name}.jpg",frame)
                else:
                    print("User not found in the database.")
            else:
                print("No face found in the captured image.")
            break
        elif key == 27:  # Press Esc to exit verification
            cv2.destroyAllWindows()
            break

    capture.release()



if __name__ == "__main__":
    while True:
        choice = input("Choose an option:\n1. Capture User Image\n2. Verify User\n3. Quit\n Enter any number 1,2,3: ")

        if choice == "1":
            user_name = input("Enter your name: ")
            capture_and_save_image(user_name)
        elif choice == "2":
            verify_user()

        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
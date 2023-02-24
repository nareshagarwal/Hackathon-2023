import dlib

model_path = "eye_prediction_model.dat"
test_data = r"C:\Users\msi\Downloads\Invincible - Hackathon 2023\ibug_300W_large_face_landmark_dataset\labels_ibug_300W_train_eye.xml"
#for test data labels_ibug_300W_test.xml and labels_ibug_300W_test_eye.xml
#for train data labels_ibug_300W_tr ain.xml and labels_ibug_300W_train_eye.xml

error = dlib.test_shape_predictor(test_data, model_path)

# test 8.177337578979452
# train 1.922246654681192
print(error)
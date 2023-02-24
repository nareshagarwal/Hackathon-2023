import dlib
import multiprocessing

training_data = r"C:\Users\msi\Downloads\Invincible - Hackathon 2023\ibug_300W_large_face_landmark_dataset\labels_ibug_300W_train_eye.xml"

output_model_path = "eye_prediction_model.dat"

options = dlib.shape_predictor_training_options()

options.tree_depth = 4
# depth of regression tree, bigger value = deep tree more accurate but takes more time
# smaller value = shallow tree faster less accurate

options.nu = 0.2
# regularization parameter generalize model range[0,1], values closer to 1 make model fit the data better

options.cascade_depth = 15
# thr number cascade needed, more number of cascade increases accuracy of model but also increases the size

options.feature_pool_size = 400
# number of pixels use
# pid to generate features for the random tree in each cascade
# more pixel = more accurate = slower
# less pixel = less accurate = faster

options.num_test_splits = 50
# determines the time taken to train
# more solpits = high accuracy = higher time

options.oversampling_amount = 5
# data augmentation applied to training set
# uses to increase size of dataset, here we are creating 5 images from each single image, apply 5 random deformations to each input image

options.oversampling_translation_jitter = 0.1
# controls the amount translation augmentation applied to the training data

options.be_verbose = True
# internal comments

options.num_threads = (multiprocessing.cpu_count() - 1)

print(options)

print("[INFO] training shape predictor...")
dlib.train_shape_predictor(training_data,output_model_path,options)
import re

eye_index = set(list(range(36, 48)))
part = re.compile("part name='[0-9]+'")

data_lines = open(r"C:\Users\msi\Downloads\Invincible - Hackathon 2023\ibug_300W_large_face_landmark_dataset\\labels_ibug_300W_train.xml").read().strip().split("\n")
#for test data labels_ibug_300W_test.xml and labels_ibug_300W_test_eye.xml
#for train data labels_ibug_300W_train.xml and labels_ibug_300W_train_eye.xml

output = open(r"C:\Users\msi\Downloads\Invincible - Hackathon 2023\ibug_300W_large_face_landmark_dataset\labels_ibug_300W_train_eye.xml", "w")

for line in data_lines:
    face_index = re.findall(part,line)

    if len(face_index) == 0:
        output.write(line+"\n")

    else:
        attr = "name='"
        i = line.find(attr)
        j = line.find("'", i + len(attr) + 1)
        index = int(line[i+len(attr):j])

        if index in eye_index:
            output.write(line+"\n")

output.close()



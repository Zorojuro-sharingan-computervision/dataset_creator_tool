import cv2
import os
from pathlib import Path
import random
import shutil


def support_video_to_frame(
    object_train_dir, object_test_dir, object_name, object_vid_path, no_of_images=0
):
    cap = cv2.VideoCapture(f"{object_vid_path}")
    while True:
        ret, frame = cap.read()
        if ret:
            file_name = os.path.join(
                object_train_dir, f"{object_name}_{no_of_images:08d}.jpg"
            )
            cv2.imwrite(str(file_name), frame)
            # copy=frame.copy()
            # cv2.putText(copy,f"Object name: {object_name}",(10,30),1,cv2.FONT_HERSHEY_SIMPLEX,(0,255,0),1)
            # cv2.putText(copy,f"No of frames captured: {no_of_images}",(10,60),1,cv2.FONT_HERSHEY_SIMPLEX,(0,255,0),1)
            # cv2.imshow(f"object_name",copy)
            print(f"Saved {file_name}")

            no_of_images += 1
        else:
            return no_of_images
            break

    return no_of_images


def data_maker(folder_path, train_dir, test_dir):
    no_of_objects = int(input("Number of Objects \n"))

    n_objects = no_of_objects
    objects = []
    object_no = 1
    object_images_no = []
    while n_objects != 0:
        object_name = input(f"Enter {object_no} object name: \n")
        no_of_videos = int(input(f"No. of videos for {object_name}: \n"))
        n_videos = no_of_videos
        object_train_dir = train_dir / object_name
        object_test_dir = test_dir / object_name
        os.mkdir(object_train_dir)
        os.mkdir(object_test_dir)
        videos_no = 1
        while n_videos != 0:
            object_vid_path = input(
                f"Enter {videos_no} video Path for {object_name} : \n"
            )
            objects.append((object_name, object_vid_path, object_train_dir))
            print(f"Objects array : {objects}")
            n_videos -= 1
            videos_no += 1

        n_objects -= 1
        object_no += 1

    no_of_images = 0
    current_name = None
    for object_data in objects:
        object_name, object_vid_path, object_train_dir = object_data
        if object_name != current_name:
            no_of_images = 0
            current_name = object_name
        no_of_images = int(
            support_video_to_frame(
                object_train_dir,
                object_test_dir,
                object_name,
                object_vid_path,
                no_of_images,
            )
        )
        object_images_no.append((object_name, no_of_images))

    object_transfer_test_dir_arr = []
    object_image_test_dir = {}

    for object_name, object_no in object_images_no:
        image_files = [
            file
            for file in os.listdir(train_dir / object_name)
            if file.endswith(".jpg")
        ]
        num_of_images_to_move = int(len(image_files) * (25 / 100))
        images_to_move = random.sample(image_files, num_of_images_to_move)

        for image_file in images_to_move:
            source_path = os.path.join(train_dir / object_name, image_file)
            destination_path = os.path.join(test_dir / object_name, image_file)
            shutil.move(source_path, destination_path)
        object_transfer_test_dir_arr.append((object_name, num_of_images_to_move))

    for object_info in object_transfer_test_dir_arr:
        object_name, num_of_images_to_move = object_info
        if object_name in object_image_test_dir:
            object_image_test_dir[object_name] += num_of_images_to_move
        else:
            object_image_test_dir[object_name] = num_of_images_to_move
    for object_name, total in object_image_test_dir.items():
        print(f"{total} Images tranferred to  {object_name} test dir ")

    object_image_totals = {}

    for object_name, no_of_images in object_images_no:
        if object_name in object_image_totals:
            object_image_totals[object_name] += no_of_images
        else:
            object_image_totals[object_name] = no_of_images
    for object_name, total in object_image_totals.items():
        print(f"Total Images of {object_name} : {total}")


folder_name = input("Enter Folder Name : \n")
folder_dir = os.mkdir(f"{folder_name}")
print("Folder Created")
folder_path = Path(folder_name)
train_dir = folder_path / "train"
test_dir = folder_path / "test"
print("train & test dir created")
train_dir.mkdir()
test_dir.mkdir()
data_maker(folder_path, train_dir, test_dir)


# Proggrammed by Samyak A. Nahar

# Libraries used:
#  cv2
#  os
#  pathlib
#  random
#  shutil

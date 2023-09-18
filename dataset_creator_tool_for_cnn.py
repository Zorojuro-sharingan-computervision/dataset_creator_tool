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

where=False
while where is False:
  cnn_yolo=input("Dataset of CNN or YOLO ? \n")
  if cnn_yolo.lower()=="cnn":
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
      where=True
  elif cnn_yolo.lower()=="yolo":
      def support_video_to_frame(
          folder_path, object_name, object_vid_path, start_image_number=0
      ):
          if not folder_path.exists():
              os.mkdir(folder_path)
              print("Folder Created \n")
          else:
              print("Folder Exists,adding to the folder \n")
              existing_images = [f.name for f in folder_path.glob(f"{object_name}_*.jpg")]
              if existing_images:
                  last_image_number = max(int(fname.split('_')[1].split('.')[0]) for fname in existing_images)
                  start_image_number = last_image_number + 1

          cap = cv2.VideoCapture(object_vid_path)
          no_of_images = start_image_number

          while True:
              ret, frame = cap.read()
              if ret:
                  file_name = os.path.join(
                      folder_path, f"{object_name}_{no_of_images:09d}.jpg"
                  )
                  cv2.imwrite(str(file_name), frame)
                  print(f"Saved {file_name} \n")
                  no_of_images += 1
              else:
                  return no_of_images

      folder_name = "Images"
      where=False
      while where is False:
        where_to_save=input("Do you want to save the Images in drive? Y/n \n")
        if where_to_save.lower()=="y":
            folder_path=Path("/content/drive/MyDrive/Images")
            where=True
        elif where_to_save.lower()=="n":
            folder_path=Path("Images")
            where=True
        else:
            print("Enter Y/n, Do you want to save the Images in drive? \n")
            


        object_name = input("Enter object name: ")


        no_of_videos=int(input(f"Enter no. of Videos for {object_name} \n"))
        no_of_vid=int(no_of_videos)
        vid_paths=[]
        i=1
        while no_of_vid!=0:
          object_vid_path = input(f"Enter {i} video Path for {object_name}: \n")
          vid_paths.append(object_vid_path)
          no_of_vid-=1
          i+=1
        i=0
        while no_of_videos!=0:
          object_vid_path=vid_paths[i]
          no_of_images = support_video_to_frame(folder_path, object_name, object_vid_path)
          print(f"Total images saved: {no_of_images}")
          no_of_videos-=1
          i+=1
      where=True
  else:
    print("Enter either yolo or cnn... \n")
# Proggrammed by Samyak A. Nahar

# Libraries used:
#  cv2
#  os
#  pathlib
#  random
#  shutil

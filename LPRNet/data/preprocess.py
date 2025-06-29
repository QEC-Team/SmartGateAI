

"""



"""

from imutils import paths
import numpy as np
import cv2
import os
import argparse
import random

alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z', 'O']
ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
       'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']


parser = argparse.ArgumentParser(description='crop the licence plate from original image')
parser.add_argument("-image", help='image path', default='//media/muhannad/wdd3/thamer/perfect/sdp4/SmartGateAI/License_Plate_Recognation_Dataset', type=str)
parser.add_argument("-dir_train", help='save directory', default='train', type=str)
parser.add_argument("-dir_val", help='save directory', default='validation', type=str)
args = parser.parse_args()

img_paths = []
img_paths += [el for el in paths.list_images(args.image)]
random.shuffle(img_paths)

save_dir_train = args.dir_train
save_dir_val = args.dir_val

print('image data processing is kicked off...')
print("%d images in total" % len(img_paths))

idx = 0
idx_train = 0
idx_val = 0
for i in range(len(img_paths)):
    filename = img_paths[i]
    
    basename = os.path.basename(filename)
    imgname, suffix = os.path.splitext(basename)
    imgname_split = imgname.split('-')
    rec_x1y1 = imgname_split[2].split('_')[0].split('&')
    rec_x2y2 = imgname_split[2].split('_')[1].split('&')  
    x1, y1, x2, y2 = int(rec_x1y1[0]), int(rec_x1y1[1]), int(rec_x2y2[0]), int(rec_x2y2[1])
    w = int(x2 - x1 + 1.0)
    h = int(y2 - y1 + 1.0)
    
    img = cv2.imread(filename)
    img_crop = np.zeros((h, w, 3))
    img_crop = img[y1:y2+1, x1:x2+1, :]
#    img_crop = cv2.resize(img_crop, (94, 24), interpolation=cv2.INTER_LINEAR)
    
    pre_label = imgname_split[4].split('_')
    lb = ""
    lb += provinces[int(pre_label[0])]
    lb += alphabets[int(pre_label[1])]
    for label in pre_label[2:]:
        lb += ads[int(label)]
        
    idx += 1 
    
    if idx % 100 == 0:
        print("%d images done" % idx)
    
    if idx % 4 == 0:
        save = save_dir_val+'/'+lb+suffix      
        cv2.imwrite(save, img_crop)
        idx_val += 1
    else:
        save = save_dir_train+'/'+lb+suffix      
        cv2.imwrite(save, img_crop)
        idx_train += 1
        
print('image data processing done, write %d training images, %d val images' % (idx_train, idx_val))

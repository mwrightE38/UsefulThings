import numpy as np
import os
import sys
import tensorflow as tf
import math
import camera
from collections import defaultdict
from io import StringIO
from PIL import Image
import cv2
from utils import label_map_util
import glob

global MODEL_NAME
global PATH_TO_CKPT
global PATH_TO_LABELS
global NUM_CLASSES
global detection_graph
MODEL_NAME = 'coco'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = MODEL_NAME + '/labelmap.pbtxt'
NUM_CLASSES = 3




#Use::Loads a frozen tensorflow graph into memory
def load_model():
	global detection_graph
	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')



#Required::image=image data that can be converted to a np array
#Use::runs inference on an image
#Returns::x coordinate of center of object detected
#Returns::y coordinate of center of object detected
def run_inference(image):
	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	category_index = label_map_util.create_category_index(categories)
	with detection_graph.as_default():
  		with tf.Session(graph=detection_graph) as sess:
      				image_np = np.asanyarray(image)
      				# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      				image_np_expanded = np.expand_dims(image_np, axis=0)
      				image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      				# Each box represents a part of the image where a particular object was detected.
      				boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      				# Each score represent how level of confidence for each of the objects.
      				# Score is shown on the result image, together with the class label.
      				scores = detection_graph.get_tensor_by_name('detection_scores:0')
      				classes = detection_graph.get_tensor_by_name('detection_classes:0')
      				num_detections = detection_graph.get_tensor_by_name('num_detections:0')
     				 # Actual detection.
      				(boxes, scores, classes, num_detections) = sess.run(
          			[boxes, scores, classes, num_detections],
          			feed_dict={image_tensor: image_np_expanded})
				print(boxes)
      				#y = (((boxes[0][1][2] * 480) - (boxes[0][1][0] * 480)) / 2) + (boxes[0][1][0] * 480)
      				#x = (((boxes[0][1][3] * 640) - (boxes[0][1][1] * 640)) / 2) + (boxes[0][1][1] * 640)
				#print(x)
				#print(y)
      				return boxes,scores,classes;

i = 0;
def drawbox(boxes,image,scores):
	global i;
	height,width,channel = image.shape
	print (width)
	print (height)
	n = 0;
	for val in scores[0]:
        if val == 77 or val == 3:
            cv2.rectangle(img,(int(boxes[0][n][1]*width),int(boxes[0][n][0]*height)),(int(boxes[0][n][3]*width),int(boxes[0][n][2]*height)),(0,255,0),3)
        n = n+1;

	i = i+1
	cv2.imwrite("labeled/labeled_" + str(i) + ".jpg" , img)




load_model()

print()

files = glob.glob('*.jpg')
n=215;
for file in files:
    image = "scene" + n.zfill(5) + ".jpg";
    n = n +1;
	img = cv2.imread(image,cv2.IMREAD_COLOR)
	box,scores classes = run_inference(img)
	drawbox(box,img,scores)


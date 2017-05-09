 #!/usr/bin/env python

"""
Run this file to perform stitching operation on videos.


"""


import cv2, os, argparse
import numpy as np 
import matplotlib.pyplot as plt
from stitcher_engine.panorama import Stitcher
import time


__author__ 	= 	"Tejas Bobhate"
__email__	=	"tejas25789@gmail.com"
__status__	=	"prototype" 




def extract_key_frames():
	"""
	This function extracts key frames from a video feed. 
	'batch_size' parameter decides how many consecutive frames are considered to determine key frame. 
	Extracted key frames are appended in a list
	Stitching Engine then stitches the key frames to form a singlr image. 

	Returns:
		key_frames 	(list)	:	list of key frames extracted from video
	"""
	vlc = 'vlcsnap-'
	count = 1
	file_dir = os.path.dirname(os.path.realpath(__file__))
	index=0
	index_diff=0
	diff = np.zeros((250,1))
	key_frames = []
	batch_size = 10


	#Read 'batch_size' number of frames from video 
	for i in range(batch_size,248,batch_size):

		gray = np.zeros((480,640,batch_size), np.uint8)
		index=0
		mean_img = np.zeros((480,640), np.float64)
		for j in range(i-9,i+1,1):
			img_path = os.path.join(file_dir ,'vlcsnaps')
			img_name = os.path.join(img_path ,vlc + str(j).zfill(5) + '.jpg')
			gray[:,:,index] = cv2.imread(img_name, 0)
			mean_img += gray[:,:,index]
			index+=1

		# compute mean image 
		mean_img = mean_img/float(batch_size)
		# plt.imshow(np.uint8(mean_img))
		# plt.show()

		# compute variance of frames
		diff2 = np.zeros((batch_size,1))
		for k in range(batch_size):
			diff2[k,0] = np.sum((gray[:,:,k] - mean_img)**2)
		diff2 = diff2/(640*480.0)


		diff[index_diff:index_diff+batch_size] = diff2
		index_diff+=batch_size

		# Select frame with minimum variance among batch of frames. Nrmally it is the middle frame
		# as it has more common region with all other images in the batch
		# Reject frames if all frames are same. That is indicatd by zero variance value.
		if np.all(diff2) == True:
			min_ = np.where(diff2 == np.min(diff2))[0][0]
			key_frames.append(cv2.imread( os.path.join(img_path, vlc + str(i-batch_size + min_+1).zfill(5) + '.jpg')))


	# To visualise varince valuse for each batch of frames uncomment following lines

	# plt.plot(diff)
	# xcorr = range(batch_size,250,batch_size)
	# plt.axvline(x=0, color = 'r', label = 'Upper and Lower bound for batch size')
	# for x in xcorr:
	# 	plt.axvline(x = x, color = 'r')
	# plt.title("We select a frame with least variance from a batch\n")
	# plt.xlabel('\nFrame Number')
	# plt.xticks(range(0,250, 10))
	# plt.ylabel('Variance of frame among a batch of frames')
	# plt.legend(loc = 'Best')
	# plt.show()

	return key_frames



if __name__ == '__main__':

	#Parse arguments to find out user's choice
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--choice", required=True, help="choice of detector and descriptor")
	args = vars(ap.parse_args())


	time1  =time.time()
	key_frames = extract_key_frames()
	key_frames.reverse()
	time2 = time.time()

	print 'Key frames have been extracted.'

	stitcher = Stitcher(choice = int(args["choice"]))
	file_dir = os.path.dirname(os.path.realpath(__file__))
	key_frames_path = os.path.join(file_dir, 'key-frames')

	# print key_frames_path
	result = key_frames[0]
	cv2.imwrite(os.path.join(key_frames_path,str(0) + '.jpg'), result)

	for i in range(1,len(key_frames)-1,1):
 
		imageB = key_frames[i]
		cv2.imwrite(os.path.join(key_frames_path, str(i) + '.jpg'), imageB)

		result= stitcher.stitch([result, imageB], showMatches=False)[:,:1000]
		

		sum_ = np.sum(result, axis = 0)
		id_ = np.where(sum_ == 0)[0][0]
		result = np.copy(result)[:,:id_-5, :]
		# plt.imshow(result)
		# plt.show()

	# print 'end'
	cv2.imwrite('note_' + cv2.__version__.split('.')[0] + '_'  +str(args["choice"])+'.jpg', result)
	time3 = time.time()

	print 'key frames extraction:', time2-time1, ' sec'
	print 'Stitching: ', time3 -time2, ' sec'





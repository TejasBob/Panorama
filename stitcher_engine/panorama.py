 #!/usr/bin/env python

"""
This is Stitcher class file"
"""


import numpy as np
import cv2
import matplotlib.pyplot as plt

__author__ 	= 	"Tejas Bobhate"
__email__	=	"tejas25789@gmail.com"
__status__	=	"prototype" 



class Stitcher:
	"""This is Stitcher class which encapsulates stitching engine in form of member functions.

	"""
	def __init__(self, choice = 1):

		""" This constructor determines OpenCV version being used and accordingly initialises 
			feature detector and descriptors. User defined input choice determines type of detecor and descriptor used for stitching two frames together.

			Args:
				self	(Stitcher)	:	Reference to the current Object
				choice	(int)		:	Choice of detector and descriptor

			"""

		# Determine OpenCV version
		ver = int(cv2.__version__.split('.')[0])
		if ver ==3:
			self.version3 = True
		else:
			self.version3 = False

		self.choice = choice



		# Initialize feature detectors and Descriptors based on choice parameter
		#Menu
		# Choice 	Feature detector 	Feature Descriptor 		Note
		#    1			SIFT 				SIFT 				-
		#    2 			SURF 				SURF 				Without Upright
		#	 3			SURF 				SURF 				With Upright
		# 	 4 			STAR 				BRIEF 				-
		# 	 5 			ORB 				ORB 				-


		if self.choice == 1:
			print 'Using SIFT...'
			if self.version3:		
				self.sift = cv2.xfeatures2d.SIFT_create()
			else:
				self.detector = cv2.FeatureDetector_create("SIFT")
				self.extractor = cv2.DescriptorExtractor_create("SIFT")

		if self.choice == 2:
			print 'Using SURF without Upright...'
			if self.version3:
				self.surf = cv2.xfeatures2d.SURF_create(400)
			else:
				self.detector = cv2.FeatureDetector_create("SURF")
				self.extractor = cv2.DescriptorExtractor_create("SURF")

		if self.choice == 3:
			print 'Using SURF with Upright...'
			if self.version3:
				self.surf = cv2.xfeatures2d.SURF_create(400)
				self.surf.setUpright(True)
			else:
				self.detector = cv2.SURF(hessianThreshold = 400, upright=1)
				self.extractor = cv2.DescriptorExtractor_create("SURF")

		if self.choice == 4:
			print 'Using STAR detector with BRIEF descriptor...'
			if self.version3:
				self.star = cv2.xfeatures2d.StarDetector_create()
				self.brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()

			else:
				self.detector = cv2.StarDetector()
				self.extractor = cv2.DescriptorExtractor_create("BRIEF")

		if self.choice == 5:
			print 'Using ORB...'
			if self.version3:
				self.orb = cv2.ORB_create()
			else:
				self.orb = cv2.ORB()

		return

	def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
		"""
		This function performs image stitching with help of other member functions of Stitcher class.

		Args:
			images			(list)	:	List of two images ordered left to right 
			ratio			(float)	:	Ratio for Lowe's Test
			reprojThresh	(float)	:	reprojThresh parameter for RANSAC for homography computation
			showMatches		(bool)	:	Flag for marking showing matches on input images
		"""
		(imageL, imageR) = images

		#Find key points and features for input images
		(kpsR, featuresR) = self.find_kp_features(imageR)
		(kpsL, featuresL) = self.find_kp_features(imageL)

		# Match features between two input images
		M = self.matchKeypoints(kpsR, kpsL,	featuresR, featuresL, ratio, reprojThresh)

		if M is None:
			return None

	
		(matches, H, status) = M
		#Perform perspective correction on second image (imageR)
		result = cv2.warpPerspective(imageR, H, (imageR.shape[1] + imageL.shape[1], imageR.shape[0]))

		#Insert Left image (imageL) in result to obtai stitched image
		result[0:imageL.shape[0], 0:imageL.shape[1]] = imageL

		if showMatches:
			vis = self.drawMatches(imageR, imageL, kpsR, kpsL, matches,
				status)

			return (result, vis)

		return result



	def find_kp_features(self,image):
		"""
		This function computes keypoints and features for the input image.

		The feature detector and descriptors are decided by user input choice. They are already initialised in constructor.

		Args:
			image 	(numpy.ndarray)	:	Input image in BGR colorspace
	
		Returns:
			Key points and features computed for input image
		"""

		if self.choice == 1:
			if self.version3:
				(kps, features) = self.sift.detectAndCompute(image, None)
			else:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				kps = self.detector.detect(image)
				(kps, features) = self.extractor.compute(image, kps)
			kps = np.float32([kp.pt for kp in kps])
			return kps,features

		if self.choice == 2 :
			if self.version3:
				kps, features = self.surf.detectAndCompute(image,None)
			else:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				kps = self.detector.detect(image)
				(kps, features) = self.extractor.compute(image, kps)
			kps = np.float32([kp.pt for kp in kps])
			return kps, features

		if self.choice == 3:
			if self.version3:
				kps, features = self.surf.detectAndCompute(image,None)
			else:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				kps = self.detector.detect(image)
				(kps, features) = self.extractor.compute(image, kps)
			kps = np.float32([kp.pt for kp in kps])
			return kps, features

		if self.choice == 4 : 
			if self.version3:
				kp = self.star.detect(image,None)
				kps, features = self.brief.compute(image, kp)
			else:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				kps = self.detector.detect(image)
				(kps, features) = self.extractor.compute(image, kps)
			kps = np.float32([kp.pt for kp in kps])
			return kps, features
		if self.choice == 5:
			if self.version3:
				kp = self.orb.detect(image, None)
				kps, features = self.orb.compute(image, kp)
			else:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				kp = self.orb.detect(image, None)
				kps, features = self.orb.compute(image, kp)
			kps = np.float32([kp.pt for kp in kps])
			return kps, features



	def matchKeypoints(self, kpsR, kpsL, featuresR, featuresL,ratio, reprojThresh):
		
		"""
		This function matches keypoints between to successive images and matched keypoints are used for computing Homography matrix 
		for perspective correction.

		Args:
			kpsR 		(numpy array)	:	Keypoints for right image
			kpsL 		(numpy array)	:	Keypoints for left image
			featuresR 	(numpy array)	:	features for right image
			featuresL	(numpy array)	:	features for left image
			ratio			(float)	:	Ratio for Lowe's Test
			reprojThresh	(float)	:	reprojThresh parameter for RANSAC for homography computation

		"""

		# compute the raw matches and initialize the list of actual matches
		matcher = cv2.DescriptorMatcher_create("BruteForce")
		rawMatches = matcher.knnMatch(featuresR, featuresL, 2)
		matches = []

		# loop over the raw matches
		for m in rawMatches:
		# Lowe's ratio test
			if len(m) == 2 and m[0].distance < m[1].distance * ratio:
				matches.append((m[0].trainIdx, m[0].queryIdx))

		# computing a homography if more than 4 matched points
		if len(matches) > 4:
			# construct the two sets of points

			ptsA = np.float32([kpsR[i] for (_, i) in matches])
			ptsB = np.float32([kpsL[i] for (i, _) in matches])

			# compute the homography between the two sets of points
			(H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

			return (matches, H, status)

		# otherwise, no homograpy could be computed
		return None

	def drawMatches(self, imageR, imageL, kpsR, kpsL, matches, status):
		"""
		This helper function helps with visualization of matched points for two successive images
		"""
		(hR, wR) = imageA.shape[:2]
		(hL, wL) = imageB.shape[:2]
		vis = np.zeros((max(hR, hL), wR + wL, 3), dtype="uint8")
		vis[0:hR, 0:wR] = imageA
		vis[0:hL, wR:] = imageB

		# loop over the matches
		for ((trainIdx, queryIdx), s) in zip(matches, status):
			# Only matched points are processed
			if s == 1:
				# draw the match
				ptA = (int(kpsR[queryIdx][0]), int(kpsR[queryIdx][1]))
				ptB = (int(kpsL[trainIdx][0]) + wA, int(kpsL[trainIdx][1]))
				cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

		return vis

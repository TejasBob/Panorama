To run the demo  enter:
$ python test.py --choice <1-5>

Result image will be saved in same directory as test.py with name "note_[opencv_version]_[choice].jpg". Also key frames used for stitching will be stored under "key-frames" directory. 
The choice parameter is for selecting particular pair of feature detector and descriptor.

Here's the table:
Choice 	Feature detector 	Feature Descriptor 		Note
    1			SIFT 				SIFT 				-
    2 			SURF 				SURF 				Without Upright
	3			SURF 				SURF 				With Upright
 	4 			STAR 				BRIEF 				-
 	5 			ORB 				ORB 				-
 	
 For e.g.
 To run demo with SIFT detector and descriptor use:
 $ python test.py --choice 1
 
 
 In order to run this demo your system must have following packages:
 OpenCV
 Numpy
 Matplotlib
 Argparse
 
 

# Panorama-AutomaticImageStitchingFromVideoFrames
To run the demo  enter:
    
    $ python test.py --choice <1-5>

Result image will be saved in result directory with name "note_[opencv_version]_[choice].jpg". Also key frames used for stitching will be stored under "key-frames" directory. 
The choice parameter is for selecting particular pair of feature detector and descriptor.

Here's the table:

    | Choice 	| Feature detector 	| Feature Descriptor 	| Note            	|
    |--------	|------------------	|--------------------	|-----------------	|
    | 1      	| SIFT             	| SIFT               	| -               	|
    | 2      	| SURF             	| SURF               	| without Upright 	|
    | 3      	| SURF             	| SURF               	| with Upright    	|
    | 4      	| STAR             	| BRIEF              	| -               	|
    | 5      	| ORB              	| ORB                	| -               	|
 	
For e.g.
To run demo with SIFT detector and descriptor use:
 
    $ python test.py --choice 1
 
In order to run this demo your system must have following packages:
    
    Python(2.7.13)
    OpenCV(3.1.0)
    Numpy(1.11.3)
    Matplotlib(2.0.0)
 
**Key Frames**
 
 <p>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/0.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/1.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/2.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/3.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/4.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/5.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/6.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/7.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/8.jpg" width="150"/>
  <img src="https://github.com/TejasBob/Panorama/blob/master/key-frames/9.jpg" width="150"/>
<br/><br/><br/>




**Stitching Results Based On User's Choice <1-5>** 

<p>
<img src="https://github.com/TejasBob/Panorama/blob/master/result/note_3_1.jpg" width="640"  />
</p>
<p>
<img src="https://github.com/TejasBob/Panorama/blob/master/result/note_3_2.jpg" width="640"  />
</p>
<p>
<img src="https://github.com/TejasBob/Panorama/blob/master/result/note_3_3.jpg" width="640"  />
</p>
<p>
<img src="https://github.com/TejasBob/Panorama/blob/master/result/note_3_4.jpg" width="640"  />
</p>
<p>
<img src="https://github.com/TejasBob/Panorama/blob/master/result/note_3_5.jpg" width="640"  />
</p>


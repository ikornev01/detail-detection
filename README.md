# detail-detection 
Practice RUB Jan-Apr 23


The project "detail-detection" cosnists of two parts:
1.  TensorFlow Lite model, which detects the detail with Pi Camera
2.  Python webserver, which gets a request to detect a detail and then shows the data of this detail


Running the detail detection:

The instruction for the installation of TensorFlow Lite is in folder "raspberry_pi"
I also recommend to use "requirements.txt" to avoid the versions' conflict.


Usage of this (my) setting-up:

To start server: 
```
python detail-detection/server/server.py
```
To start detection separately: 
```
source tflite/bin/activate
cd detail-detection/raspberry_pi/
```

To teach your own model: 

[Google Colab](https://colab.research.google.com/github/khanhlvg/tflite_raspberry_pi/blob/main/object_detection/Train_custom_model_tutorial.ipynb)

[TensorFlow Raspberry Pi](https://www.youtube.com/watch?v=-ZyFYniGUsw&t=67s)

[TensorFlow Lite object detection project](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)

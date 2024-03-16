# py_face_landmark_helper
A package to help you utilise landmarks in the face_landmark feature of google open source mediapipe.



## Installation

To install the mediapipe_helper library, you can use pip:

```bash
pip install mediapipe_helper
```

or

```bash
git clone https://github.com/LearningnRunning/py_face_landmark_helper

python setup.py install
```

```python
from mediapipe_helper import face_landmark_helper

# Create an instance of FaceMeshProcessor
face_mesh_processor = face_landmark_helper.FaceLandmarkProcessor()
img_path = ""

# Call the convert_landmark method to get the face landmarks
face_landmarks = face_mesh_processor.convert_landmark(img_path)

lmk_idx = 170
lmk_invert = face_mesh_processor.invert_landmark(lmk_idx)
# OUTPUT: 395

lmk_idx = [170, 171, 180, 190]
lmk_invert_list = face_mesh_processor.invert_landmark_list(lmk_idx)
# OUTPUT: [395, 396, 404, 414]

```


## License
mediapipe_helper is provided under the Apache License 2.0. 


"""Utility functions to display the pose detection results."""

import cv2
import numpy as np
from tflite_support.task import processor
import settings #global variables

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (50, 205, 50)  # rectangle color

def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """
  settings.init()
  
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 2)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)
    
    # Define global variables
    settings.name = category_name
    settings.precision = probability
    
    if settings.name == 'red_empty' or settings.name == 'white_empty' or settings.name == 'black_empty':
      settings.inner_part = 'false'
    else: settings.inner_part = 'true'
    
    if settings.name == 'red_empty' or settings.name == 'red_full':
      settings.color = 'red'
    if settings.name == 'white_empty' or settings.name == 'white_full':
      settings.color = 'white'
    if settings.name == 'black_empty' or settings.name == 'black_full':
      settings.color = 'black'
    
  return image

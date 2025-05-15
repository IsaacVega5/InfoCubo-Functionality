from read_roi import read_roi_zip
import numpy as np
import cv2
def read_roi(roi_path):
    """
    Read the roi file and return the coordinates.
    Arguments:
        roi_path: Path to the roi file.
    Returns:
        A dictionary with the coordinates of the roi.
    """
    rois_list = read_roi_zip(roi_path)
    order_roi_list = sorted(rois_list, key=lambda x: int(x.split("-")[2]))
    order_roi_list = {roi : rois_list[roi] for roi in order_roi_list}
    return order_roi_list

def get_roi_info(roi_list, image):
  """
  Get ROI information with optimized operations and negative values clipped to 0.
  
  Args:
    roi_list: Dictionary of ROIs with 'x' and 'y' coordinates
    image: 2D numpy array with image data
      
  Returns:
    Dictionary with statistics for each ROI (negative values converted to 0)
  """
  results = {}
  height, width = image.shape
  
  for roi_name, roi_data in roi_list.items():
    # Create polygon efficiently
    polygon = np.column_stack((roi_data['x'], roi_data['y'])).astype(np.int32)
    
    # Create mask
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 255)
    
    # Get masked values and process them
    masked_image = image[mask > 0]
    valid_values = masked_image[~np.isnan(masked_image)]
    
    # Convert negative values to 0
    valid_values = np.where(valid_values < 0, 0, valid_values)
    
    if valid_values.size > 0:
      results[roi_name] = {
        'mean': np.mean(valid_values),
        'min': max(np.min(valid_values), 0),  # Ensure min is not negative
        'max': np.max(valid_values),
        'std': np.std(valid_values),
        'area': valid_values.size,
      }
    else:
      results[roi_name] = {
        'mean': np.nan,
        'min': np.nan,
        'max': np.nan,
        'std': np.nan,
        'area': 0
      }
            
  return results
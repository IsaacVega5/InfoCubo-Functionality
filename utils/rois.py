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
    Get the information of the roi.
    """
    # Get the image size
    image_size = image.shape

    results = {}
    for roi in roi_list:
      polygon = [ [x, y] for x, y in zip(roi_list[roi]['x'], roi_list[roi]['y'])]
      polygon = np.array(polygon, dtype=np.int32)
      
      mask = np.zeros(image_size, dtype=np.uint8)
      cv2.fillPoly(mask, [polygon], 255)
      
      # Aplicar máscara y filtrar NaN en un solo paso
      value_list = image[(mask > 0) & (~np.isnan(mask))]
      
      results[roi] = {
        'mean': np.mean(value_list),
        'min': np.min(value_list),
        'max': np.max(value_list),
        'std': np.std(value_list),
        'area': len(value_list),
      }
    return results
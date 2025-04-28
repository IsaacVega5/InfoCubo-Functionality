import pandas as pd

index_table_path = "./data/indexTable.csv"
from data import wavelenghts as wl

def read_idex_list():
  index_file = pd.read_csv(index_table_path, sep=';')
  index_list = index_file.to_dict(orient='records')
  return index_list

def get_closest_wavelength(wavelength_to_find):
  """
  Get the closest wavelength to the given band from the list of wavelengths.
  """
  closest = {
    "sensor": None,
    "band": None,
    "wavelength": None,
    "diff": float("inf")
  }
  
  for band, wavelength in enumerate(wl.NANO):
    diff = abs(wavelength - wavelength_to_find)
    if diff < closest["diff"]:
      closest["sensor"] = "nano"
      closest["band"] = band
      closest["wavelength"] = wl.NANO[band]
      closest["diff"] = diff
  
  for band, wavelength in enumerate(wl.SWIR):
    diff = abs(wavelength - wavelength_to_find)
    if diff < closest["diff"]:
      closest["sensor"] = "swir"
      closest["band"] = band
      closest["wavelength"] = wl.SWIR[band]
      closest["diff"] = diff

  return closest
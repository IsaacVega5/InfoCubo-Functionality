from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
import tkinter as tk

import spectral.io.envi as envi
from data import wavelenghts as wl
import pandas as pd

from classes import State
from utils.text import separate_paragraph
import widgets as wdg

from utils.files import get_firmware, get_metadata
from utils.rois import get_roi_info, read_roi
from utils.thread import resource_controller

def export_waves(nano_data, swir_data, output_path, process_flag : State, console : wdg.Console, progress_bar: wdg.ProgressBar, max_workers=None):
  process_flag.set(True)
  progress_bar(0)
  
  imgs = {
    'nano' : envi.open(nano_data["img"]) if nano_data["img"] else None,
    'swir' : envi.open(swir_data["img"]) if swir_data["img"] else None
  }
  
  nano_firmware = get_firmware(get_metadata(nano_data["img"])) if nano_data["img"] else None
  swir_firmware = get_firmware(get_metadata(swir_data["img"])) if swir_data["img"] else None

  warnings = []
  if "nhs" not in str(nano_firmware).lower() and nano_firmware:
    warnings.append(
      "    - Firmware is not from a nhs sensor\n      may be not a Nano image"
    )
  if "hc" not in str(swir_firmware).lower() and swir_firmware:
    warnings.append(
      "    - Firmware is not from a hc sensor\n      may be not a Swir image"
    )
  
  # 1. Leer rois de nano y swir
  rois = {
    'nano' : read_roi(nano_data["roi"]) if nano_data["roi"] else [],
    'swir' : read_roi(swir_data["roi"]) if swir_data["roi"] else []
  }
  
  if len(rois['nano']) != len(rois['swir']):
    warnings.append(
      "    - The number of rois in the images is different"
    )
  
  # 2. Comparar rois para ver si coinciden
  if len(warnings) > 0:
    console.add_text("\n⚠️Warnings: ", "#f0ad4e")
    console.add_text("\n".join(warnings), "#f0ad4e")
  
  cont = 0
  
  total_waves = {}
  for i, wave in enumerate(wl.NANO): total_waves[i] = {'wave': wave, 'type': 'nano', 'band': i}
  for i, wave in enumerate(wl.SWIR): total_waves[i + len(wl.NANO)] = {'wave': wave, 'type': 'swir', 'band': i}
  
  console.add_text("\nReading waves...", "white")
  init = time.time()
  
  max_workers = min(len(total_waves) ,(os.cpu_count() or 1) * 2, 10) if max_workers is None else max_workers
  results = {}
  with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # futures = {executor.submit(get_wave_data_df, (imgs[total_waves[i]['type']], total_waves[i]['band'], rois[total_waves[i]['type']])) : i for i in range(len(total_waves))}
    futures = {}
    for i in range(len(total_waves)):
      if not imgs[total_waves[i]['type']]:
        console.add_text(f"\n⚠️Warning: \n    - Skipping {total_waves[i]['wave']} because {total_waves[i]['type']} is not in the images\n", "#f0ad4e")
        continue
      futures[executor.submit(get_wave_data_df, (imgs[total_waves[i]['type']], total_waves[i]['band'], rois[total_waves[i]['type']], total_waves[i]['wave']))] = i

    for future in as_completed(futures):
      if not resource_controller():
        executor._max_workers = max(1, executor._max_workers - 2)
      
      idx = futures[future]
      try:
        results[idx] = future.result()
        progress_bar(len(results.keys()) / len(total_waves), f"{round(len(results.keys()) / len(total_waves) * 100)}%")
      except Exception as e: 
        console.add_text(str(e), "#f0ad4e")
  results = [ results[i] for i in sorted(results.keys()) ]
  
  console.add_text("Saving...", "white")
  progress_bar(0, f"{round(0)}%")
  try:
    with pd.ExcelWriter(output_path, engine='xlsxwriter', mode='w') as writer:
      for i in range(len(results)):
        df = results[i]['df']
        df.to_excel(writer, sheet_name=f"{results[i]['wave']}", index=False)
        cont += 1
        progress_bar((cont + 1) / len(total_waves), f"{round((cont + 1) / len(total_waves) * 100)}%")
  except Exception as e: 
    text = str(e)
    text = separate_paragraph(text, 8, 20)
    console.add_text(text, "#FA5252")
    tk.messagebox.showerror("Error", text)
    return None
  
  end = time.time()
  console.add_text(f"Process finished in {end - init} seconds", "#5cb85c")
  process_flag.set(False)
  progress_bar(100, f"{round(100)}%")
  return output_path

def order_export(data):
  res = [ {
    'Parc.': index + 1, 
    'Name': current,
    'area' : data[current]['area'],
    'mean': data[current]['mean'],
    'min': data[current]['min'],
    'max': data[current]['max'],
    'std': data[current]['std']
    } for index, current in enumerate(data) ]
  
  return res

def get_wave_data_df(props : tuple):
  """
  props = (img, band, roi_set, type)
  """
  img, band, roi_set, wave = props
  band_img = img.read_band(band)
  roi_info = order_export(get_roi_info(roi_set, band_img))
  df = pd.DataFrame(roi_info)
  return {
    'band': band,
    'wave': wave,
    'df': df
  }
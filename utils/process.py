import ttkbootstrap as ttk
from tkinter.filedialog import askdirectory
import numpy as np
import spectral.io.envi as envi
from utils.files import formate_filename, get_firmware, get_metadata
from utils.formula import eval_formula, format_formula
from utils.index import get_closest_wavelength, read_idex_list
from utils.rois import get_roi_info, read_roi
import pandas as pd
import os

def calculate_index(nano_data, swir_data, console, progress_bar : ttk.Progressbar):
    progress_bar.step(0)
    progress_bar.update_idletasks()
    
    # Obtener la carpeta de destino para guardar los resultados
    folder = askdirectory(title="Select folder to save results")
    if folder == "":
        return
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    imgs = {
        'nano' : envi.open(nano_data["img"]),
        'swir' : envi.open(swir_data["img"])
    }
    
    nano_firmware = get_firmware(get_metadata(nano_data["img"]))
    swir_firmware = get_firmware(get_metadata(swir_data["img"]))

    warnings = []
    if "nhs" not in str(nano_firmware).lower() and nano_firmware:
        warnings.append(
            "    - Firmware is not from a nhs sensor\n      may be not a Nano image"
        )
    if "hc" not in str(swir_firmware).lower() and swir_firmware:
        warnings.append(
            "    - Firmware is not from a hc sensor\n      may be not a Swir image"
        )

        
    #* Pasos para calcular indices
    
    # 1. Leer rois de nano y swir
    rois = {
        'nano' : read_roi(nano_data["roi"]),
        'swir' : read_roi(swir_data["roi"])
    }
    
    if len(rois['nano']) != len(rois['swir']):
        warnings.append(
            "    - The number of rois in the images is different"
        )
    
    # 2. Comparar rois para ver si coinciden
    if len(warnings) > 0:
        console.add_text("\n⚠️Warnings: ", "#f0ad4e")
        console.add_text("\n".join(warnings), "#f0ad4e")
    
    # 3. Obtener la lista de los indices
    index_list = read_idex_list()
    
    # 4. Por cada indice obtener la formula para calcularlo y almacenar en un diccionario
    #    las bandas que se requieren para calcularlo
    
    for step, current_index in enumerate(index_list):
        
        formula = current_index['Formula']
        try:
            bands = current_index['Bands'].replace("[", "").replace("]", "").replace("R", "").split(",")
            bands = [int(band.strip()) for band in bands]
        except Exception as e:
            console.add_text("\n⚠️Error: ", "#d9534f")
            console.add_text(
                "Error parsing bands: {e}. Please check the format of the bands in the index list.",
                "#d9534f"
            )
            raise ValueError(
                f"Error parsing bands: {e}. Please check the format of the bands in the index list."
            )
        
        # 5. Por cada banda obtener el valor de la banda mas cercana en el otro sensor
        closest = { band : get_closest_wavelength(band) for band in bands }

        console.add_text("\n[i] Closest Wavelengths: ", "#4582ec")
        console.add_text("\n".join([f"{band}: {closest[band]['wavelength']}" for band in closest]), "#4582ec")
                
        # 6. Por cada banda hacer un diccionario con las parcelas de los rois y su respectivo
        #    valor promedio, mínimo y máximo de esa banda
        #    eg. {"parcela1": {"mean": 0.1, "min": 0.2, "max": 0.3}, "parcela2": {...}}
        
        band_roi_data = {}
        for band in closest:
            band_img = imgs[closest[band]["sensor"]].read_band(closest[band]["band"])

            roi_list = rois[closest[band]["sensor"]]
            rois_image_data = get_roi_info(roi_list, band_img)
            band_roi_data[band] = rois_image_data
            
        # 7. Almacenar los datos obtenidos en el paso anterior en cache para no volver a calcularlos
        #    en caso de que los vuelva a necesitar otra función
        
        # 8. Analizar la formula y hacer cambios necesarios de símbolos
        #    eg. ^ -> ** √ -> math.sqrt()
        formula = format_formula(formula)
        
        # 9. Hacer un eval() de la formula con los datos obtenidos en el paso 6 sobre la función ya
        #    modificada por cada parcela
        
        results = {}
        for index, roi in enumerate(rois["nano"]):
            bands_mean = { band : band_roi_data[band][roi]['mean'] for band in band_roi_data.keys() }
            bands_min = { band : band_roi_data[band][roi]['min'] for band in band_roi_data.keys() }
            bands_max = { band : band_roi_data[band][roi]['max'] for band in band_roi_data.keys() }
            bands_std = { band : band_roi_data[band][roi]['std'] for band in band_roi_data.keys() }
            bands_area = np.mean([roi_data['area'] for band_data in band_roi_data.values() for roi_data in band_data.values()])

            results[index] = {
                "Parc.": index,
                "Name": roi,
                "area" : bands_area, 
                "mean" : eval_formula(formula, bands_mean),
                "min" : eval_formula(formula, bands_min),
                "max" : eval_formula(formula, bands_max),
                "std" : eval_formula(formula, bands_std),
            } 
        
        # 10. Almacenar los resultados en un diccionario de indices
        #    eg. indices = {"index1": {"parcela1": 0.1, "parcela2": 0.2}, "index2": {...}}
        df = pd.DataFrame.from_dict(results, orient='index')
        
        # 11. Exportar el diccionario de indices en un archivo .xlsx y crear una hoja por cada indice
        file_name = formate_filename(current_index['Name'])
        df.to_excel(f"{folder}/{file_name}.xlsx", index=False)
        
        current_step = step / len(index_list) * 10
        progress_bar.step(current_step)
        progress_bar.update_idletasks()
    return folder + "/"
        
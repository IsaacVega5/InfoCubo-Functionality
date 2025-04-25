from utils.files import get_firmware, get_metadata


def calculate_index(nano_data, swir_data, console):
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

    if len(warnings) > 0:
        console.add_text("\nWarnings: ", "#f0ad4e")
        console.add_text("\n".join(warnings), "#f0ad4e")
        
    #* Pasos para calcular indices
    
    # 1. Leer rois de nano y swir
    
    # 2. Comparar rois para ver si coinciden
    
    # 3. Obtener la lista de los indices
    
    # 4. Por cada indice obtener la formula para calcularlo y almacenar en un diccionario
    #    las bandas que se requieren para calcularlo
    
    # 5. Dentro de ese mismo diccionario almacenar junto con el la banda la imagen de la banda
    #    eg. {"banda1": {"formula": "f1", "bands": ["banda1", "banda2"]}, "banda2": {...}}
    
    # 6. Por cada banda hacer un diccionario con las parcelas de los rois y su respectivo
    #    valor promedio, mínimo y máximo de esa banda
    #    eg. {"parcela1": {"mean": 0.1, "min": 0.2, "max": 0.3}, "parcela2": {...}}
    
    # 7. Almacenar los datos obtenidos en el paso anterior en cache para no volver a calcularlos
    #    en caso de que los vuelva a necesitar otra función
    
    # 8. Analizar la formula y hacer cambios necesarios de símbolos
    #    eg. ^ -> ** √ -> math.sqrt()
    
    # 9. Hacer un eval() de la formula con los datos obtenidos en el paso 6 sobre la función ya
    #    modificada por cada parcela
    
    # 10. Almacenar los resultados en un diccionario de indices
    #    eg. indices = {"index1": {"parcela1": 0.1, "parcela2": 0.2}, "index2": {...}}
    
    # 11. Exportar el diccionario de indices en un archivo .xlsx y crear una hoja por cada indice
    
    
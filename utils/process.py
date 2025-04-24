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

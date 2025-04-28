import re
import numexpr as ne
import re
import numpy as np

def format_formula(formula : str) -> str:
  """
  Format the formula to be used in the calculation of the index.
  
  Args:
      formula (str): The formula to be formatted.
      image_prefix (str): The prefix to be used for the images. Default is "img".
      
  Returns:
      str: The formatted formula.
  """
  formula = formula.replace("√", "sqrt")
  formula = formula.replace("^", "**")
  formula = formula.replace(" ", "").replace("x", "*")
  
  return formula

def eval_formula(formula_str, band_dict):
    # Reemplazar RXXX por variables y añadir soporte para sqrt
    formula_str = re.sub(r'R(\d+)', r'b\1', formula_str)
    formula_str = re.sub(r'\|([^|]+)\|', r'abs(\1)', formula_str)
    
    # Crear entorno con bandas + funciones matemáticas seguras
    variables = {f'b{k}': v for k, v in band_dict.items()}
    variables.update({
        'sqrt': np.sqrt, 
        'log': np.log,
        'abs': np.abs,
    })
    
    return ne.evaluate(formula_str, local_dict=variables)
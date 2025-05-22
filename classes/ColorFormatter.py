import logging
import os


class ColorFormatter(logging.Formatter):
  COLORS = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[31;1m' # Bright Red
  }
  RESET = '\033[0m'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Verificar si la consola soporta colores ANSI
    self.supports_color = self._console_supports_color()

  def _console_supports_color(self):
    """Verify if the console supports color output."""
    if os.name == 'nt':  # Windows
      try:
        import colorama
        colorama.init()
        return True
      except ImportError:
        return False
    return True  # Asumir soporte en otros sistemas

  def format(self, record):
    message = super().format(record)
    if self.supports_color:
      color = self.COLORS.get(record.levelname, '')
      return f"{color}{message}{self.RESET}" if color else message
    return message
import ctypes
import logging
import os
import sys
import tkinter as tk
import traceback
from datetime import datetime

from classes import ColorFormatter


# Configuración inicial de consola
def setup_console():
    """Configure the console for debug mode."""
    if os.name == 'nt' and '--debug' in sys.argv:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        
        # Si no hay consola, crear una
        if kernel32.GetConsoleWindow() == 0:
            kernel32.AllocConsole()
            sys.stdout = open('CONOUT$', 'w')
            sys.stderr = open('CONOUT$', 'w')
            
        # Traer consola al frente
        console_window = kernel32.GetConsoleWindow()
        if console_window:
            user32.ShowWindow(console_window, 1)
            user32.SetForegroundWindow(console_window)

# Configuración de logging
def setup_logging(debug_mode):
    logger = logging.getLogger()
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Configurar solo una vez
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    if debug_mode:
        # Configurar colorama si está disponible
        if os.name == 'nt':
            try:
                import colorama
                colorama.init()
            except ImportError:
                pass
            
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter('%(levelname)s - %(message)s'))
        logger.addHandler(console_handler)
        
        import builtins

        #original_print = builtins.print
        
        def debug_print(*args, **kwargs):
            sep = kwargs.get('sep', ' ')
            msg = sep.join(str(arg) for arg in args)
            logger.info(msg)
            if kwargs.get('end', '\n') != '\n':
                sys.stdout.write(kwargs['end'])
                sys.stdout.flush()
        
        builtins.print = debug_print
        
        # Mensaje inicial único
        logger.info("\n=== MODO DEBUG ACTIVATED ===")
        logger.info("Every message will appear here")
        logger.info("The console will remain active until you close the application\n")
    
    return logger

# Manejo de excepciones
def handle_exception(exc_type, exc_value, exc_traceback):
    logging.critical("Exception not handled", exc_info=(exc_type, exc_value, exc_traceback))
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    tk.messagebox.showerror("Critical error", f"Error:\n\n{error_msg}")
    os._exit(1)

# Función para mantener la consola activa
def keep_console_alive():
    """Keeps the console window open"""
    root = tk._default_root
    if root:
        root.wait_window()
        os._exit(0)
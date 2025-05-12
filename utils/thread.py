import psutil
def resource_controller(max_cpu_percent=80, max_ram_percent=80):
  """
  Verify the CPU and RAM usage and kill the process if it exceeds the limits
  """
  cpu_ok = psutil.cpu_percent() < max_cpu_percent
  ram_ok = psutil.virtual_memory().percent < max_ram_percent
  return cpu_ok and ram_ok
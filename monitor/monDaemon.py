import time
import psutil

VIRTINE_PROC_IDENTIFIER = "virtine"
LOG_DELIMITER = " | "

class VirtMonitor:
  def __init__(self, _activate_logger, _interval, _log_file):
    self.activate_logger = _activate_logger
    self.interval = _interval
    self.log_file = _log_file
    self.pong = "pong"

  def get_virt_processes(self):
    virt_running_dir = {}
    for proc in psutil.process_iter():
      if proc.name().find(VIRTINE_PROC_IDENTIFIER) == -1:
        continue

      virt_running_dir[proc.pid] = { "name": proc.name(), \
      "pid": proc.pid, "cpu_times": proc.cpu_times(), "cpu_percent": proc.cpu_percent(), \
      "status": proc.status(), "memory_info": memory_info() }

    return virt_running_dir

  def dump_to_logfile(self, vrd):
    f = open(self.log_file, "a")
    for pid in vrd:
      f.write(str(pid) + LOG_DELIMITER + vrd[pid]["name"])
    f.close()

  def start_monitor(self):
    print("Starting monitor daemon")
    if not self.activate_logger:
      return

    while True:
      print("monitor")
      virt_running_dir = self.get_virt_processes()
      self.dump_to_logfile(virt_running_dir)
      time.sleep(self.interval)

  def num_instances(self):
    virt_running_dir = self.get_virt_processes()
    return len(virt_running_dir)

  def all_virt_stat(self):
    virt_running_dir = self.get_virt_processes()
    return virt_running_dir

  def stat_pid(self, pid):
    pid = int(pid);
    virt_running_dir = self.get_virt_processes()
    if pid not in virt_running_dir:
      return {}

    return virt_running_dir[pid]

  def get_pong(self):
    return self.pong

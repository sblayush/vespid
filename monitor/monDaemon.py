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

      virt_running_dir[proc.pid] = { "ts": str(round(time.time() * 1000)), "name": proc.name(), \
      "pid": str(proc.pid), "cpu_times": str(proc.cpu_times()), "cpu_percent": str(proc.cpu_percent()), \
      "status": proc.status(), "memory_info": str(proc.memory_info()) }

    return virt_running_dir

  def dump_to_logfile(self, vrd):
    f = open(self.log_file, "a")

    f.write("pid" + LOG_DELIMITER + "name" + LOG_DELIMITER + "ts" \
      + LOG_DELIMITER + "cpu_times" + LOG_DELIMITER + "cpu_percent" \
      + LOG_DELIMITER + "status" + LOG_DELIMITER + "memory_info" + "\n")

    for pid in vrd:
      f.write(vrd[pid]["pid"] + LOG_DELIMITER + vrd[pid]["name"] + LOG_DELIMITER + vrd[pid]["ts"] \
      + LOG_DELIMITER + vrd[pid]["cpu_times"] + LOG_DELIMITER + vrd[pid]["cpu_percent"] \
      + LOG_DELIMITER + vrd[pid]["status"] + LOG_DELIMITER + vrd[pid]["memory_info"] + "\n")
    f.close()

  def start_monitor(self):
    print("Starting monitor daemon")
    if not self.activate_logger:
      return

    while True:
      virt_running_dir = self.get_virt_processes()

      if len(virt_running_dir):
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

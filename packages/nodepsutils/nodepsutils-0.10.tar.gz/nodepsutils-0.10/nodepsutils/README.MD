# Some utilities made with the standard library - Windows only

## Tested against Windows / Python 3.11 / Anaconda


```py
from nodepsutils import (
    get_tmpfile_with_remove,
    prettify_csv,
    startfile_wait,
    get_dev_dict,
    get_ip_of_this_pc,
    get_short_path_name,
    get_short_path_name_cached,
    send_ctrlc_to_process,
    get_information_from_all_procs_with_connections_and_open_files,
    get_pids_with_open_file,
    get_information_from_all_procs_with_connections,
    get_information_from_all_procs,
    get_tmpfile,
    kill_process,
    kill_processes_with_executable,
    set_read_write,
    set_read_only,
    start_detached_process,
    get_free_port,
    disable_internet_for_app,
    enable_internet_for_app,
    touch,
)

tmpfile1,removefunction=get_tmpfile_with_remove(suffix=".csv")
print(tmpfile1)
print(removefunction)
tmpfile2=get_tmpfile()
print(tmpfile2)
prettyfile = prettify_csv(r"C:\Users\hansc\Downloads\titanic2.csv")
print(prettyfile)
startfile_wait(r"C:\Users\hansc\Downloads\titanic2.csv")

# network devices
devi=get_dev_dict()
print(devi)
# ips 
myip=get_ip_of_this_pc()
myipwithproxy = get_ip_of_this_pc(
    proxy={
        "https": f"socks5://{myip}:50688",
        "http": f"socks5://{myip}:50688",
    }
)
print(myip)
print(myipwithproxy)

# get short path
shortpath=get_short_path_name(
    long_name=r"C:\Users\hansc\Downloads\_1a063db4-b3b7-4bb2-84f5-cc6c9a21b9a8.jfif"
)
print(shortpath)
shortpathcached = get_short_path_name_cached(
    long_name=r"C:\Users\hansc\Downloads\_1a063db4-b3b7-4bb2-84f5-cc6c9a21b9a8.jfif"
)
print(shortpathcached)

# ctrl+c
send_ctrlc_to_process(pid=5342)

# process information
p1=get_information_from_all_procs()
p2=get_information_from_all_procs_with_connections()
p3=get_information_from_all_procs_with_connections_and_open_files()
p4 = get_pids_with_open_file(file=r"C:\Users\hansc\Downloads\todasasmusicax.xlsx")
# killing a process, first gracefully, than forcefully
for v in p4:
    kill_process(pid=(v["ProcessId"]), sleep_between_exitcommands=1)
# killing a process, first gracefully, than forcefully
kill_processes_with_executable(
    path=r"C:\WINDOWS\system32\notepad.exe", sleep_between_exitcommands=1
)   


# change rights of file 
path = r"C:\Users\hansc\Downloads\titanic2.csv"
set_read_write(path)
set_read_only(path)

# start completely detached process (won't close when python closes)
processdata=start_detached_process(
    command=[r"C:\Program Files\BlueStacks_nxt\HD-Player.exe", "--instance", "Rvc64_7"],
    working_dir=r"C:\ProgramData\BlueStacks_nxt\Engine\Rvc64_7",
    convert_exe_to_83=True,
    convert_all_to_83=False,
    accept_already_running=True,
    use_cached_shortpath=True,
    timeout_get_new_process_data=5,
    get_proc_information=True,
)
print(processdata)
# free port with certain length
get_free_port(minlen=5)
# disable internet 
disable_internet_for_app(exefile=r"C:\Program Files\BlueStacks_nxt\HD-Player.exe")
enable_internet_for_app(exefile=r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",disable_firewall=False)
#create a file
touch('c:\\some\\not\\existing\\file.txt')

```
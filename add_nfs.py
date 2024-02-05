import os
import subprocess
import asyncio


IP_LIST = {

"192.168.1.1":    "VM-1", 
"192.168.1.2":    "VM-2", 
}

DISK="/mnt/my-nfs"

# NFS Mount Point
NFS_POINT = f"192.168.1.3:{DISK}         {DISK}          nfs auto  0 0"

async def run_cmd(ip, vm_name):
    try:
        print("Executing commands for", ip, vm_name)
        #await asyncio.create_subprocess_shell(f"ssh ubuntu@{ip} 'sudo bash -c \"echo {NFS_POINT} >> /etc/fstab\"'")
        #await asyncio.create_subprocess_shell(f"ssh ubuntu@{ip} 'sudo mkdir -pv {DISK}'")
        #await asyncio.create_subprocess_shell(f"ssh ubuntu@{ip} 'sudo mount {DISK}'")
        print("Executing commands for", ip, vm_name, "DONE!")
    except asyncio.subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        raise Exception(f"{str(e)}")
    except Exception as e:
        print(e, ip)
        raise Exception(f"{str(e)}")

async def async_main(IP_LIST: dict):
    tasks = [run_cmd(ip, vm_name) for ip, vm_name in IP_LIST.items()]
    await asyncio.gather(*tasks)
    
def sync_main(IP_LIST: dict):
    for ip, vm_name in IP_LIST.items():
        try:
            print("Executing commands for", ip, vm_name)
            #subprocess.run(f"ssh ubuntu@{ip} 'sudo bash -c \"echo {NFS_POINT} >> /etc/fstab\"'", shell=True, check=True)
            #subprocess.run(f"ssh ubuntu@{ip} 'sudo mkdir -pv ${DISK}'", shell=True, check=True)
            subprocess.run(f"ssh ubuntu@{ip} 'sudo mount {DISK}'", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"{ip}, {vm_name}")
            raise e
        except Exception as e:
            print(e, ip, vm_name)

if __name__ == "__main__":

    run_async = False

    if run_async:
        asyncio.run(async_main(IP_LIST))
    else:
        sync_main(IP_LIST)
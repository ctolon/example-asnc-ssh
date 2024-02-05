import asyncio
import subprocess
import os

IP_LIST = {

"192.168.1.1":    "VM-1", 
"192.168.1.2":    "VM-2", 
}

ssh_keys=[
    # Add ssh keys here
    "ssh-rsa ...",
]

async def run_cmd(ip, vm_name):
    counter = 0
    for ssh in ssh_keys:
        try:
            counter = counter + 1
            print("Executing commands for", ip)
            result = await asyncio.create_subprocess_shell(
                cmd=f"ssh ubuntu@{ip} 'bash -c \"echo {ssh} >> /home/ubuntu/.ssh/authorized_keys\"'",
                shell=True,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE     
                )
            stdout, stderr = await result.communicate()
            if result.returncode == 0:
                print(f"{ip} - {vm_name} -> ssh key added: {ssh} \n")
                with open("success_commands.txt", "a") as success_file:
                    success_file.write(f"{ip} - {vm_name} -> ssh key added: {ssh} \n")
            else:
                print(f"Error executing command for {ip} - {vm_name}:")
                print("STDOUT:")
                print(stdout.decode())
                print("STDERR:")
                print(stderr.decode())
                with open("error_commands.txt", "a") as error_file:
                    error_file.write(f"Error for {ip} - {vm_name}\n")
        except Exception as e:
            print(f"Exception for {ip} - {vm_name}: {e}")

async def async_main(IP_LIST: dict):
    
    for filename in ["success_commands.txt", "error_commands.txt", "exceptions.txt"]:
        if os.path.exists(filename):
            os.remove(filename)
    
    tasks = [run_cmd(ip, vm_name) for ip, vm_name in IP_LIST.items()]
    await asyncio.gather(*tasks)
    
def sync_main(IP_LIST: dict):
    for ip, vm_name in IP_LIST.items():
        for ssh in ssh_keys:
            try:
                print("Executing commands for", ip, vm_name)
                subprocess.run(f"ssh ubuntu@{ip} 'bash -c \"echo {ssh} >> /home/ubuntu/.ssh/authorized_keys\"'", shell=True, check=True) 
                print(f"{ip} - {vm_name} -> ssh key added: {ssh} \n")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(f"{ip} - {vm_name}")
                raise e
            except Exception as e:
                print(e, ip, vm_name)

if __name__ == "__main__":

    run_async = True

    if run_async:
        asyncio.run(async_main(IP_LIST))
    else:
        sync_main(IP_LIST)
    
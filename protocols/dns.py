import subprocess
from protocols.protocol import Protocol
from lib.colors import debug, info, warn, error, fail, e, Style, Fore

class DNS_enum(Protocol):
    def __init__(self, host, port, service, basedir, verbose):
        super().__init__(host, port, service, basedir, verbose)

        nmblookup_command = f"nmblookup -A {host} | grep '<00>' | grep -v '<GROUP>' | cut -d' ' -f1"
        info_message = 'Running task {bgreen}nmblookup-{port}{rst}'
        info(info_message + (' with {bblue}{nmblookup_command}{rst}' if verbose >= 1 else '...'))

        try:
            hostname = subprocess.check_output(nmblookup_command, shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if hostname:
                self.run_cmds([
                    (
                        e(f'dig -p{port} @{hostname} axfr > "{basedir}/{port}_dns_dig.txt"'),
                        e(f'dig-{port}')
                    )
                ])
        except subprocess.CalledProcessError:
            pass  

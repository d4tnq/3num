import subprocess
from protocols.protocol import Protocol
from lib.colors import debug, info, warn, error, fail, e, Style, Fore
	#
	#  DNS
	#

class DNS_enum (Protocol):
    def __init__(self, host, port, service, basedir,verbose):
        Protocol.__init__(self, host, port, service, basedir,verbose)
        
        nmblookup = e("nmblookup -A {host} | grep '<00>' | grep -v '<GROUP>' | cut -d' ' -f1")

        info('Running task {bgreen}nmblookup-{port}{rst}' + (' with {bblue}' + nmblookup + '{rst}' if self.verbose >= 1 else '...'))

        try:
            hostname = subprocess.check_output(nmblookup, shell=True, stderr=subprocess.DEVNULL).decode().strip()
        except subprocess.CalledProcessError:
            return

        self.run_cmds([
            (
                e('dig -p{port} @{hostname} axfr > "{basedir}/{port}_dns_dig.txt"'),
                e('dig-{port}')
            )
        ])

        

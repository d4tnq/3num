import subprocess
from protocols.protocol import Protocol
from lib.colors import debug, info, warn, error, fail, e, Style, Fore
	#
	#  SMB
	#

class SMB_enum (Protocol):
    def __init__(self, host, port, service, basedir,verbose):
        Protocol.__init__(self, host, port, service, basedir,verbose)
        nmap_port = self.port
        if self.port == 139 or self.port == 445:
            nmap_port = '139,445'
        msfmodules = [
            {"path": "auxiliary/scanner/smb/smb_version", "toset": {"RHOSTS": self.host}},
        ]
        msf=self.create_msf_cmd(msfmodules)
        self.run_cmds([
			(
				e('nmap -vv --reason -sV -p {nmap_port} --script="(nbstat or smb*) and not (brute or broadcast or dos or external or fuzzer)" --script-args=unsafe=1 -oN "{basedir}/{port}_smb_nmap.txt" -oX "{basedir}/{port}_smb_nmap.xml" {host}'),
				e('nmap-{port}')
			),
			(
				e('enum4linux -a -M -l -d {host}  | tee "{basedir}/{port}_smb_enum4linux.txt"'),
				e('enum4linux-{port}')
			),			
			(
				e('nbtscan -rvh {host} | tee "{basedir}/{port}_smb_nbtscan.txt"'),
				e('nbtscan-{port}')
			),(
				e('{msf}'),
				e('msf-{port}')
			)
		])

        

import subprocess
from protocols.protocol import Protocol
from lib.colors import debug, info, warn, error, fail, e, Style, Fore
	#
	#  SMTP
	#

class SMTP_enum (Protocol):
    def __init__(self, host, port, service, basedir, verbose):
        Protocol.__init__(self, host, port, service, basedir,1)
        self.run_cmds([
			(
				e('nmap -vv --reason -sV -p {port} --script="(smtp*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{basedir}/{port}_smtp_nmap.txt" -oX "{basedir}/{port}_smtp_nmap.xml" {host}'),
				e('nmap-{port}')
			)
		])

        

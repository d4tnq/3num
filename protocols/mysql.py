from protocols.protocol import Protocol
from lib.colors import debug, info, warn, error, fail, e, Style, Fore
	#
	#  MYSQL
	#

class MYSQL_enum (Protocol):
    def __init__(self, host, port, service, basedir,verbose):
        Protocol.__init__(self, host, port, service, basedir,verbose)
        self.run_cmds([
			(
				e('nmap -vv --reason -sV -p {port} --script="(mysql*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{basedir}/{port}_mysql_nmap.txt" -oX "{basedir}/{port}_mysql_nmap.xml" {host}'),
				e('nmap-{port}')
			)
		])

        

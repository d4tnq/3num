from protocols.protocol import Protocol
from lib.colors import e 

class MYSQL_enum(Protocol):
    def __init__(self, host, port, service, basedir, verbose):
        super().__init__(host, port, service, basedir, verbose)  # Use super() for a cleaner call to the base class
        self.run_cmds([
            (
                e(f'nmap -vv -sV -p {port} --script="(mysql*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{basedir}/{port}_mysql_nmap.txt" -oX "{basedir}/{port}_mysql_nmap.xml" {host}'),
                e(f'nmap-{port}')
            )
        ])


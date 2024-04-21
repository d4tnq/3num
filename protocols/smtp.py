from protocols.protocol import Protocol
from lib.colors import e  # Import only what's needed

class SMTP_enum(Protocol):
    def __init__(self, host, port, service, basedir, verbose):
        super().__init__(host, port, service, basedir, 1)  # Using super() for base class initialization, forced verbose level to 1
        self.run_cmds([
            (
                e(f'nmap -vv -sV -p {port} --script="(smtp*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{basedir}/{port}_smtp_nmap.txt" -oX "{basedir}/{port}_smtp_nmap.xml" {host}'),
                e(f'nmap-{port}')
            )
        ])


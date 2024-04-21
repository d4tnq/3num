from protocols.protocol import Protocol
from lib.colors import e
import os
class HTTP_enum (Protocol):
    def __init__(self, host, port, service, basedir,verbose):
        Protocol.__init__(self, host, port, service, basedir,verbose)
        
        scheme = 'https' if 'https' in service or 'ssl' in service else 'http'
        nikto_ssl = ' -ssl' if 'https' in service or 'ssl' in service else '' 
        wordlist="/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"

        self.run_cmds([
            (
                e('nmap -vv --reason -sV -p {port} --script="(http* or ssl*) and not (broadcast or dos or external or http-slowloris* or fuzzer)" -oN "{basedir}/{port}_http_nmap.txt" -oX "{basedir}/{port}_http_nmap.xml" {host}'),
                e('nmap-{port}')
            ),
            (
                e('curl -i {scheme}://{host}:{port}/ -m 10 -o "{basedir}/{port}_http_index.html"'),
                e('curl-1-{port}')
            ),([
                e('whatweb -v {host}:{port} | tee "{basedir}/{port}_http_whatweb.txt"'),
                e('whatweb-{port}')
            ])
            
        ])


        self.run_cmds([
            (
                e('gobuster dir -w {wordlist} -t 10 -u {scheme}://{host}:{port} -e -b "404,403" | tee "{basedir}/{port}_http_dirb.txt"'),
                e('gobuster-{port}')
            ),
            (
                e('nikto -h {scheme}://{host}:{port}{nikto_ssl} -o "{basedir}/{port}_http_nikto.txt"'),
                e('nikto-{port}')
            )
        ])
        if(os.path.exists(f'results/{host}/80_http_whatweb.txt')):
            with open(f'results/{host}/80_http_whatweb.txt','r') as file:
                content=file.read()
                if('Wordpress' in content):
                    self.run_cmds([
                        e('wpscan --url {scheme}://{host}:{port} --api-token rZO8qXTzQkDWs5kkksDuZ5xZysMfQF2MUo6Rztsv9n8 --enumerate vp,vt --plugins-detection aggressive -o "{basedir}/{port}_http_wpscan.txt"'),
                        e('wpscan-{port}')
                    ])


        

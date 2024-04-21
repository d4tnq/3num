from protocols.protocol import Protocol
from lib.colors import e,info,error
import os
import requests
from bs4 import BeautifulSoup

class HTTP_enum(Protocol):
    def __init__(self, host, port, service, basedir, verbose):
        super().__init__(host, port, service, basedir, verbose)
        
        scheme = 'https' if 'https' in service or 'ssl' in service else 'http'
        nikto_ssl = ' -ssl' if scheme == 'https' else ''
        wordlist = "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"

        # Define all commands to be run
        commands = [
            (e(f'nmap -v -sV -T4 -p {port} --script="(http* or ssl*) and not (broadcast or dos or external or http-slowloris* or fuzzer)" -oN "{basedir}/{port}_http_nmap.txt" -oX "{basedir}/{port}_http_nmap.xml" {host}'), e(f'nmap-{port}')),
            (e(f'curl -i {scheme}://{host}:{port}/ -m 10 -o "{basedir}/{port}_http_index.html"'), e(f'curl-1-{port}')),
            (e(f'whatweb -v {host}:{port} | tee "{basedir}/{port}_http_whatweb.txt"'), e(f'whatweb-{port}')),
            (e(f'gobuster dir -w {wordlist} -t 10 -u {scheme}://{host}:{port} -e -b "404,403" | tee "{basedir}/{port}_http_dirb.txt"'), e(f'gobuster-{port}')),
            (e(f'nikto -h {scheme}://{host}:{port}{nikto_ssl} -o "{basedir}/{port}_http_nikto.txt"'), e(f'nikto-{port}')),
        ]

        # Execute all commands
        self.run_cmds(commands)

        if self.check_wordpress(scheme,host):
            info("Wordpress detected, running WPScan...")
            self.run_cmds([
                (e(f'wpscan --url {scheme}://{host}:{port} --api-token rZO8qXTzQkDWs5kkksDuZ5xZysMfQF2MUo6Rztsv9n8 --enumerate vp,vt --plugins-detection aggressive -o "{basedir}/{port}_http_wpscan.txt"'),
                e(f'wpscan-{port}'))
            ])
        else:
            error("No Wordpress found")
            
    def check_wordpress(self,scheme,host):
        try:
            response = requests.get(scheme+'://'+self.host)
            if 'wp-content' in response.text:
                return 1
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find_all(name='meta', attrs={'name': 'generator', 'content': 'WordPress'}):
                return 1
            return 0
        except requests.exceptions.RequestException as e:
            print(f"Error checking host: {e}")


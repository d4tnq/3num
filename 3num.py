#!/usr/bin/env python3
import os
import argparse
import subprocess
import multiprocessing
from libnmap.parser import NmapParser
from lib.colors import debug, info, error

from protocols.smb import SMB_enum
from protocols.http import HTTP_enum
from protocols.dns import DNS_enum
from protocols.smtp import SMTP_enum
from protocols.mysql import MYSQL_enum
import banner

class ActiveEnum:
    def __init__(self, verbose=0, deepscan=False, outdir='results', srvname=''):
        self.verbose = verbose
        self.deepscan = deepscan
        self.outdir = outdir
        self.srvname = srvname

    def run_cmd(self, cmd):
        info(f'Running command: {cmd}')
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if self.verbose > 1:
            debug(stdout.decode())
            error(stderr.decode())

        return proc.returncode == 0

    def run_nmap(self, address):
        out = os.path.join(self.outdir, address + self.srvname)
        nmap_file = f'{out}/tcp_nmap.xml'
        if not os.path.exists(out):
            os.makedirs(out, exist_ok=True)
        self.run_cmd(f'nmap -sV -sC -p- -T4 -oX "{nmap_file}" {address}')

        report = NmapParser.parse_fromfile(nmap_file)
        return [(address, svc.port, svc.service) for svc in report.hosts[0].services if svc.state == 'open']

    def enum_service(self, address, port, service):
        info(f'Enumerating {service} on {address}:{port}')
        basedir = os.path.join(self.outdir, address + self.srvname)
        os.makedirs(basedir, exist_ok=True)

        if 'smb' in service or ('netbios' in service and port in [139, 445]):
            SMB_enum(address, port, service, basedir,self.verbose)
        elif 'http' in service and port in [80, 443]:
            HTTP_enum(address, port, service, basedir,self.verbose)
        elif 'dns' in service:
            DNS_enum(address, port, service, basedir,self.verbose)
        elif 'smtp' in service:
            SMTP_enum(address, port, service, basedir,self.verbose)
        elif 'mysql' in service:
            MYSQL_enum(address, port, service, basedir,self.verbose)

    def scan_host(self, address):
        info(f'Scanning host {address}...')
        services = self.run_nmap(address)
        for address, port, service in services:
            self.enum_service(address, port, service)

if __name__ == '__main__':
    info(banner.intro)
    parser = argparse.ArgumentParser(description='Enumeration for nhom7.')
    parser.add_argument('address', help='address of the host.')
    parser.add_argument('-p', '--port', type=int, help='port of the service, if scanning only one port')
    parser.add_argument('-s', '--service', help='type of the service, when port is specified')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='enable verbose output, repeat for more verbosity')
    parser.add_argument('-o','--outdir',action="store",default="results",help='output file')
    args = parser.parse_args()

    scanner = ActiveEnum(verbose=args.verbose,outdir=args.outdir)
    if args.port:
        if(args.service is None):
            error("Service type is required when enumerating only 1 port!")
        else: 
            scanner.enum_service(args.address, args.port, args.service)

    else:
        scanner.scan_host(args.address)

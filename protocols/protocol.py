import os
import threading
import subprocess
import multiprocessing
from lib.colors import debug, info, error, Fore, Style

class Protocol:
    def __init__(self, host, port, service, basedir, verbose):
        self.host = host
        self.port = port
        self.service = service
        self.basedir = basedir
        self.verbose = verbose

    def _dump_pipe(self, stream, stop_event, tag, color):
        while not stop_event.is_set():
            line = stream.readline().decode('utf-8').strip()
            if line and self.verbose >= 1:
                debug(f'{color}[{Style.BRIGHT}{tag}{Style.NORMAL}] {Fore.RESET}{line}', color=color)

    def run_cmd(self, cmd, tag):
        redirect = self.verbose >= 2
        info(f'Running task {Fore.GREEN}{tag}{Fore.RESET}' + (f' with {Fore.BLUE}{cmd}{Fore.RESET}' if self.verbose >= 1 else '...'))
        
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            if redirect:
                thdout_event = threading.Event()
                thderr_event = threading.Event()
                threading.Thread(target=self._dump_pipe, args=(proc.stdout, thdout_event, tag, Fore.BLUE)).start()
                threading.Thread(target=self._dump_pipe, args=(proc.stderr, thderr_event, tag, Fore.RED)).start()

            ret = proc.wait()

            if redirect:
                thdout_event.set()
                thderr_event.set()

            if ret:
                error(f'Task {Fore.RED}{tag}{Fore.RESET} returned non-zero exit code: {ret}')
            else:
                info(f'Task {Fore.GREEN}{tag}{Fore.RESET} finished successfully.')

        return ret == 0

    def run_cmds(self, cmds):
        processes = [multiprocessing.Process(target=self.run_cmd, args=cmd) for cmd in cmds]
        for proc in processes:
            proc.start()
        for proc in processes:
            proc.join()

    def create_msf_cmd(self, params):
        return "msfconsole -q -x '" + "; ".join(
            f"use {p['path']}; " + "; ".join(f"set {k} {v}" for k, v in p['toset'].items()) + "; run" for p in params
        ) + "; exit'"


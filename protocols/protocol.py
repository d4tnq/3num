import os
import threading
import subprocess
from lib.colors import debug, info, warn, error, fail, e, Style, Fore
import multiprocessing
class Protocol:
    def __init__(self, host, port, service, basedir, verbose):
        self.host = host
        self.port = port
        self.service = service
        self.basedir = basedir
        self.verbose = verbose

    def dump_pipe(self, stream, stop_event=None, tag='?', color=Fore.BLUE):
        while stream.readable() and (stop_event is not None and not stop_event.is_set()):
            line = stream.readline().decode('utf-8').rstrip()

            if len(line) != 0 and int(self.verbose) >= 1:
                debug(color + '[' + Style.BRIGHT + tag + Style.NORMAL + '] ' + Fore.RESET + '{line}', color=color)


    def run_cmd(self, cmd, tag='?', redirect=None):
        if redirect is None:
            redirect = int(self.verbose) >= 2

        info('Running' + ' task {bgreen}{tag}{rst}' + (' with {bblue}{cmd}{rst}' if self.verbose >= 1 else '...'))


        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE if redirect else subprocess.DEVNULL, stderr=subprocess.PIPE if redirect else subprocess.DEVNULL)

        if redirect:
            thdout = threading.Event()
            thderr = threading.Event()

            threading.Thread(target=self.dump_pipe, args=(proc.stdout, thdout, tag)).start()
            threading.Thread(target=self.dump_pipe, args=(proc.stderr, thderr, tag, Fore.RED)).start()

        ret = proc.wait()

        if redirect:
            thdout.set()
            thderr.set()

        if ret != 0:
            error('Task {bred}{tag}{rst} returned non-zero exit code: {ret}')
        else:
            info('Task {bgreen}{tag}{rst} finished successfully.')

        return ret == 0


    def run_cmds(self, cmds):
        procs = []

        for cmd in cmds:
            proc = multiprocessing.Process(target=self.run_cmd, args=cmd)
            procs.append(proc)
            proc.start()

 

    def create_msf_cmd(self, params):
        cmd = "msfconsole -q -x '"
        for param in params:
            cmd += "use " + param["path"] + ";"
            for key in param["toset"]:
                cmd += "set "+key+" "+param["toset"][key]+";"
            cmd += "run;"
        cmd += "exit'"
        return cmd

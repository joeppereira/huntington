"""Supervise `openwiki visualize` child processes.

Uses subprocess.Popen plus a reader thread rather than asyncio subprocesses, which on Windows only
work under the Proactor event loop (not guaranteed under uvicorn).
"""

import re
import subprocess
import threading
import time
from collections.abc import Mapping
from pathlib import Path

import psutil

_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_OPEN_LINE = re.compile(r"^\s*open:\s*(http://\S+)")


def parse_visualizer_url(line: str) -> str | None:
    """Return the URL from the visualizer's `open: http://...` banner line (it auto-increments ports)."""
    match = _OPEN_LINE.match(_ANSI.sub("", line))
    return match.group(1) if match else None


def listening_port(pid: int, timeout: float = 5.0) -> int | None:
    """The loopback port `pid` is actually listening on.

    OpenWiki 0.7.0 leaves the first listen() callback attached when it retries on EADDRINUSE, so after
    an auto-increment it prints a stale banner with the taken port before the real one. The socket
    table is the reliable source.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            ports = [
                conn.laddr.port
                for conn in psutil.Process(pid).net_connections(kind="tcp")
                if conn.status == psutil.CONN_LISTEN and conn.laddr.ip == "127.0.0.1"
            ]
        except psutil.NoSuchProcess:
            return None
        if ports:
            return ports[0]
        time.sleep(0.1)
    return None


def kill_process_tree(pid: int) -> None:
    try:
        parent = psutil.Process(pid)
        procs = [*parent.children(recursive=True), parent]
    except psutil.NoSuchProcess:
        return  # already exited
    for proc in procs:
        try:
            proc.kill()
        except psutil.NoSuchProcess:
            pass
    psutil.wait_procs(procs, timeout=5)


class Visualizer:
    def __init__(
        self,
        name: str,
        cli_js: Path,
        wiki_dir: Path,
        port: int,
        env: Mapping[str, str],
        log_path: Path,
    ) -> None:
        self.name = name
        self._cli_js = cli_js
        self._wiki_dir = wiki_dir
        self._port = port
        self._env = dict(env)
        self._log_path = log_path
        self._proc: subprocess.Popen[str] | None = None
        self._url: str | None = None
        self._ready = threading.Event()

    @property
    def url(self) -> str | None:
        return self._url if self.is_running else None

    @property
    def is_running(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def start(self, timeout: float = 30.0) -> str:
        if self.is_running and self._url:
            return self._url
        self._ready.clear()
        self._url = None
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        args = ["node", str(self._cli_js), "visualize", str(self._wiki_dir), "--port", str(self._port), "--no-open"]
        self._proc = subprocess.Popen(
            args,
            env=self._env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        threading.Thread(target=self._pump_output, args=(self._proc,), daemon=True).start()
        port = listening_port(self._proc.pid) if self._ready.wait(timeout) and self._url else None
        if port is None:
            self.stop()
            raise RuntimeError(f"{self.name} visualizer did not start; see {self._log_path}")
        self._url = f"http://127.0.0.1:{port}"
        return self._url

    def _pump_output(self, proc: subprocess.Popen[str]) -> None:
        # Keeps draining stdout for the process lifetime so the pipe never fills and blocks the child.
        with self._log_path.open("a", encoding="utf-8") as log:
            assert proc.stdout is not None
            for line in proc.stdout:
                log.write(line)
                log.flush()
                if self._url is None and proc is self._proc:
                    url = parse_visualizer_url(line)
                    if url:
                        self._url = url
                        self._ready.set()
        # Process exited: unblock start(). Only for the current process: on restart() the old pump
        # reaches EOF after start() cleared the event, and must not wake the new process's wait.
        if proc is self._proc:
            self._ready.set()

    def restart(self, timeout: float = 30.0) -> str:
        """Stop and start again (re-scans the wiki; needed after OpenWiki replaces the wiki folder)."""
        self.stop()
        return self.start(timeout)

    def stop(self) -> None:
        if self._proc is not None:
            kill_process_tree(self._proc.pid)
            self._proc.wait(timeout=5)
        self._proc = None
        self._url = None

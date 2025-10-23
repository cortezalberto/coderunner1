"""
Docker Runner Service - Executes code in isolated Docker containers
"""
import subprocess
import time
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DockerRunResult:
    """Result of a Docker container execution"""
    stdout: str
    stderr: str
    returncode: int
    duration: float
    timed_out: bool


class DockerRunner:
    """Service for executing code in Docker containers"""

    def __init__(
        self,
        runner_image: str = None,
        workspace_dir: str = None,
        host_workspace_dir: str = None,
        default_cpus: str = "1.0",
        default_memory_mb: int = 256
    ):
        self.runner_image = runner_image or os.getenv("RUNNER_IMAGE", "py-playground-runner:latest")
        self.workspace_dir = workspace_dir or os.getenv("WORKSPACE_DIR", "/workspaces")
        self.host_workspace_dir = host_workspace_dir or os.getenv("HOST_WORKSPACE_DIR", "/workspaces")
        self.default_cpus = default_cpus
        self.default_memory_mb = default_memory_mb

    def run(
        self,
        workspace: str,
        timeout_sec: float = 5.0,
        memory_mb: int = None,
        cpus: str = None
    ) -> DockerRunResult:
        """
        Execute pytest in a Docker container

        Args:
            workspace: Path to workspace directory (in worker container)
            timeout_sec: Execution timeout in seconds
            memory_mb: Memory limit in MB
            cpus: CPU limit as string (e.g., "1.0")

        Returns:
            DockerRunResult with execution details
        """
        # Use defaults if not provided
        memory_mb = memory_mb or self.default_memory_mb
        cpus = cpus or self.default_cpus

        # Convert workspace path from worker to host
        workspace_rel = workspace.replace(self.workspace_dir, "").lstrip("/")
        host_workspace = f"{self.host_workspace_dir}/{workspace_rel}"

        # Build Docker command
        docker_cmd = self._build_command(
            host_workspace=host_workspace,
            memory_mb=memory_mb,
            cpus=cpus
        )

        # Execute with timeout
        start = time.time()
        timed_out = False

        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec + 2  # +2 seg buffer
            )
            duration = time.time() - start
            stdout = result.stdout
            stderr = result.stderr
            returncode = result.returncode

        except subprocess.TimeoutExpired:
            duration = time.time() - start
            stdout = ""
            stderr = "Timeout expired"
            returncode = -1
            timed_out = True

        return DockerRunResult(
            stdout=stdout,
            stderr=stderr,
            returncode=returncode,
            duration=duration,
            timed_out=timed_out
        )

    def _build_command(
        self,
        host_workspace: str,
        memory_mb: int,
        cpus: str
    ) -> list:
        """
        Build Docker run command

        Args:
            host_workspace: Workspace path on host machine
            memory_mb: Memory limit in MB
            cpus: CPU limit as string

        Returns:
            List of command arguments
        """
        return [
            "docker", "run", "--rm",
            "--network", "none",  # No network access
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
            f"--cpus={cpus}",
            f"--memory={memory_mb}m",
            "--memory-swap", f"{memory_mb}m",
            "-v", f"{host_workspace}:/workspace:rw",
            "-w", "/workspace",
            self.runner_image,
            "pytest", "-q", "--tb=short", "tests_public.py", "tests_hidden.py"
        ]


# Singleton instance
docker_runner = DockerRunner()

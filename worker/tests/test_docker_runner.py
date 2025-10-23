"""
Tests for DockerRunner service

Note: These are unit tests that mock Docker execution.
Integration tests with real Docker would require Docker daemon.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from worker.services.docker_runner import DockerRunner, DockerRunResult


class TestDockerRunner:
    """Test cases for DockerRunner"""

    def test_init_default_values(self):
        """Test DockerRunner initialization with default values"""
        runner = DockerRunner()

        assert runner.runner_image == "py-playground-runner:latest"
        assert runner.workspace_dir == "/workspaces"
        assert runner.host_workspace_dir is not None

    def test_init_custom_values(self):
        """Test DockerRunner initialization with custom values"""
        runner = DockerRunner(
            runner_image="custom-image:v1",
            workspace_dir="/custom/workspace",
            host_workspace_dir="/host/workspace"
        )

        assert runner.runner_image == "custom-image:v1"
        assert runner.workspace_dir == "/custom/workspace"
        assert runner.host_workspace_dir == "/host/workspace"

    def test_build_command_basic(self):
        """Test building basic Docker command"""
        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        workspace = "/workspaces/sandbox-123"
        cmd = runner._build_command(workspace, timeout_sec=5.0)

        assert "docker" in cmd
        assert "run" in cmd
        assert "--rm" in cmd
        assert "--network" in cmd
        assert "none" in cmd
        assert "py-playground-runner:latest" in cmd

    def test_build_command_with_memory_limit(self):
        """Test building command with memory limit"""
        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        workspace = "/workspaces/sandbox-123"
        cmd = runner._build_command(workspace, timeout_sec=5.0, memory_mb=256)

        assert "--memory=256m" in cmd
        assert "--memory-swap=256m" in cmd

    def test_build_command_with_cpu_limit(self):
        """Test building command with CPU limit"""
        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        workspace = "/workspaces/sandbox-123"
        cmd = runner._build_command(workspace, timeout_sec=5.0, cpus="1.0")

        assert "--cpus=1.0" in cmd

    def test_build_command_path_translation(self):
        """Test that workspace path is correctly translated"""
        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        workspace = "/workspaces/sandbox-abc-123"
        cmd = runner._build_command(workspace, timeout_sec=5.0)

        # Should translate /workspaces/xxx to /host/workspaces/xxx
        volume_arg = None
        for i, arg in enumerate(cmd):
            if arg == "-v":
                volume_arg = cmd[i + 1]
                break

        assert volume_arg is not None
        assert volume_arg.startswith("/host/workspaces/sandbox-abc-123:")

    @patch('subprocess.run')
    def test_run_success(self, mock_run):
        """Test successful Docker execution"""
        # Mock subprocess.run
        mock_run.return_value = Mock(
            stdout="....\\n4 passed in 0.15s",
            stderr="",
            returncode=0
        )

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=5.0
        )

        assert isinstance(result, DockerRunResult)
        assert result.returncode == 0
        assert result.stdout == "....\\n4 passed in 0.15s"
        assert result.stderr == ""
        assert result.timed_out is False
        assert result.duration >= 0

    @patch('subprocess.run')
    def test_run_with_stderr(self, mock_run):
        """Test Docker execution with stderr output"""
        mock_run.return_value = Mock(
            stdout="",
            stderr="Warning: something happened",
            returncode=0
        )

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=5.0
        )

        assert result.returncode == 0
        assert result.stderr == "Warning: something happened"

    @patch('subprocess.run')
    def test_run_timeout(self, mock_run):
        """Test Docker execution timeout"""
        import subprocess

        # Mock timeout exception
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=['docker', 'run'],
            timeout=5.0
        )

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=5.0
        )

        assert result.timed_out is True
        assert result.returncode == -1
        assert "timeout" in result.stderr.lower() or "timeout" in result.stdout.lower()

    @patch('subprocess.run')
    def test_run_with_error_returncode(self, mock_run):
        """Test Docker execution with non-zero return code"""
        mock_run.return_value = Mock(
            stdout="",
            stderr="Error: test failed",
            returncode=1
        )

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=5.0
        )

        assert result.returncode == 1
        assert result.timed_out is False

    @patch('subprocess.run')
    def test_run_exception_handling(self, mock_run):
        """Test handling of unexpected exceptions"""
        mock_run.side_effect = Exception("Unexpected error")

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=5.0
        )

        assert result.returncode == -1
        assert "error" in result.stderr.lower() or "error" in result.stdout.lower()
        assert result.timed_out is False

    @patch('subprocess.run')
    def test_run_with_memory_and_cpu_limits(self, mock_run):
        """Test run with both memory and CPU limits"""
        mock_run.return_value = Mock(
            stdout="tests passed",
            stderr="",
            returncode=0
        )

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=10.0,
            memory_mb=512,
            cpus="2.0"
        )

        # Verify that subprocess.run was called
        assert mock_run.called
        call_args = mock_run.call_args

        # Check that the command includes memory and CPU limits
        cmd = call_args[0][0]
        assert "--memory=512m" in cmd
        assert "--cpus=2.0" in cmd

    def test_docker_run_result_dataclass(self):
        """Test DockerRunResult dataclass structure"""
        result = DockerRunResult(
            stdout="output",
            stderr="error",
            returncode=0,
            duration=1.5,
            timed_out=False
        )

        assert result.stdout == "output"
        assert result.stderr == "error"
        assert result.returncode == 0
        assert result.duration == 1.5
        assert result.timed_out is False

    def test_singleton_instance(self):
        """Test that docker_runner is a singleton"""
        from worker.services.docker_runner import docker_runner

        assert docker_runner is not None
        assert isinstance(docker_runner, DockerRunner)

    @patch('subprocess.run')
    def test_run_measures_duration(self, mock_run):
        """Test that run() measures execution duration"""
        import time

        def slow_run(*args, **kwargs):
            time.sleep(0.1)  # Simulate slow execution
            return Mock(stdout="", stderr="", returncode=0)

        mock_run.side_effect = slow_run

        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        result = runner.run(
            workspace="/workspaces/sandbox-123",
            timeout_sec=5.0
        )

        # Duration should be at least 0.1 seconds
        assert result.duration >= 0.1

    def test_path_translation_edge_cases(self):
        """Test path translation with edge cases"""
        runner = DockerRunner(
            workspace_dir="/workspaces",
            host_workspace_dir="/host/workspaces"
        )

        # Test with trailing slash
        workspace = "/workspaces/sandbox-123/"
        cmd = runner._build_command(workspace, timeout_sec=5.0)

        volume_arg = None
        for i, arg in enumerate(cmd):
            if arg == "-v":
                volume_arg = cmd[i + 1]
                break

        assert volume_arg is not None
        # Should handle trailing slash correctly
        assert "/host/workspaces/sandbox-123" in volume_arg

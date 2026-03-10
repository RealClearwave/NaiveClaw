import subprocess

def run_command(command: str) -> str:
    """
    Runs a shell command and returns the output (stdout or stderr).
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10 # Prevent hanging
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Exception: {str(e)}"

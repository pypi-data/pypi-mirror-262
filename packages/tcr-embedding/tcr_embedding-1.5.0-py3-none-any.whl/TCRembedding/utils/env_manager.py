import os
import subprocess
from pathlib import Path
import platform

class VirtualEnvManager:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)

    def setup_virtualenv(self, env_name, custom_env_dir=None, mirror_url=None):
        """设置虚拟环境并安装依赖"""
        requirements_path = self.base_dir / env_name / "requirements.txt"
        env_dir = Path(custom_env_dir) if custom_env_dir else self.base_dir / env_name / f"{env_name}_venv"

        if not env_dir.exists():
            env_dir.mkdir(parents=True, exist_ok=True)
            print(f"Creating virtual environment at {env_dir} for {env_name}...")
            subprocess.run(["python", "-m", "venv", str(env_dir)], check=True)
            subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip", "-i", mirror_url])
            if requirements_path.exists():
                print(f"Installing dependencies for {env_name} from {requirements_path}...")
                pip_command = env_dir / "bin" / "pip" if platform.system() != "Windows" else env_dir / "Scripts" / "pip"
                install_command = [str(pip_command), "install", "-r", str(requirements_path)]
                if mirror_url:
                    install_command += ["-i", mirror_url]
                subprocess.run(install_command, check=True)
            else:
                print(f"No requirements.txt found for {env_name}. Skipping dependencies installation.")
        else:
            print(f"Virtual environment for {env_name} already exists at {env_dir}.")

        self._print_activate_instruction(env_dir)

    def _print_activate_instruction(self, env_dir):
        """输出激活虚拟环境的指令，根据操作系统差异调整"""
        if platform.system() == "Windows":
            activate_script = env_dir / "Scripts" / "activate.bat"
            print(f"\nTo activate the virtual environment on Windows, run:")
        else:
            activate_script = env_dir / "bin" / "activate"
            print(f"\nTo activate the virtual environment on Unix or MacOS, run:")

        print(f"{activate_script}")

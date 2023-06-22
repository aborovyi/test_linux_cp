"""
This class contains filestructure for testing purposes.
This should be (ideally a separate) package, but for the demo purpose let's
stop here.
"""

import os
import subprocess
from pathlib import Path
from typing import Union


class DirStructure:
    """
    Create a structure of files for testing
    """

    files_and_content = [
        ("srcA", "spam"),
        ("srcB", "ham"),
        ("SrcDir/srcC", "foo"),
        ("SrcDir/SrcSubDir/srcD", "bar"),
    ]
    links = [("srcLink", "srcA")]

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

        for file, cnt in self.files_and_content:
            f_path = Path(self.root_dir) / file
            f_path.parent.mkdir(parents=True, exist_ok=True)
            f_path.write_text(cnt)
            self.__setattr__(f_path.name, f_path)

        for src, dst in self.links:
            src_path = Path(self.root_dir) / src
            dst_path = Path(self.root_dir) / dst
            src_path.symlink_to(dst_path.absolute())
            self.__setattr__(dst_path.name, dst_path)

        self.update_env()

    def call_cmd(self, cmd, timeout=10):
        """
        Run any system command.
        """
        subp = subprocess.run(
            cmd, capture_output=True, shell=True, check=False, timeout=timeout
        )
        return subp.returncode, subp.stdout, subp.stderr

    def call_copy(self, src="", dst="", flags="", timeout=10):
        """
        Run system `cp` app.
        """
        if not isinstance(src, str):
            src = str(src)
        if not isinstance(dst, str):
            dst = str(dst)
        cmd = " ".join(
            [f"cd {self.root_dir.absolute()};cp", flags, src, dst]
        ).strip()
        subp = subprocess.run(
            cmd,
            capture_output=True,
            shell=True,
            check=False,
            timeout=timeout,
        )
        return subp.returncode, subp.stdout, subp.stderr

    def update_env(self, lang: str = "C"):
        """
        Sets forcibly environment to <lang>, to test correctly messages.
        """
        self._original_env = os.environ.copy()
        os.putenv("LANG", lang)
        os.putenv("LC_ALL", lang)

    def set_attr(self, file: Union[str, Path] = "", attr: str = ""):
        """
        Set attribute to the file, using chattr command.

        This functionality requires either running tests from root user, or
        adding NOPASSWD option to /etc/sudoers. See README.md for more details.
        """
        if isinstance(file, str):
            file = Path(file).resolve()

        subp = subprocess.run(
            f"sudo chattr {attr} {file}",
            shell=True,
            capture_output=True,
            check=False,
        )
        return subp

    def clean(self):
        """
        Reset and clean directories and files.
        """
        dirs_to_drop = []
        for dirpath, _, files in os.walk(self.root_dir, topdown=True):
            for file in files:
                target_file = Path(dirpath) / file
                if target_file.exists() and not target_file.is_symlink:
                    target_file.chmod(0o666)  # Reset permissions if any
                target_file.unlink(missing_ok=True)
            if dirpath not in dirs_to_drop:
                dirs_to_drop.append(dirpath)

        for dirname in dirs_to_drop[::-1]:
            drop_dir = Path(dirname)
            if drop_dir.exists():
                drop_dir.chmod(0o777)
                drop_dir.rmdir()

"""
    This module will handle all filesystem interactions
    The FSManager class is the base class for all filesystem managers
"""
import os
import subprocess

class FSManager:
    """Base class for all FS operations.

    Attributes:
        fs_path (type): path to the fs location.

    Methods:
        execute: Execute command
        commit: Commit SQL calls
        revert: "Revert changes to previous commit through git LFS
        initialize_git_lfs: Initialize the current directory as a git lfs repo if it isn't already
    """
    def __init__(self, fs_path=None):
        """Initialize the FSManager.
        
        Args:
            fs_path (str): path to the fs path. Default is CWD
        """
        if not fs_path:
            self.fs_path = os.getcwd()
        else:
            self.fs_path = fs_path

    def execute(self, command: str):
        """Execute command.
        
        Args:
            command (str): Command to execute.
        """
        return subprocess.call(command, shell=True, cwd=self.fs_path)
    
    def commit(self, message='Auto-commit via FSManager', clean=True):
        """Commit all current changes through git LFS"""
        try:
            self.execute(f'git add .')  # Stage all changes
            self.execute(f'git commit -m "{message}"')  # Commit with a message
            if clean:
                self.execute('rm -rf .git')  # Remove git once commit happens to save space
        except Exception as e:
            print(f"Error during commit: {e}")
    
    def revert(self, clean=True):
        """Revert changes to previous commit through git LFS"""
        try:
            self.execute('git clean -fd')  # Remove untracked files and directories
            if clean:
                self.execute('rm -rf .git')  # Remove git once revert happens to save space
        except Exception as e:
            print(f"Error during revert: {e}")
    
    def initialize_version_control(self):
        """Initialize the current directory as a git lfs repo if it isn't already."""
        if not os.path.exists(os.path.join(self.fs_path, '.git')):
            try:
                self.execute('git init')  # Initialize git repository
                if self._exceed_directory_size(os.getcwd()):
                    self.execute('git lfs install')  # Initialize git LFS
                    print("Initialized current directory as a Git LFS repository.")
                else:
                    print("Initialized current directory as a Git repository.")
                self.commit("Init", clean=False)
            except Exception as e:
                print(f"Error during Git initialization: {e}")
        else:
            print("Current directory is already a Git repository.")

    def _exceed_directory_size(self, path):
        """Calculates the total size of the directory in bytes."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
                    if total_size >= 200 * 1024 * 1024:
                        return True
        return False


import sys
import termios

__all__ = ["_riscv"]

# pylint: disable=invalid-name
stdin_fd = None
old_termios = None

if sys.stdin.isatty():
    # Get the file descriptor for standard input
    stdin_fd = sys.stdin.fileno()
    # Get the current terminal settings
    old_termios = termios.tcgetattr(stdin_fd)

# Import _riscv (which indirectly loads libriscv.so and messes up the terminal)
# pylint: disable=wrong-import-position
from . import _riscv

if stdin_fd is not None and old_termios is not None:
    # Restore the old settings after importing _riscv
    termios.tcsetattr(stdin_fd, termios.TCSAFLUSH, old_termios)

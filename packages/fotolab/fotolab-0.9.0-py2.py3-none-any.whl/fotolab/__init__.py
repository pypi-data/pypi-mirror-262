# Copyright (C) 2024 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""A console program that manipulate images."""

import logging
import os
import subprocess
import sys

__version__ = "0.9.0"

log = logging.getLogger(__name__)


def _open_image(filename):
    """Open generated image using default program."""
    if sys.platform == "linux":
        subprocess.call(["xdg-open", filename])
    elif sys.platform == "darwin":
        subprocess.call(["open", filename])
    elif sys.platform == "windows":
        os.startfile(filename)

    log.info("open image: %s using default program.", filename.resolve())

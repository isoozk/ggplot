from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
from .geom import geom
import numpy as np


class geom_linerange(geom):
    DEFAULT_AES = {'color': 'black', 'alpha': None, 'linetype': 'solid', 'size': 1.0}
    REQUIRED_AES = {'x', 'ymin', 'ymax'}
    DEFAULT_PARAMS = {'stat': 'identity', 'position': 'identity'}

    _aes_renames = {'size': 'linewidth', 'linetype': 'linestyle'}
    _units = {'alpha', 'color', 'linestyle'}

    def __init__(self, *args, **kwargs):
        super(geom_linerange, self).__init__(*args, **kwargs)
        self._warning_printed = False

    def _plot_unit(self, pinfo, ax):
        if 'linewidth' in pinfo and isinstance(pinfo['linewidth'], list):
            # ggplot also supports aes(size=...) but the current mathplotlib
            # is not. See https://github.com/matplotlib/matplotlib/issues/2658
            pinfo['linewidth'] = 4
            if not self._warning_printed:
                msg = "'geom_lineragne()' currenty does not support the mapping of " +\
                      "size ('aes(size=<var>'), using size=4 as a replacement.\n" +\
                      "Use 'geom_linerange(size=x)' to set the size for the whole line.\n"
                sys.stderr.write(msg)
                self._warning_printed = True

        x = pinfo.pop('x')
        ymin = pinfo.pop('ymin')
        ymax = pinfo.pop('ymax')

        if 'levels' in pinfo:
            levels = pinfo.pop('levels')
            if 'x' in levels:
                levels = levels['x']

        left = np.arange(0, len(levels) + 2)
        i = 0
        for level in levels:
            i += 1
            for (_x, _ymin, _ymax) in zip(x, ymin, ymax):
                if _x==level:
                    ax.plot([i, i], [_ymin, _ymax], **pinfo)

        ax.set_xticks(left)
        ax.set_xticklabels([""] + levels)

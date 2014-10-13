"""
Nathan's matplotlib-based plotting tools.
"""

from . import tkplot, tikzplot

import numpy as np
import pandas as pd
#import seaborn as sns
import mpltools.style
mpltools.style.use('ggplot')
import scipy.stats

class Figure(tkplot.MatplotFigure):
    def save_as_tikz(self, filename, path='plots/'):
        tikzplot.save_matplotlib_for_paper(self.figure, filename, path)

    def _set_label(self, spec, which_coor):
        if hasattr(spec, 'name'):
            label = spec.name
        elif isinstance(spec, str):
            label = spec
        else:
            return
        method = getattr(self.axis, 'set_' + which_coor + 'label')
        method(label)
        
    def scatter(self, x, y, xscale='linear', yscale='linear', xlabel=None, ylabel=None,
                regression=False, annotate=True, **kwargs):
        data = pd.DataFrame({'x':x, 'y':y})
        data = data[data.x.notnull()&data.y.notnull()]
        ax = self.axis
        ax.scatter(data.x, data.y, **kwargs)
        ax.set_xscale(xscale), ax.set_yscale(yscale)
        if xlabel is None:
            xlabel = x
        if ylabel is None:
            ylabel = y
        self._set_label(xlabel, 'x'), self._set_label(ylabel, 'y')
        if regression:
            self.add_regression_line(data.x, data.y, annotate)
        else:
            self.draw()

    def add_regression_line(self, x, y, annotate=True):
        ax = self.axis
        if ax.get_xscale() =='log':
            x = np.log10(x)
        if ax.get_yscale() =='log':
            y = np.log10(y)
        slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)
        xr = np.max(x) - np.min(x)
        xs = [np.min(x)-xr*0.03, np.max(x)+xr*0.03]
        ys = [slope*a + intercept for a in xs]
        if ax.get_xscale() =='log':
            xs = [10**a for a in xs]
        if ax.get_yscale() == 'log':
            ys = [10**a for a in ys]
        ax.plot( xs, ys, linewidth=1.5, color='#040404' )
        posargs = dict(transform=ax.transAxes, verticalalignment='top',
                    horizontalalignment='right')
        if annotate:
            ax.text(0.2, 0.95, 'slope=%.3f' % slope, **posargs)
            ax.text(0.2, 0.85, 'intercept=%.3f' % intercept, **posargs)
            ax.text(0.2, 0.75, 'r=%.3f' % r, **posargs)
        self.draw()


def histogram(dataframe, column, fancy_col_name=None, bins=50, figure=None):
    """
    Make a nice histogram from a Pandas DataFrame column
    """ 
    data = dataframe[column]
    if figure is None:
        figure = Figure()
    ax = figure.axis
    ax.hist(np.asarray(data), bins=bins, normed=True)

    if fancy_col_name is None:
        fancy_col_name = column.replace('_', '')
    ax.set_xlabel(fancy_col_name, labelpad=20)
    
    posargs = dict(transform=ax.transAxes, verticalalignment='top',
                horizontalalignment='right')
    ax.text(0.95, 0.95, '$\mu=%.1f$' % data.mean(), **posargs)
    ax.text(0.95, 0.75, '$\mathrm{median}=%.1f$' % data.median(), **posargs)
    ax.text(0.95, 0.55, '$\sigma=%.1f$' % data.std(), **posargs)
    return figure

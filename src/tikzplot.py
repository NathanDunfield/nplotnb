"""
Saving Matplotlib figures so that all text becomes a TikZ overlay.

Typical usage:

sage: import sagetikzplot
sage: F
<matplotlib.figure.Figure object at 0x11941da50>
sage: print sagetikzplot.matplotlib_tikz_labels(F, "/tmp/figure.pdf")
\begin{tikzoverlayabs}[width=4in]{/tmp/figure.pdf}[\footnotesize]
  \draw (0.512500, 0.042083) node[ below] {Volume};
   ...
\end{tikzoverlayabs}

Also includeds the utility function

matplotlib_with_opts_matching_save

to allow saving of Sage graphics.  
"""


from matplotlib.text import Text
from matplotlib.backends.backend_agg import FigureCanvasAgg
from collections import Counter
import os

def matplotlib_with_opts_matching_save(sage_graphic, **kwds):
    """
    The method Graphics.matplotlib doesn't produce the same 
    matplotlib.Figure as is used in Graphics.save/Graphics.show.
    This function matches what Graphics.save does.  
    """
    options = sage_graphic.SHOW_OPTIONS.copy()
    options.update(sage_graphic._extra_kwds)
    options.update(kwds)
    for opt in ['dpi', 'transparent', 'fig_tight']:
        options.pop(opt)
    figure = sage_graphic.matplotlib(**options)
    figure.set_canvas(FigureCanvasAgg(figure))
    figure.tight_layout()
    return figure

def position(fig, T):
    text_trans = T.get_transform().transform_point
    if hasattr(fig, 'transFigure'):
        fig = fig.transFigure
    fig_trans = fig.transform_point
    return tuple(fig_trans(text_trans(T.get_position())))

def convert_Text_to_tikz(figtrans, T):
    x, y = position(figtrans, T)
    horizontal = {'left':'right', 'center':'', 'right':'left'}[T.get_horizontalalignment()]
    vertical = {'top':'below', 'bottom':'above', 'center':'',
                'baseline':'', 'center_baseline':''}[T.get_verticalalignment()]
    horvert = vertical + ' ' + horizontal
    if T.get_rotation():
        horvert = 'rotate=%.1f' % T.get_rotation()
    text = T.get_text().replace(r'\mathdefault', '').replace(u'\u2212', '-')
    try:  # Make tic lables in mathmode.
        float(text)
        text = '$' + text + '$'
    except ValueError:
        pass
    return "  \\draw (%.6f, %.6f) node[%s] {%s};" % (x, y, horvert.strip(), text)

def save_without_text(matplotlib_figure, filename):
    matplotlib_figure.savefig(filename)  # Hack to finalize the figure. 
    texts = [T for T in matplotlib_figure.findobj(Text) if T.get_text()]
    alphas = [T.get_alpha() for T in texts]
    for T in texts:
        T.set_alpha(0.0)
    matplotlib_figure.savefig(filename)
    for a, T in zip(alphas, texts):
        T.set_alpha(a)

def convert_labels_to_tikz(matplotlib_figure):
    def pos(T):
        return position(matplotlib_figure, T)
    texts = [T for T in matplotlib_figure.findobj(Text) if T.get_text()]
    label_positions = Counter([pos(T) for T in texts])
    bad = [b[0] for b in label_positions.most_common(2) if b[1] > 3]
    texts = [T for T in texts if not pos(T) in bad]
    figtrans = matplotlib_figure.transFigure.inverted()
    return "\n".join( [convert_Text_to_tikz(figtrans, T) for T in texts]) 


#def sageplot_tikz_labels(graphic, filename):
#    save_graphic_for_tikz_overlay(graphic, filename)
#    return convert_labels_to_tikz(graphic)

def matplotlib_tikz_labels(figure, filename,
                           relative_filename=None, width='4in', font='\\footnotesize'):
    save_without_text(figure, filename)
    if relative_filename is None:
        relative_filename = filename    
    head = "\\begin{tikzoverlayabs}[width=%s]{%s}[%s]\n" % (
        width, relative_filename, font)
    foot = "\n\\end{tikzoverlayabs}"
    return head + convert_labels_to_tikz(figure) + foot

def save_matplotlib_for_paper(figure, filename, path='plots/'):
    """
    Saving a matplotlib figure for use in a paper.  The given filename
    can be of type ".pdf" or ".png" as appropriate.  The graphics
    are saved in the subdirectory "images" of the given "path" with 
    the TikZ code itself is saved in a corresponding ".tex" file in "path".  
    """
    base = os.path.splitext(filename)[0]
    imagename = os.path.join(path, 'images', filename) 
    save_without_text(figure, imagename)
    labels = matplotlib_tikz_labels(figure, imagename,
                                    relative_filename=os.path.join('plots/images', filename),
                                    width='\\matplotlibfigurewidth',
                                    font='\\matplotlibfigurefont')
    texname = os.path.join(path, base + '.tex')
    texfile = open(texname, 'w')
    texfile.write(labels + '\n')
    texfile.close()
        
if __name__ == "__main__":
    import numpy, matplotlib
    figure = matplotlib.figure.Figure(figsize=(10,6), dpi=100)
    FigureCanvasAgg(figure)
    axis = figure.add_subplot(111)
    t = numpy.arange(0.0,3.0,0.01)
    axis.plot(t,numpy.sin(2*numpy.pi*t))
    axis.set_title(r'Plot of $\sin(t)$')
    axis.set_xlabel(r'$t$')
    axis.set_ylabel(r'$\sin(t)$')
    save_matplotlib_for_paper(figure, 'test.pdf', '/tmp/plots')
    figure.savefig('/tmp/plots/raw_figure.pdf')
              
    
    



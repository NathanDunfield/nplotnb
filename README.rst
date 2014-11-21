Nathan Dunfield's personal Python-based plotting suite. 
=======================================================

Uses: Matplotlib, Pandas, and mpltools.

Installation 
------------

In the directory containing the file "setup.py" do::

   python setup.py install  

Replace "python" by "sage -python" if you're going to be using this
inside Sage.


Advanced Installation: Using Tk backend within Sage
---------------------------------------------------

Matplotlib does all the 2D graphics for Sage, but unfortunately none
of its GUI backends are compiled by default. (You can still use
Matplotlib inside an IPython notebook or by saving things directly to
graphics files.)  The following suffices to compile the Tk backend on
Linux, provided you have the tk-dev(el) package installed::

  export SAGE_MATPLOTLIB_GUI=yes; sage -f matplotlib

This doesn't work on OS X because in addition to TkAgg, Sage will try
to compile the native Mac backend, which fails since Sage doesn't
include an Objective-C compiler.  For OS X, download the source
tarball for matplotlib, and then do::

  cd matplotlib-*
  sage -sh echo '[gui_support]' >> setup.cfg
  echo 'macosx=false' >> setup.cfg
  python setup.py install

Also, if one has freetype or libpng installed via brew, one should
temporarily unlink them to avoid conflicting with Sage's internal
version.

Note that the TkAgg backend will be compiled against one's current
version of Tk, which might not be the one that Sage is linked against.
So inaddition one may need to recompile the Tkinter module via::

   sage -f python



Documentation 
-------------

I wrote this for my own personal use, so "Use the source, Luke!". 


License
--------

Copyright 2014 to present by Nathan Dunfield; released under the terms
of the GNU General Public License, version 2 or later.


bibcat
======

what is bibcat
--
It takes a bibtex file and for each entry will call the arXiv API and try
and find its arXiv category from the title. Supposing it is able to find
it, it will then write that entry into a file of that name. After doing this, there
is another script that will go on to combine these files into "main" bibtex files
which can then be browser conveniently in, say, [JabRef](http://jabref.sourceforge.net/).


why would I want to do that?
--
Like me, you may have far too many bibtex entries in a single file, and so you'd like
to split them in some fashion that makes sense. I happen to think that this way makes
sense.


how do I use it?
--
clone it from github:

    git clone git://github.com/silky/bibcat.git

go into the directionry

    cd bibcat

run bibcat on your bibtex file

    python bibcat.py sample.bib

observe that many .bib files have been created in your current directory. Hence, you
may now optionally run *do_group.py*, which will trivially group the bib files by
concatinating them in the wat you specify

    python do_group.py

observe that grouped bibtex files have now been created in your current directory.
rejoice.


what do I need?
--
Python. and you'll want to pip install the relevant dependencies (these will be
apparent by running it).

The exact dependencies are:

  * Python 2.7+ (Works on this version at least)
  * pip (then "pip install feedparser")
  * cat (if you're running linux or mac you probably have this)
  * A "nicely" formatted bibtex file. Specifically, each key/value should be on a
    seperate line and preferably be always surrounded by curly-braces: {}; this is the
    standard representation in JabRef.


how do I specify the "main" categories?
--
By editing the *do_groups.py* file; it allows you to specify files and wildcards for
the output (of bibcat) that it should include in this file. Notably, it works by just
concatenating the files together.

Note that if it can't locate a file on the arXiv it will write it to the "nocat.bib"
file.


faqs
--

None yet; email [me](mailto:noonsilk+bibcat@gmail.com) if you'd like help using it though.

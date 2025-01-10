The FASLR documentation can be found by going to:

https://faslr.com/docs

# Style Guide

Due to the documentation's current reliance on [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/), the styling is subject to change as new versions are released. However, there are some things that I'd like to keep consistent, so here's a checklist of things to adjust if a new version changes the look and feel of things:

- Landing page should only be as big as what you'd see on a standard 4k monitor (that is, the user should be able to see the entire landing page without having to scroll.
- The gallery page should not have sidebars on either side.

# Deployment

New versions of the docs are deployed via SSH by logging into the server, and then running the file **build_docs.sh** that is also located in this directory. This build script will pull the repo contents and then run the sphinx command **make html**.
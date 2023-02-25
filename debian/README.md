# Debian Packaging notes

edit the .bashrc file:

```
DEBEMAIL="genedan@gmail.com"
DEBFULLNAME="Gene Dan"
export DEBEMAIL DEBFULLNAME

# mc related
if [ -f /usr/lib/mc/mc.sh ]; then
  . /usr/lib/mc/mc.sh
fi
```
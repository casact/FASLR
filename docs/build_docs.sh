git pull;
make html;
cp -fR _build/html/* /var/www/faslr.com/docs;
cd /var/www/faslr.com/media;
git pull;
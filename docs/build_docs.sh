cd /root/faslr/docs;
git pull;
make html;
cp -fR _build/html/* /var/www/faslr.com/docs;
cd /var/www/faslr.com/media;
git pull;

cd /root/faslr;
python3 faslr/samples/db/generate_sample_db.py;
mv sample.db ../schema/sample.db;
cd /root/schema;
java -jar schemaspy-6.2.3.jar -t sqlite-xerial -dp sqlite-jdbc-3.42.0.0.jar -db sample.db -sso -s sample -cat % -o db;
sed -i "s/sample.db.sample/FASLR/g" db/index.html;
sed -i "s/sample.db/FASLR/g" db/index.html;
sed -i "s/.sample//g" db/index.html;
sed -i "s/sample.db.sample/FASLR/g" relationships.html;
sed -i "s/sample.db.sample/FASLR/g" columns.html;
sed -i "s/sample.db.sample/FASLR/g" anomalies.html;
sed -i "s/sample.db.sample/FASLR/g" constraints.html;
sed -i "s/sample.db.sample/FASLR/g" orphans.html;
sed -i "s/sample.db.sample/FASLR/g" routines.html;
mv db/sample.db.sample.xml db/FASLR.xml
cp -fR db/* /var/www/faslr.com/db;
import sys
sys.path.append('//faslr')
from datetime import  datetime
import time
from faslr.constants import BUILD_VERSION

d = datetime.now()
datetime_string = d.strftime("%a, %d, %b %Y %H:%M:%S ")
tz_offset = str(int(- time.timezone * 100 / 3600)).zfill(5)
datetime_string = datetime_string + tz_offset

codename = 'jammy'
urgency = 'medium'
package_name = 'faslr'

changelog_string = """{} ({}) {}; urgency={}

  * Additional release
  
 -- Gene Dan <genedan@gmail.com> {}"""\
    .format(package_name, BUILD_VERSION, codename, urgency, datetime_string)

with open('debian/changelog', 'w') as changelog_file:
    changelog_file.write(changelog_string)

changelog_file.close()
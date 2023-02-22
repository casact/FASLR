import sys
sys.path.append('//faslr')
from datetime import  datetime
from time import tzname
from faslr.constants import BUILD_VERSION

# d = datetime.now(tz=tzname[0])
datetime_string = d.strftime("%a, %d, %b %Y %H:%M:%S %z")
datetime_string
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
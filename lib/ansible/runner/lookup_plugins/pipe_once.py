# (c) 2012, Daniel Hokka Zakrisson <daniel@hozac.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
from ansible import utils, errors

CACHE = {}

class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, **kwargs):


        if isinstance(terms, basestring):
            terms = [ terms ]
        ret = []
        for term in terms:
            if term in CACHE:
                ret.append(CACHE.get(term))
                continue
            p = subprocess.Popen(term, cwd=self.basedir, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout, stderr) = p.communicate()
            if p.returncode == 0:
                result = stdout.strip()
                CACHE[term] = result
                ret.append(result)
            else:
                raise errors.AnsibleError("lookup_plugin.pipe(%s) returned %d" % (term, p.returncode))
        return ret

import re
import os
import codecs


class PARSER:
    def __init__(self):
        self.patterns = {
            'username': '\s+\*\s+Username\s+:\s+',
            'isusername': '\$\s*$|\(null\)\s*$|\@\s*$',
            'password': '\s+\*\s+Password\s+:\s+',
            'ispassword': '\(null\)\s*$',
            'domain': '\s+\*\s+Domain\s+:\s+',
            'isdomain': '\(null\)\s*$'}
        self.list = []

    def parsing(self, path):
        files = self.detectfiles(path)
        for filename in files:
            with codecs.open(filename, "r", encoding='utf-8',
                             errors='ignore') as file:
                data = file.readlines()

                for line in range(0, len(data) - 2):
                    username = self.search('username', data[line],
                                           'isusername')

                    if username:
                        domain = self.search('domain', data[line + 1],
                                             'isdomain')

                        if domain:
                            password = self.search('password', data[line + 2],
                                                   'ispassword')

                            if password:
                                self.addlist(username, domain, password)

                file.close()

            return self.list

    def addlist(self, username, domain, password):
        control = True

        for u, p, d in self.list:
            if u == username and p == password and d == domain:
                control = False
                break

        if control:
            self.list.append([username, password, domain])

        return self.list

    def search(self, pattern, data, control):
        if (re.search(r'{}'.format(self.patterns[pattern]), data) and
                not re.search(r'{}'.format(self.patterns[control]), data)):
            return re.sub(r'{}'.format(self.patterns[pattern]), '',
                          data).rstrip()
        else:
            return False

    @staticmethod
    def detectfiles(path):
        if os.path.isfile(path):
            return {path}
        else:
            return os.listdir(path)

import re
import os
import codecs

from mimikatz_parser.output import OUTPUT


class PARSER:
    def __init__(self, args):
        self.output = OUTPUT(args)
        self.patterns = {
            'username': '\s+\*\s+Username\s+:\s+',
            'isusername': '\$\s*$|\(null\)\s*$|\@\s*$',
            'password': '\s+\*\s+Password\s+:\s+',
            'ispassword': '\(null\)\s*$',
            'domain': '\s+\*\s+Domain\s+:\s+',
            'isdomain': '\(null\)\s*$'
        }
        self.list = []
        self.limit = args.limit
        self.one_file = args.all
        self.parsing(args.input)

    def parsing(self, path):
        files = self.detect_files(path)
        self.list = []
        for file_name in files:
            with codecs.open('%s%s' % (path, file_name), 'r', encoding='utf-8', errors='ignore') as file:
                data = file.readlines()

                for line in range(0, len(data) - 2):
                    username = self.search('username', data[line], 'isusername')

                    if username:
                        domain = self.search('domain', data[line + 1], 'isdomain')

                        if domain:
                            password = self.search('password', data[line + 2], 'ispassword')

                            if password:
                                if self.limit and len(password) > self.limit:
                                    password = password[:self.limit] + '***'
                                    self.add_list(username, domain, password)
                                else:
                                    self.add_list(username, domain, password)

                file.close()

            if not self.one_file:
                self.output.give_data(self.list, file_name)
                self.list = []
        if self.one_file:
            self.output.give_data(self.list, 'MimikatzOutput')

    def add_list(self, username, domain, password):
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
            return re.sub(r'{}'.format(self.patterns[pattern]), '', data).rstrip()
        else:
            return False

    @staticmethod
    def detect_files(path):
        if os.path.isfile(path):
            return {path}
        else:
            return os.listdir(path)

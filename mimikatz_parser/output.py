import os
from xml.etree import ElementTree as eTree

import xlsxwriter
import pdfkit


class OUTPUT:
    def __init__(self, args):
        self.path = args.output
        self.type = args.type
        self.file_name = ''
        self.data = []

    def give_data(self, data, file_name):
        self.file_name = file_name.replace(file_name.split('.')[-1], '')
        self.data = data
        if self.type == 'txt':
            self.txt()
        elif self.type == 'pdf':
            self.pdf()
        elif self.type == 'html':
            self.html()
        elif self.type == 'xml':
            self.xml()
        elif self.type == 'excel':
            self.excel()
        else:
            print('Yanlış çıktı türü seçmeye çalıştınız.')

    def excel(self):
        workbook = xlsxwriter.Workbook(os.path.join(self.path, ''.join((self.file_name, 'xlsx'))))
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        worksheet.set_column(0, 0, 25)
        worksheet.set_column(1, 1, 40)
        worksheet.set_column(2, 2, 20)

        worksheet.write('A1', 'UserName', bold)
        worksheet.write('B1', 'Password', bold)
        worksheet.write('C1', 'Domain', bold)

        row = 1
        col = 0

        for username, password, domain in self.data:
            worksheet.write_string(row, col, username)
            worksheet.write_string(row, col + 1, password)
            worksheet.write_string(row, col + 2, domain)
            row += 1

        workbook.close()

        return self.result('xlsx')

    def pdf(self):
        source_html = '<html><body><style>table{' \
                      'border-collapse: collapse;}td,th{font-size:18px;' \
                      'border-bottom: 1px solid black; padding: 5px 10px}' \
                      'td+td{border-left:1px solid black}</style><table>' \
                      '<thead><tr><th><strong>UserName</strong></th><th>' \
                      '<strong>Password</strong></th><th><strong>Domain' \
                      '</strong></th></tr></thead><tbody>'
        for username, password, domain in self.data:
            source_html += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(username, password, domain)
        source_html += '</tbody></table></body></html>'

        pdfkit.from_string(source_html, os.path.join(self.path, ''.join((self.file_name, 'pdf'))))

        return self.result('pdf')

    def html(self):
        source_html = '<html><body><style>table{border-collapse: collapse;}' \
                      'td,th{border-bottom: 1px solid black;padding: 5px ' \
                      '10px}td+td{border-left:1px solid black}</style><table>' \
                      '<thead><tr><th><strong>UserName</strong></th><th>' \
                      '<strong>Password</strong></th><th><strong>Domain' \
                      '</strong></th></tr></thead><tbody>'
        for username, password, domain in self.data:
            source_html += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(username, password, domain)
        source_html += '</tbody></table></body></html>'

        file = open(os.path.join(self.path, ''.join((self.file_name, 'html'))), 'w+b')
        file.write(source_html.encode('utf-8'))
        file.close()

        return self.result('html')

    def txt(self):
        data = 'UserName Password Domain\n'
        for username, password, domain in self.data:
            data += ' '.join((username, password, domain)) + os.linesep
        file = open(os.path.join(self.path, ''.join((self.file_name, 'log'))), 'w+b')
        file.write(data.encode('utf-8'))
        file.close()

        return self.result('log')

    def xml(self):
        from xml.etree import ElementTree as eTree

        root = eTree.Element('AllItems')
        for i in self.data:
            self.add_items(eTree.SubElement(root, 'Item'), i)
        tree = eTree.ElementTree(root)
        tree.write(os.path.join(self.path, ''.join((self.file_name, 'xml'))), xml_declaration=True, encoding='utf-8')

        return self.result('xml')

    def result(self, file_type):
        file = os.path.join(self.path, ''.join((self.file_name, file_type)))
        if os.path.isfile(file) is True:
            print('Dosyanız hazır sizi bekliyor: %s' % file)
        else:
            print('Dosya çıktısında sorun oluştu. İstediğiniz dizinde yazma '
                  'izniniz olduğuna emin olunuz. Eminseniz parser bu defa '
                  'patladı demektir :) Lütfen github\'da issue açarak yardım '
                  'isteyiniz.')

    @staticmethod
    def add_items(root, items):
        elem = eTree.SubElement(root, 'username')
        elem.text = items[0]
        elem = eTree.SubElement(root, 'password')
        elem.text = items[1]
        elem = eTree.SubElement(root, 'password')
        elem.text = items[2]

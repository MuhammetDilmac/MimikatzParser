import os

import xlsxwriter
import pdfkit


class OUTPUT:
    def __init__(self, path, data):
        self.path = path
        self.data = data
        self.filename = 'mimikatz'

    def excel(self):
        workbook = xlsxwriter.Workbook(os.path.join(
            self.path, '.'.join((self.filename, 'xlsx'))))
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
        sourcehtml = '<html><body><style>table{' \
                     'border-collapse: collapse;}td,th{font-size:18px;' \
                     'border-bottom: 1px solid black; padding: 5px 10px}' \
                     'td+td{border-left:1px solid black}</style><table>' \
                     '<thead><tr><th><strong>UserName</strong></th><th>' \
                     '<strong>Password</strong></th><th><strong>Domain' \
                     '</strong></th></tr></thead><tbody>'
        for username, password, domain in self.data:
            sourcehtml += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'. \
                format(username, password, domain)
        sourcehtml += '</tbody></table></body></html>'

        pdfkit.from_string(sourcehtml, os.path.join(self.path, '.'.join(
            (self.filename, 'pdf'))))

        return self.result('pdf')

    def html(self):
        sourcehtml = '<html><body><style>table{border-collapse: collapse;}' \
                     'td,th{border-bottom: 1px solid black;padding: 5px ' \
                     '10px}td+td{border-left:1px solid black}</style><table>' \
                     '<thead><tr><th><strong>UserName</strong></th><th>' \
                     '<strong>Password</strong></th><th><strong>Domain' \
                     '</strong></th></tr></thead><tbody>'
        for username, password, domain in self.data:
            sourcehtml += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'. \
                format(username, password, domain)
        sourcehtml += '</tbody></table></body></html>'

        file = open(os.path.join(self.path, '.'.join(
            (self.filename, 'html'))), 'w+b')
        file.write(sourcehtml.encode('utf-8'))
        file.close()

        return self.result('html')

    def txt(self):
        data = 'UserName Password Domain'
        for username, password, domain in self.data:
            data += '\n' + ' '.join((username, password, domain))
        file = open(os.path.join(self.path, '.'.join(
            (self.filename, 'txt'))), 'w+b')
        file.write(data.encode('utf-8'))
        file.close()

        return self.result('txt')

    def xml(self):
        from xml.etree import ElementTree as eTree

        root = eTree.Element('AllItems')
        for i in self.data:
            self.add_items(eTree.SubElement(root, 'Item'), i)
        tree = eTree.ElementTree(root)
        tree.write(os.path.join(self.path, '.'.join(
            (self.filename, 'xml'))), xml_declaration=True, encoding='utf-8')

        return self.result('xml')

    def result(self, filetype):
        file = os.path.join(self.path, '.'.join((self.filename, filetype)))
        if os.path.isfile(file) is True:
            print('Dosyanız hazır sizi bekliyor: %s' % file)
        else:
            print('Dosya çıktısında sorun oluştu. İstediğiniz dizinde yazma '
                  'izniniz olduğuna emin olunuz. Eminseniz parser bu defa '
                  'patladı demektir :) Lütfen github\'da issue açarak yardım '
                  'isteyiniz.')

    @staticmethod
    def add_items(root, items):
        from xml.etree import ElementTree as eTree

        elem = eTree.SubElement(root, 'username')
        elem.text = items[0]
        elem = eTree.SubElement(root, 'password')
        elem.text = items[1]
        elem = eTree.SubElement(root, 'password')
        elem.text = items[2]

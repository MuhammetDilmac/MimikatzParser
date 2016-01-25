from setuptools import setup

setup(name='Mimikatz Parser',
      version='0.1',
      description='Mimikatz uygulamasının çıktısından kullanıcı adı, parola ve ip bilgisini alıp ardından bu bilgileri \
      txt, html, xml, pdf veya excel formatlarından birinden alabilirsiniz.',
      url='https://github.com/MuhammetDilmac/MimikatzParser',
      author='Muhammet Dilmaç',
      author_email='iletisim@muhammetdilmac.com.tr',
      license='MIT',
      packages=['mimikatz_parser'],
      install_requires=[
          'argparse', 'xlsxwriter', 'pdfkit'
      ],
      scripts=['bin/mimikatzparser'],
      include_package_data=True,
      zip_safe=False)

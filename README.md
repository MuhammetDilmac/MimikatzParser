# MimikatzParser

İnstall
```bash
sudo pip3 install git+https://github.com/MuhammetDilmac/MimikatzParser.git
```
Usage:
```bash
mimikatzparser -i [Input File Or Directory] -o [Output Directory] -t [TYPE{txt, html, xml, pdf, excel}] -l [LIMIT OF PASSWORD CHARACTER] -a [ALL OUTPUT IN ONE FILE(True, False)]
```
Example:
```bash
mimikatzparser -i /home/root/Desktop/example/1.txt -o /home/root/Desktop/ -t excel -l 3
```

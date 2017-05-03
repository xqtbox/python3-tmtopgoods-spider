class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        # 在windows下新文件的默认编码是gbk，需手动改为utf-8
        fout = open('output.html', 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')

        # 表头
        fout.write('<tr>')
        fout.write('<td>公司-车名</td>')
        fout.write('<td>网友评分</td>')
        fout.write('</tr>')


        for data in self.datas:
            fout.write('<tr>')
            # fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td> %s</td>' % data['summary'])
            fout.write('</tr>')

        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')

        fout.close()

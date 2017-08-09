#! /usr/bin/ python
# coding:utf8
'''
输出结果
'''
import os
import pymysql


class HtmlOutputer(object):
    def __init__(self):
        self.datas = [{
            '计算机程序设计语言': 'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E8%AF%AD%E8%A8%80'}]
        # self.datas = [{'计算机程序设计语言': 'https://baike.baidu.com/item%AF%AD%E8%A8%80'}]

    def collect_data(self, new_data):
        if new_data is None:
            return None
        self.datas.append(new_data)

    def save_db(self):
        conn = pymysql.connect(host="localhost", user="root", password="mysql@sl0903", port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute('USE python_baike;')
        # print cur.fetchall()
        # cur.execute('SHOW TABLES;')
        # print cur.fetchall()
        # cur.execute('SHOW DATABASES;')
        # print cur.fetchall()
        cur.execute('SELECT DATABASE();')
        print cur.fetchall()
        table_name = 'baike_python'
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS %s(pid INT(10) NOT NULL AUTO_INCREMENT,
                                                            name VARCHAR(50),
                                                            url TEXT(200),
                                                            PRIMARY KEY(pid));''' % table_name)
        for data_dict in self.datas:
            for title in data_dict.keys():
                url = data_dict[title]
                cur.execute('DELETE FROM %s WHERE name="%s"' % (table_name, title))
                cur.execute('INSERT INTO %s(name,url) VALUES("%s", "%s");' % (table_name, title, url))
        cur.execute('SELECT * FROM %s' % table_name)
        # cur.execute('DELETE FROM %s WHERE pid IS NOT NULL;' % table_name)
        # cur.execute('DROP TABLE IF EXISTS %s;' % table_name)
        # print cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        pass

    def change_code_form(self, str):
        if isinstance(str, unicode):
            str = str.encode('utf8')
        return str

    def output_html(self):
        if self.datas is None:
            return None
        fopen = open(os.path.join(os.getcwd(), 'output/outputer.html'), 'w')
        fopen.write('<html>\n')
        fopen.write('\t<body>\n\t')

        fopen.write('\t<table border="1">\n\t\t')
        fopen.write('\t<tr>\n\t\t\t')
        fopen.write('\t<td>Title</td>\n\t\t\t')
        fopen.write('\t<td>Url</td>\n\t\t')
        fopen.write('\t</tr>\n\t')

        for data_dict in self.datas:
            for title in data_dict.keys():
                fopen.write('\t\t<tr>\n\t\t\t')

                url = data_dict[title]

                fopen.write('\t<td>%s</td>\n\t\t\t' % self.change_code_form(title))
                fopen.write('\t<td ><a target="_blank" href="%s">%s</a></td>\n\t\t' % (url, self.change_code_form(url)))
                fopen.write('\t</tr>\n\t')
        fopen.write('\n')
        fopen.write('\t\t</table>\n')

        fopen.write('\t</body>\n')
        fopen.write('</html>')
        fopen.close()
        pass


if __name__ == '__main__':
    obj = HtmlOutputer()
    obj.save_db()
    pass

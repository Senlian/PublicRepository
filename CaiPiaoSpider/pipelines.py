# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import MySQLdb as db
import scrapy


class CaipiaospiderPipeline(object):
    def process_item(self, item, spider):
        # print item
        # self.save_html(item)
        self.save_db(item)

        return item

    def change_code_form(self, str):
        if isinstance(str, unicode):
            str = str.encode('utf8')
        return str

    def save_db(self, item):
        conn = db.connect(host="localhost", user="root", passwd="mysql@sl0903", port=3306, charset='utf8')
        cur = conn.cursor()
        cur.execute("USE caipiao")
        cur.execute('SELECT DATABASE();')
        # print cur.fetchall()
        table_name = 'ssq'
        cur.execute(
            ''' CREATE TABLE IF NOT EXISTS {0}(
                                 pid INT(100) Not NULL AUTO_INCREMENT,
                                 uid INT(10) NOT NULL DEFAULT 0,
                                 red_one INT(10) NOT NULL DEFAULT 0,
                                 red_two INT(10) NOT NULL DEFAULT 0,
                                 red_three INT(10) NOT NULL DEFAULT 0,
                                 red_four INT(10) NOT NULL DEFAULT 0,
                                 red_five INT(10) NOT NULL DEFAULT 0,
                                 red_six INT(10) NOT NULL DEFAULT 0,
                                 blue INT(10) NOT NULL DEFAULT 0,
                                 link TEXT NOT NULL,
                                 PRIMARY KEY(pid));'''.format(table_name))
        cur.execute("SHOW TABLES;")
        cur.execute(
            '''INSERT INTO {0}(uid,red_one,red_two,red_three,red_four,red_five,red_six,blue,link)
               VALUES({1},{2},{3},{4},{5},{6},{7},{8},'{9}');
            '''.format(table_name, item['uid'], item['red_one'], item['red_two'], item['red_three'], item['red_four'],
                       item['red_five'], item['red_six'], item['blue'], item['link'])
        )
        # print cur.fetchall()
        cur.execute("SELECT * FROM %s;" % table_name)
        # print cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return None
        pass

    def save_html(self, item):
        out_html = os.path.join(os.getcwd(), os.path.basename(os.getcwd()), 'outputer', 'shuangseqiu.html')
        print out_html

        with open(out_html, 'a') as f:
            f.write('<html>\n')

            f.write('\t<head>\n')
            f.write('\t\t<title>福彩双色球开奖记录</title>\n')
            f.write('\t</head>\n')

            f.write('\t<body>\n')
            f.write('\t\t<table border="1">\n')
            f.write('\t\t\t<tr>\n')
            f.write('\t\t\t\t<td>%s</td>\n' % item['id'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['red_one'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['red_two'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['red_three'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['red_four'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['red_five'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['red_six'])
            f.write('\t\t\t\t<td>%s</td>\n' % item['blue'])
            f.write('\t\t\t\t<td><a target="_blank" href=%s>%s</a></td>\n' % (
                item['link'], self.change_code_form(item['link'])))
            f.write('\t\t\t</tr>\n')
            f.write('\t\t</table>\n')
            f.write('\t</body>\n')
            f.write('</html>')
        return out_html
        pass

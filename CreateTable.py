#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author:  Analyst1981@gmail.com
# @date:    2019-02-27
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='toor', db='spiders', charset='utf8')

cursor = db.cursor()
try:
    cursor.execute('DROP TABLE IF EXISTS TestComment')
except:
    print('表TestComment不存在！，直接创建')

else:
    print('原表已删除！')
finally:
    pass

sql = """CREATE TABLE TestComment(
          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增 id',
          nickname VARCHAR(1024) NOT NULL COMMENT '匿名',
          link VARCHAR(1024) NOT NULL COMMENT '链接',
          img_link VARCHAR(1024) NULL NULL COMMENT '图像链接',
          starts VARCHAR(1024) DEFAULT NULL COMMENT '星级',
          _eval VARCHAR(1024) DEFAULT NULL COMMENT '推荐度',
          votes VARCHAR(1024) DEFAULT NULL COMMENT '认可度',
          comments_time VARCHAR(1024) DEFAULT NULL COMMENT '评论时间',
          comments VARCHAR(10000) DEFAULT NULL COMMENT '评论',
          createtime DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间'
          )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试评论表';"""

try:
    cursor.execute(sql)
    db.commit()
    print('已提交')
except:
    print('发生错误,数据回滚')
    db.rollback()

db.close()
print('数据库已关闭')
本项目主要针对拉勾网上数据的爬取：
拉勾网使用的非传统的数据交互技术，ajax--在Ajax.txt 对该技术进行大致说明
diary.log文件 是记录http协议进行文件传输时候的相关记录，访问成功时候访问网址，抛出异常时候记录异常原因（level；error)
https.py --重写post与get 方法
parse.py --数据解析，处理类型是json 格式 而非html 格式
manage.py--主要逻辑实现 文件存储
setting.py--设置请求头header ,cookies 等 具体值可以打开对应网页按键F12,按 F12 查看页面源码，在 NETWORK 标签中可以分析网站的请求响应过程，这里看到 NETWORK 标签下 TYPE XHR 里有 companyAjax.json 和 positionAjax.json 

遇到和解决的问题：
cookies 值不能长时间使用，代码复用时 setting 里面cookies 值需要更新
header 中refer 值也视具体情况更新

频繁爬取页面会出现{‘success’: False, ‘msg’: ‘您操作太频繁,请稍后再访问} 通过设置每一页爬去间隔时间 本项目中为 30s
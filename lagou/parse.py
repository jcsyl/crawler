import re
import demjson

class Parse:
    '''
    解析网页信息
    compile--据包含正则表达式的字符串创建模式对象 re.S 点任意匹配模式
    re.sub(pattern ,repl ,string) example: re.sub(r"hello (\w+),nihao \1","gsc",inputstr)
    '''
    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        self.json = demjson.decode(htmlCode)
        pass# 函数体为空

        #通过正则表达式去掉相关标签 
    def parseTool(self,content):
        '''
        清除html标签
        '''
        if type(content) != str: return content
        sublist = ['<p.*?>','</p.*?>','<b.*?>','</b.*?>','<div.*?>','</div.*?>',
                   '</br>','<br />','<ul>','</ul>','<li>','</li>','<strong>',
                   '</strong>','<table.*?>','<tr.*?>','</tr>','<td.*?>','</td>',
                   '\r','\n','&.*?;','&','#.*?;','<em>','</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error '+str(substring.pattern))
        return content


    def parsePage(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''
        totalCount = self.json['content']['positionResult']['totalCount']      #职位总数量
        resultSize = self.json['content']['positionResult']['resultSize']      #每一页显示的数量
        print("{}_{}".format(totalCount,resultSize))
        pageCount = int(totalCount) // int(resultSize) + 1          #页面数量
        return pageCount


    def parseInfo(self):
        '''
        解析信息
        '''
        info = []
        for position in self.json['content']['positionResult']['result']:
            i = {}
            i['companyName'] = position['companyFullName']
            i['companyDistrict'] = position['district']
            i['companyLabel'] = position['companyLabelList']
            i['companySize'] = position['companySize']
            i['companyStage'] = position['financeStage']
            i['companyType'] = position['industryField']
            i['positionType'] = position['firstType']
            i['positionEducation'] = position['education']
            i['positionAdvantage'] = position['positionAdvantage']
            i['positionSalary'] = position['salary']
            i['positionWorkYear'] = position['workYear']
            info.append(i)
        return info








from https import Http
from parse import Parse
from setting import headers as hd
from setting import cookies as ck
import time
import logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=hd, cookies=ck)
    generalParse = Parse(htmlCode)

    pageCount = generalParse.parsePage()
    print(pageCount)
    info = []
    for i in range(1, pageCount+1):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=hd, cookies=ck)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        time.sleep(30)
    return info


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info


def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        title = 'companyName,companyType,companyStage,companyLabel,companySize,companyDistrict,' \
                'positionType,positionEducation,positionAdvantage,positionSalary,positionWorkYear\n'
        file = open('广州.txt', 'a',)
        file.write(title)
        for p in info:
            line = str(p['companyName']) + ',' + str(p['companyType']) + ',' + str(p['companyStage']) + ',' + \
                   str(p['companyLabel']) + ',' + str(p['companySize']) + ',' + str(p['companyDistrict']) + ',' + \
                   str(p['positionType']) + ',' + str(p['positionEducation']) + ',' + str(p['positionAdvantage']) + ',' +\
                   str(p['positionSalary']) + ',' + str(p['positionWorkYear']) + '\n'
            file.write(line)
        file.close()
        return True
    except:
        logging.error('Process except')
        return None


def main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        info = getInfo(url, para)             # 获取信息
        flag = processInfo(info, para)             # 信息储存
        return flag
    else:
        return None


if __name__ == '__main__':
    kdList = [u'数据挖掘']
    cityList = ['广州']
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false&isSchoolJob=0'
    for city in cityList:
        print('爬取%s' % city)
        para = {'first': 'True','pn': '1', 'kd': kdList[0]}
        flag = main(url, para)
        if flag: print('%s爬取成功' % city)
        else: print('%s爬取失败' % city)

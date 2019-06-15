import requests
import time
import hashlib
import json
import re
from http import cookiejar
last={}
something3={}
fakechaoxing={}
def get_course():
    print("正在获取课程")
    header={'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh_CN',
            'Host': 'mooc1-api.chaoxing.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_1969814533'
        }
    my_course=ses.get("http://mooc1-api.chaoxing.com/mycourse?rss=1&mcode=",headers=header)
    result=my_course.json()
    channelList=result['channelList']
    channelList_json=channelList[0]
    content=channelList_json['content']
    fakechaoxing['urlcpi']=channelList_json['cpi']
    course=content['course']
    data=course['data']
    data_json=data[0]
    print("课程名称:"+data_json['name'])
    print("讲师："+data_json['teacherfactor'])
    something3['clazzid']=content['id']
    something3['courseid']=data_json['id']
    fakechaoxing['clazzid']=content['id']
    get_lesson(content['id'])
    


def get_lesson(content_id):
    print("正在获取章节")
    header={'User-agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_1969814533',
            'contentType': 'utf-8',
            'Accept-Language': 'zh_CN',
            'Host': 'mooc1-api.chaoxing.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
    url='http://mooc1-api.chaoxing.com/gas/clazz?id='+str(content_id)+'&fields=id,bbsid,classscore,allowdownload,isstart,chatid,name,state,isthirdaq,information,discuss,visiblescore,begindate,course.fields(id,infocontent,name,objectid,classscore,bulletformat,imageurl,privately,teacherfactor,unfinishedJobcount,jobcount,state,knowledge.fields(id,name,indexOrder,parentnodeid,status,layer,label,begintime,attachment.fields(id,type,objectid,extension,name).type(video)))&view=json'
    my_lesson=ses.get(url,headers=header)
    result=my_lesson.json()
    data=result['data']
    data_json=data[0]
    course=data_json['course']
    data2=course['data']
    data2_json=data2[0]
    knowledge=data2_json['knowledge']
    data3=knowledge['data']
    ids={}
    for i in data3:
        if i['parentnodeid']!=0 :
            print(str(i['label'])+"  "+i['name'])
    for i in data3:
        ids[i['label']]=i['id']
    num=input("请输入序号:")
    something3['knowledgeid']=ids[num]
    fakechaoxing['nodeId']=ids[num]
    get_something(ids[num],data2_json['id'])
    




def get_something(lesson_id,course_id):
    url='http://mooc1-api.chaoxing.com/gas/knowledge?id='+str(lesson_id)+'&courseid='+str(course_id)+'&fields=begintime,clickcount,createtime,description,indexorder,jobUnfinishedCount,jobcount,jobfinishcount,label,lastmodifytime,layer,listPosition,name,openlock,parentnodeid,status,id,card.fields(cardIndex,cardorder,description,knowledgeTitile,knowledgeid,theme,title,id).contentcard(all)&view=json'
    header={
        'Accept-Language': 'zh_CN',
        'Host': 'mooc1-api.chaoxing.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_19698145335.21'

        }
    req=ses.get(url,headers=header)
    result=req.text
    objectId=re.search(r'objectid&quot;:&quot;([0-9a-f]{32})',result).group(1)
    last['objectId']=objectId
    fakechaoxing['objectId']=objectId
    jobid=re.search(r'jobid&quot;:([0-9]{13})',result).group(1)
    fakechaoxing['jobid']=jobid
    cookie=requests.utils.dict_from_cookiejar(ses.cookies)
    fid=cookie['fid']
    fakechaoxing['userid']=cookie['_uid']
    get_something2(objectId,fid)



def get_something2(objectId,fid):
    url='http://mooc1-api.chaoxing.com/ananas/status/'+objectId+'?k='+str(fid)+'&flag=normal&_dc='+str(time.time()*1000)
    header={
        'Host': 'mooc1-api.chaoxing.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_19698145335.21',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        }
    req=ses.get(url,headers=header)
    result=req.json()
    fakechaoxing['dtoken']=result['dtoken']
    fakechaoxing['duration']=result['duration']
    get_something3()




def get_something3():
    url='http://mooc1-api.chaoxing.com/knowledge/cards?clazzid='+str(something3['clazzid'])+'&courseid'+str(something3['courseid'])+'&knowledgeid='+str(something3['knowledgeid'])+'&num=2&isPhone=1&control=true'
    header={
        'Host': 'mooc1-api.chaoxing.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_19698145335.21',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.chaoxing.mobile'
        }
    req=ses.get(url,headers=header)
    fake_chaoxing()





def get_enc():
    encrypt_enc="[" + str(fakechaoxing['clazzid']) + "][" + str(fakechaoxing['userid']) + "][" + str(fakechaoxing['jobid']) + "][" + fakechaoxing['objectId'] + "][" + str((fakechaoxing['duration'])*1000) + "][" + "d_yHJ!$pdA~5" + "][" + str(fakechaoxing['duration']*1000) + "][" +"0_"+ str(fakechaoxing['duration']) + "]"
    md51=hashlib.md5()
    md51.update(encrypt_enc.encode('utf-8'))
    enc=md51.hexdigest()
    fakechaoxing['enc']=enc




def fake_chaoxing():
    get_enc()
    urls='http://mooc1-api.chaoxing.com/multimedia/log/a/'+str(fakechaoxing['urlcpi'])+'/'+fakechaoxing['dtoken']+'?otherInfo=nodeId_'+str(fakechaoxing['nodeId'])+'&playingTime='+str(fakechaoxing['duration'])+'&duration='+str(fakechaoxing['duration'])+'&akid=null&jobid='+str(fakechaoxing['jobid'])+'&clipTime=0_'+str(fakechaoxing['duration'])+'&clazzId='+str(fakechaoxing['clazzid'])+'&objectId='+fakechaoxing['objectId']+'&userid='+str(fakechaoxing['userid'])+'&isdrag=2&enc='+fakechaoxing['enc']+'&dtype=Video&view=json'
    header={
        'Accept-Language': 'zh_CN',
        'Host': 'mooc1-api.chaoxing.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_19698145335.21'

        }
    req=ses.get(urls,headers=header)
    result=req.json()
    print(result['isPassed'])
    



    
    
uname=input("请输入账号：")
upwd=input("请输入密码：")
header={'Accept-Language': 'zh_CN',
        'Content-Type': 'multipart/form-data; boundary=vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6',
        'Host': 'passport2.chaoxing.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G9350 Build/LMY48Z) com.chaoxing.mobile/ChaoXingStudy_3_5.21_android_phone_206_1 (SM-G9350; Android 5.1.1; zh_CN)_1969814533'
        }
data=[]
data.append('--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\n')
data.append('Content-Disposition: form-data; name="uname"\r\n')
data.append('Content-Type: text/plain; charset=UTF-8\r\n')
data.append('Content-Transfer-Encoding: 8bit\r\n')
data.append('\r\n')
data.append(uname+'\r\n')
data.append('--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\n')
data.append('Content-Disposition: form-data; name="code"\r\n')
data.append('Content-Type: text/plain; charset=UTF-8\r\n')
data.append('Content-Transfer-Encoding: 8bit\r\n')
data.append('\r\n')
data.append(upwd+'\r\n')
data.append('--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\n')
data.append('Content-Disposition: form-data; name="loginType"\r\n')
data.append('Content-Type: text/plain; charset=UTF-8\r\n')
data.append('Content-Transfer-Encoding: 8bit\r\n')
data.append('\r\n')
data.append('1\r\n')
data.append('--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6\r\n')
data.append('Content-Disposition: form-data; name="roleSelect"\r\n')
data.append('Content-Type: text/plain; charset=UTF-8\r\n')
data.append('Content-Transfer-Encoding: 8bit\r\n')
data.append('\r\n')
data.append('true\r\n')
data.append('--vfV33Hae5dKmSaPrHidgXv4ZK-3gOyNn-jid8-6--\r\n')
datas=''
for i in data :
    datas+=i
m_time=int(time.time()*1000)
m_token='4faa8662c59590c6f43ae9fe5b002b42'
m_encrypt_str='token='+m_token+'&_time='+str(m_time)+'&DESKey=Z(AfY@XS'
md5=hashlib.md5()
md5.update(m_encrypt_str.encode('utf-8'))
m_inf_enc=md5.hexdigest()
post_url='http://passport2.chaoxing.com/xxt/loginregisternew?'+'token='+m_token+'&_time='+str(m_time)+'&inf_enc='+m_inf_enc
ses=requests.session()
req=ses.post(post_url,data=datas,headers=header)
result=req.json()

print(result['mes'])
if(result['status']):
    get_course()

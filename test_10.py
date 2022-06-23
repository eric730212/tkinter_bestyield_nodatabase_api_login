import requests
import json


my_data = {"system": "WebActHp",
           "Username": 'TST410',
           "Password": '0410'
           }

Head = {'Content-Type': 'application/json'}
x = requests.post('https://byteiotapi.bestyield.com/signin', headers=Head, data=json.dumps(my_data))
print(x.status_code)
token = x.text




totalList = ['NY112233','123','456']
totalList = ['NY112233']
my_data1 = {"snList": totalList}
my_data1 = {'snList':'NYYYYYYYYYY'}
my_files = {'file': open('C:\\HP_LOG\\PK2\\20220622\\test3.png','rb')}


y = requests.post('https://byteiotapi.bestyield.com/api/Act18/%s/%s' % ('test003', '500'),  # 上傳
                  headers={'Authorization': 'Bearer ' + token},
                  files=my_files, data=my_data1)
print('y.status_code:',y.status_code)
print('y.text:',y.text)
print('my_data1:',my_data1)

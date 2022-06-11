
import json
with open('payment.json','r') as f:
        data = json.load(f)


temp={}
for i in data:
    if(i.get('cid',None)!=None):
        temp.update({i['id']:i['cid']})


def look_up(id):
    return temp.get('cid')
    

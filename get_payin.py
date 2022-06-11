import requests
from requests.structures import CaseInsensitiveDict
import json
from lookup_cid import look_up
def get_payin(a,b):
    l1 = razorpay_in(a,b)
    l2 =cashfree(a,b)
    return l1+l2
def razorpay_in(start,end):
    cash_in=[]
    razorpayin_list = []
    skip = 0
    new_results = True
    url = "https://api.pharmacyone.io/prod/rzp_transaction"
    headers = CaseInsensitiveDict()
    headers["session-token"] = "wantednote"
    while new_results: 
        params_dict = {'skip' : str(skip), 'from' : str(start), 'to' : str(end)}
        response = requests.get(url, params=params_dict, headers=headers)
        dict_data = response.json() 
        if 'data' in dict_data:
            new_results = dict_data.get("data").get("items", [])
        razorpayin_list.extend(new_results)
        skip = int(skip) + 100
    for item in razorpayin_list:
        cid = item.get('source').get('notes').get('cid')
        amt_in_paise = item.get('source').get('amount')
        amt = amt_in_paise * 0.01
        cash_in.append({'cid':cid,'amount':amt})
    return cash_in


def cashfree(start,end):
    temp=[]
    cashfree_list = []
    lastReturnId = 0
    new_results = True
    url = "https://api.pharmacyone.io/prod/cf_payments"
    headers = CaseInsensitiveDict()
    headers["session-token"] = "wantednote"
    while new_results: 
        headers["Content-Type"] = "application/json"
        ## convert dictionary data into string using json.dumps
        data = json.dumps({"startDate": start, "endDate": end,"lastReturnId" : lastReturnId})
        response = requests.post(url, headers=headers, data=data)
        cf_dict = response.json()
        if 'data' in cf_dict:
            new_results = cf_dict.get("data").get("payments", [])
            if 'lastReturnId' in cf_dict['data']:
                lastReturnId = cf_dict['data']['lastReturnId']
        cashfree_list.extend(new_results)
    for i in cashfree_list:
        cid =look_up(i.get('referenceId'))
        amt =i.get('amount',None)
        temp.append({'cid':cid,'amt':amt})
    return temp
import json
import requests
from requests.structures import CaseInsensitiveDict
from collections import Counter
import argparse
import datetime
from Tally_io import tally
from get_payin import get_payin

def settlement_id_call(settlement_id,start,end):
    temp=[]
    settlement_list = []
    url = f"https://api.pharmacyone.io/prod/settlement_transaction/{settlement_id}"
    headers = CaseInsensitiveDict()
    headers["session-token"] = "wantednote"
    response = requests.get(url, headers=headers)
    dict_data = response.json() 
    if 'data' in dict_data:
        new_results = dict_data.get("data").get("items", [])
    settlement_list.extend(new_results)
    for i in settlement_list:
        if(start <i['createdOn'] < end ):
            temp.append({'cid':i['cid'],'amount':i['amount']})
    return temp

    # settlement_dict = {item['id'] : item for item in settlement_list}
    # return settlement_dict


def make_razor_po_call(start,end):
    cash_out=[]
    razorpout_list = []
    skip = 0
    new_results = True
    url = "https://api.pharmacyone.io/prod/rzp_payout"
    headers = CaseInsensitiveDict()
    headers["session-token"] = "wantednote"
    while new_results: 
        params_dict = {'skip' : str(skip),'from' : str(int(start)),'to' : str(int(end))}
        response = requests.get(url, params=params_dict, headers=headers)
        dict_data = response.json() 
        
        if 'data' in dict_data:
            new_results = dict_data.get("data").get("items", [])
        razorpout_list.extend(new_results)
        skip = int(skip) + 100
    for item in razorpout_list:
        if(item.get('source') and item.get('source').get('notes')):
            if(item.get('source').get('notes').get('type',None) == 'settlement'):
                a =settlement_id_call(item.get('source').get('notes').get('id'),start,end)
                
            else:
                cid = item.get('source').get('notes').get('cid')
                amt_in_paise = item.get('source').get('amount')
                amt = amt_in_paise * 0.01
                cash_out.append({'cid':cid,'amount':amt})

    return cash_out+a

     

if __name__=="__main__":
     #take the date as input and calculate time for window of transactions
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_time",type=str,required=True)
    # parser.add_argument('--end_time',type=str)

    args = parser.parse_args()
    
    date1 = args.start_time.split("/") 
    y, m, d = date1
    start_time = datetime.datetime(int(y),int(m),int(d),int(0),int(0),int(0)).timestamp()
    end_time = datetime.datetime(int(y),int(m),int(d),23,59,59).timestamp()

    payout=make_razor_po_call(start_time,end_time)
    payin = get_payin(start_time,end_time)
    tally(payin,payout)
    
    

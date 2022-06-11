from collections import Counter

cash_in=[]
cash_out=[]
def tally(cash_in,cash_out):
    print(len(cash_in))
    list_cids_in=[]

    for i in cash_in:
        if(i['cid']!=None):
            list_cids_in.append(i['cid'])
    print(len(set(list_cids_in)))
    list_cids_out=[]
    print(cash_out)
    for i in cash_out:
        if(i['cid'] !=None):
            list_cids_in.append(i['cid'])
    print(len(set(list_cids_out)))
    

    
    
    
    # temp=[]
    # for i in cash_in:
    #     temp.append(i['cid'])
    
    # s =list(set(temp))
    # for i in s:
    #     if(i):
    #         total_of_pharma_cash_in(i.get('cid',None))
    #         total_of_pharma_cash_out(i.get('cid',None))
    
    
    
    # c= Counter(company_total_cash_in)
    # print(c)
    # d= Counter(company_total_cash_out)
    # print(d)

    # pharmas_we_paid_more = d - c
    # pharmas_we_paid_less = c-d
    # return pharmas_we_paid_less,pharmas_we_paid_more

# both are  list of dicts with dict two parameters cid and amount
company_total_cash_in={}
def total_of_pharma_cash_in(cid):
    tot =0
    for item in cash_in:
        if(item['cid']==cid):
            tot += item['amount']
    return company_total_cash_in.update({cid:tot})

company_total_cash_out={}
def total_of_pharma_cash_out(cid):
    tot =0
    for item in cash_out:
        if(item['cid']==cid):
            tot += item['amount']
    
    return company_total_cash_out.update({cid:tot})



# the companies in the result are the amount we extra paid to companies




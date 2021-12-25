from GetClient import client

info = client.get_account()
for i in info['balances']:
    if(float(i['free']) != 0.0):
        print(i)
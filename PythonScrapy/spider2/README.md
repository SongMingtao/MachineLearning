##[彩客网](http://vip.win007.com/Europe100.asp) Spider

this is spider for collecting [彩客网](http://vip.win007.com/Europe100.asp)'s historical data

for store data, you can change spider.py get_detail_datta()
method, and just now, it only print some info. you can overwrite
this, for example:
```
def get_detail_data(url):
    global count
    try:
        response = requests.get(url=url, headers=get_header())
        # print(response.text)
        print("**********")
        print(response.status_code)
        
        '''store data  for example you have a method call 
        store_data(response) just add here
        
        '''
        store_data(response.text)
        
        if count_lock.acquire():
            count += 1
            print("Total is %d " % count)
            end_time = time.time()
            tt = end_time - start_time
            print("Time:\nHave been run is %f seconds" % (tt))
            print("Avage %f \n" % (tt / count))
            count_lock.release()
    except Exception:
        return
```
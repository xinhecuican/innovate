import re
import requests
import time
import random

def get_content():
    headers = {
            'Referer': 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.173.2d324edc7BaCKr&id=591671671551&ns=1&abbucket=9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'cookie':"hng=CN%7Czh-CN%7CCNY%7C156; t=0a235e1c5cecc207bdf0bff22face3aa; thw=cn; UM_distinctid=1734540107155e-036af6631e4db5-4353760-144000-17345401072b0e; _m_h5_tk=77166abaac2977751769e89783cd6207_1594893024428; _m_h5_tk_enc=9d78621860d00260d427d2bf81c5835b; sgcookie=EI9w9wp2%2FVoqB8WGp1eRN; lLtC1_=1; enc=CNO7c%2BLTmtnCNFdfSsC%2Bs7nKr8iHxK6%2FSAj5n2Xb1v%2BY0JUyDimBTkrU0X0ePK3wSYB%2FXtdS6%2B4BpI41plc3YHoN%2BpCTd6VeS%2BfZqH9RYpA%3D; cookieCheck=59197; cookie2=1533bb55baffe9cebc1928619b11c204; _tb_token_=eeb367e19b761; XSRF-TOKEN=bd564a00-d6ae-44f5-a2ef-7a456166cb00; _samesite_flag_=true; mt=ci=0_0; tracknick=; cna=YZWQFvti82MCAXWINmEi6+ua; l=eBLugqdcQcg2Y0Z6BO5Zhurza77tFIRf1RVzaNbMiInca6TRtFTuENQqHAWXSdtjgtfAyExrb3kJjRUB7fU38x1Hrt7APlUOrxv9-; isg=BJWVwvxbZsSJ6kNUN0XbjmH2pJFPkkmkRIouMBc69oxbbrZg0eHbdc1oOHJY12Fc; tfstk=c8XdBAmVUP4HzrtO06FMPf4fBAZcZYoprDT-euAUssN4t9kRiEBcHTAuO3upBlC.."
            }

    url = 'https://rate.taobao.com/feedRateList.htm?'

    query_params = {
            'auctionNumId': '613382430211',
            'userNumId': '17879873736',
            'currentPageNum': '1',
            'pageSize': '20',
            'rateType': '',
            'orderType': 'sort_weight',
            'attribute': '',
            'sku': '',
            'hasSku': 'false',
            'folded': '0',
            'ua': 'hng=CN%7Czh-CN%7CCNY%7C156; t=0a235e1c5cecc207bdf0bff22face3aa; thw=cn; UM_distinctid=1734540107155e-036af6631e4db5-4353760-144000-17345401072b0e; _m_h5_tk=77166abaac2977751769e89783cd6207_1594893024428; _m_h5_tk_enc=9d78621860d00260d427d2bf81c5835b; lLtC1_=1; cookie2=1533bb55baffe9cebc1928619b11c204; _tb_token_=eeb367e19b761; XSRF-TOKEN=bd564a00-d6ae-44f5-a2ef-7a456166cb00; _samesite_flag_=true; cookieCheck=67980; sgcookie=Evao0gYlAAzBk94FtuqLY; enc=EWZw35bYZvX1i%2FqRRRiaARmG5UkFTH8jsxk73HgcddFa8%2FX6iRcwZasgBSlGFsN5Z%2F5msRiIkiQlykJcMmgj8QToGgaGnIrgQ2ZMv3fuiPE%3D; mt=ci=0_0; tracknick=; cna=YZWQFvti82MCAXWINmEi6+ua; l=eBLugqdcQcg2YyCjBOfZPurza77O-IR0IuPzaNbMiOCPOefH5T9lWZkxWJ8MCnGVnsBJk3ow4YKgBf8idy4Eh6Yl3ZQ7XPQondLh.; isg=BKioBQb1Y1u29k6zoma-oWxFeZa60Qzbufnjl2LZtCMWvUsnB-KpakW7tVVNtMSz; tfstk=cWC5BrwGx0m5lFwEaaa24bjrgQRFZzrXo8tRPtygwLLLUgQ5iWcwfjdfKmcvBE1..',
            '_ksTS': '1563849303999_1462',
            'callback': 'jsonp_tbcrate_reviews_list'
            }
    for i in range(1, 100):
        query_params['currentPageNum'] = i
        response = requests.get(url=url, headers=headers, params=query_params).text
        contents = re.compile(',"content":"(.*?)"').findall(response)
        if(contents == []):
            break
        for content in contents:
            print(content)
        time.sleep(random.uniform(5, 10))
get_content()
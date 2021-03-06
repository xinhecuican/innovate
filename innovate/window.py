import json

import wx
import requests
from bs4 import BeautifulSoup
import bs4
import re
import time
import random
import threading
import os
import webbrowser




class commit_thread(threading.Thread):
    def __init__(self, itemId, commitarea, statictext):
        threading.Thread.__init__(self)
        self.itemId = itemId
        self.commitarea = commitarea
        self.end_flag = False
        self.start_flag = False
        self.static_text = statictext
        self.min_time = 5
        self.max_time = 10

    def setitemId(self, itemId):
        self.itemId= itemId
    def setcommitarea(self, commitarea):
        self.commitarea = commitarea

    def run(self):
        self.start_flag = True
        headers = {
            'Referer': 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.173.2d324edc7BaCKr&id=591671671551&ns=1&abbucket=9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'cookie': "hng=CN%7Czh-CN%7CCNY%7C156; t=0a235e1c5cecc207bdf0bff22face3aa; thw=cn; UM_distinctid=1734540107155e-036af6631e4db5-4353760-144000-17345401072b0e; _m_h5_tk=77166abaac2977751769e89783cd6207_1594893024428; _m_h5_tk_enc=9d78621860d00260d427d2bf81c5835b; sgcookie=EI9w9wp2%2FVoqB8WGp1eRN; lLtC1_=1; enc=CNO7c%2BLTmtnCNFdfSsC%2Bs7nKr8iHxK6%2FSAj5n2Xb1v%2BY0JUyDimBTkrU0X0ePK3wSYB%2FXtdS6%2B4BpI41plc3YHoN%2BpCTd6VeS%2BfZqH9RYpA%3D; cookieCheck=59197; cookie2=1533bb55baffe9cebc1928619b11c204; _tb_token_=eeb367e19b761; XSRF-TOKEN=bd564a00-d6ae-44f5-a2ef-7a456166cb00; _samesite_flag_=true; mt=ci=0_0; tracknick=; cna=YZWQFvti82MCAXWINmEi6+ua; l=eBLugqdcQcg2Y0Z6BO5Zhurza77tFIRf1RVzaNbMiInca6TRtFTuENQqHAWXSdtjgtfAyExrb3kJjRUB7fU38x1Hrt7APlUOrxv9-; isg=BJWVwvxbZsSJ6kNUN0XbjmH2pJFPkkmkRIouMBc69oxbbrZg0eHbdc1oOHJY12Fc; tfstk=c8XdBAmVUP4HzrtO06FMPf4fBAZcZYoprDT-euAUssN4t9kRiEBcHTAuO3upBlC.."
        }

        url = 'https://rate.taobao.com/feedRateList.htm?'

        query_params = {
            'auctionNumId': self.itemId,
            'userNumId': '15022287670',
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
            last_content = ''
            if (contents == []):
                break
            if(self.end_flag == True):
                break
            for content in contents:
                if(content == '此用户没有填写评价。' or last_content == content):
                    continue
                self.commitarea.AppendText(content + '\n')
                last_content = content
            time.sleep(random.uniform(self.min_time, self.max_time))
        self.end_flag = False
        self.static_text.SetLabelText('已结束')
        self.start_flag = False



class my_frame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="差评原因", size=(1000, 600))
        self.Centre()
        panel = wx.Panel(parent=self)
        sizer_root = wx.BoxSizer(wx.VERTICAL)


        sizer1 = wx.GridBagSizer(100, 100)
        self.text1 = wx.StaticText(panel, label='请输入网页链接', style=wx.ST_ELLIPSIZE_MIDDLE)
        font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.text1.SetFont(font)

        self.textarea1 = wx.TextCtrl(panel)
        self.textarea1.SetBackgroundColour(wx.Colour((200, 221, 242)))

        button_confirm = wx.Button(panel, label='提交')
        self.Bind(wx.EVT_BUTTON, self.Button_confirm, button_confirm) # bind

        sizer1.Add(self.text1, pos=(0, 0), span=(1,1), flag=wx.EXPAND | wx.BOTTOM)
        sizer1.Add(self.textarea1, flag=wx.EXPAND, pos=(0, 1), span=(1,5))
        sizer1.Add(button_confirm, pos=(0, 6), span=(1, 1))
        sizer1.AddGrowableCol(1, 1)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.CommitArea = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL) # 主体评论区
        sizer2.Add(self.CommitArea,proportion=1, flag=wx.EXPAND)



        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.static_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        sizer3.Add(self.static_text, proportion=2, flag=wx.EXPAND)

        '''sizer4 = wx.GridBagSizer(2, 2)
        button_submit = wx.Button(panel, label='提交')
        #self.Bind(wx.EVT_BUTTON, self.Login, button_submit)
        login = wx.TextCtrl(panel)
        password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        login_text = wx.StaticText(panel, label='账号')
        password_text = wx.StaticText(panel, label='密码')
        sizer4.Add(login_text, border=10, flag=wx.RIGHT, pos=(0, 0), span=(1, 1))
        sizer4.Add(login, border=10, flag=wx.RIGHT, pos=(0, 1), span=(1, 1))
        sizer4.Add(password_text, pos=(0, 2), span=(1, 1))
        sizer4.Add(password, border=10, pos=(0, 3), span=(1, 1), flag=wx.LEFT | wx.RIGHT)
        sizer4.Add(button_submit, pos=(0, 4), span=(1, 1))'''

        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        button_end = wx.Button(panel, label='停止')
        self.Bind(wx.EVT_BUTTON, self.End_thread, button_end)
        sizer5.Add(button_end)

        sizer6 = wx.MenuBar()
        menu_setting = wx.Menu()
        menu_help = wx.Menu()
        setting_speed = wx.MenuItem(menu_setting, 101, '设置爬取每页时间', '', wx.ITEM_NORMAL)
        setting_help = wx.MenuItem(menu_help, 201, '常见问题', '', wx.ITEM_NORMAL)
        menu_setting.AppendItem(setting_speed)
        menu_help.AppendItem(setting_help)
        sizer6.Append(menu_setting, '设置')
        sizer6.Append(menu_help, '帮助')
        self.Bind(wx.EVT_MENU, self.Onclick)

        self.thread = commit_thread('', self.CommitArea, self.static_text)


        sizer_root.Add(sizer1, border=20, flag=wx.ALL | wx.EXPAND)
        #sizer_root.Add(sizer4, border=10, flag=wx.ALL)
        sizer_root.Add(sizer5, flag=wx.EXPAND)
        sizer_root.Add(sizer2, proportion=2, flag=wx.ALIGN_LEFT | wx.EXPAND)
        sizer_root.Add(sizer3, flag=wx.EXPAND)
        panel.SetSizer(sizer_root)
        self.SetMenuBar(sizer6)
        self.read_config()

    def End_thread(self, e):
        self.thread.end_flag = True

    def Onclick(self, e):
        num = e.GetId()
        if(num == 101):
            speed_frame = wx.Frame(self, size=(300, 200))
            speed_panel = wx.Panel(speed_frame)
            sizer_speed = wx.GridBagSizer(3, 3)
            speed_static_text = wx.StaticText(speed_panel, label='最短时间')
            speed_static_text_maxtime = wx.StaticText(speed_panel, label='最长时间')
            self.speed_text_min = wx.TextCtrl(speed_panel, value=str(self.thread.min_time))
            self.speed_text_max = wx.TextCtrl(speed_panel, value=str(self.thread.max_time))
            speed_button = wx.Button(speed_panel, label='提交')
            speed_frame.Bind(wx.EVT_BUTTON, self.SetSpeed, speed_button)
            sizer_speed.Add(speed_static_text, pos=(0, 0), span=(1, 1))
            sizer_speed.Add(self.speed_text_min, pos=(0, 1), span=(1, 1))
            sizer_speed.Add(speed_static_text_maxtime, pos=(1, 0), span=(1, 1))
            sizer_speed.Add(self.speed_text_max, pos=(1, 1), span=(1, 1))
            sizer_speed.Add(speed_button, pos=(2, 0), flag=wx.ALIGN_CENTER)

            speed_panel.SetSizer(sizer_speed)
            speed_frame.Centre()

            speed_frame.Show()
        elif(num == 201):
            webbrowser.open(os.path.realpath("help.html"), new=0, autoraise=True)




    def SetSpeed(self, e):
        min = self.speed_text_min.GetValue()
        max = self.speed_text_max.GetValue()
        if(type(eval(min)) != int):
            self.static_text.SetLabelText('请输入数字')
            return
        if(type(eval(max)) != int):
            self.static_text.SetLabelText('请输入数字')
            return

        self.thread.min_time = eval(min)
        self.thread.max_time = eval(max)
        status = {"min_time":eval(min), "max_time":eval(max)}
        ans = json.dumps(status, indent=4, ensure_ascii=False)
        with open("config.json", 'w', encoding='utf-8') as f:
            f.write(ans)



    def Button_confirm(self, e):
        if(self.thread.start_flag == False):
            url = self.textarea1.GetValue()
            if(url == ''):
                return
            kv = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
            status_code = -1
            try:
                r = requests.get(url, headers=kv, timeout=20)
                status_code = r.status_code
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                self.read_html(r.text)
            except:
                if(status_code == -1):
                    self.static_text.SetLabelText('抱歉，操作过于频繁，淘宝君承受不住呢')
                else:
                    self.static_text.SetLabelText("无法正常获得网页，状态码{}".format(status_code))
            finally:
                e.Skip()
        else:
            self.static_text.SetLabelText('请不要多次点击')

    def read_html(self, text):
        try:
            itemid_text = re.search(r'itemId=\d+\.?\d*', text)
            itemId = itemid_text.group(0).split('=')[1]
            self.thread.setitemId(itemId)
            self.thread.start()
        except:
            self.static_text.SetLabelText('无法解析网页')

    def read_config(self):
        text = ''
        with open('config.json', 'r') as f:
            text = f.read()
        res = json.loads(text)
        if(type(res['min_time']) != int or type(res['max_time']) != int):
            return
        self.thread.min_time = res['min_time']
        self.thread.max_time = res['max_time']



class app(wx.App):
    def OnInit(self):
        frame = my_frame()
        frame.Show()
        return True

    def OnExit(self):
        return 0


if __name__ == '__main__':
    app = app()
    app.MainLoop()
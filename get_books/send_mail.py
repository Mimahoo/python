#coding:utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import MySQLdb


conn=MySQLdb.connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='lcklbc1010',
	db='books'	
	)

cur=conn.cursor()


def _format_addr(s):
	name, addr=parseaddr(s)
	return formataddr((Header(name,'utf-8').encode(),addr.encode('utf-8') if isinstance(addr,unicode) else addr))


from_addr='xiangyongjiang1118@163.com'
password='xyjLOVE1996'
smtp_server ='smtp.163.com'
to_addr='563868273@qq.com'
n=cur.execute('select * from book_info where vote>500 limit 1')
if n==0:
	print 'no book information!'

book=cur.fetchone()
if book[1]=='':
	sm=''
else:
	sm='<span><span class="pl"> 书名</span>:%s</span><br>' %book[1]
if book[2]=='':
	zz=''
else:
	zz='<span><span class="pl"> 作者</span>:%s</span><br>' %book[2]
if book[3]=='':
	cbs=''
else:
	cbs='<span><span class="pl"> 出版社</span>:%s</span><br>' %book[3]
if book[4]=='':
	yzm=''
else:
	yzm='<span><span class="pl"> 原作名</span>:%s</span><br>' %book[4]
if book[5]=='':
	yz=''
else:
	yz='<span><span class="pl"> 译者</span>:%s</span><br>' %book[5]
if book[6]=='':
	cbn=''
else:
	cbn='<span><span class="pl"> 出版年</span>:%s</span><br>' %book[6]
if book[7]=='':
	ys=''
else:
	ys='<span><span class="pl"> 页数</span>:%s</span><br>' %book[7]
if book[8]=='':
	dj=''
else:
	dj='<span><span class="pl"> 定价</span>:%s</span><br>' %book[8]
if book[9]=='':
	zd=''
else:
	zd='<span><span class="pl"> 装帧</span>:%s</span><br>' %book[9]
if book[0]=='':
	isbn=''
else:
	isbn='<span><span class="pl"> ISBN</span>:%s</span><br>' %book[0]
if book[10]=='':
	score=''
else:
	score='<span><span class="pl"> 豆瓣评分</span>:%s</span><br>' %book[10]
if book[11]=='':
	vote=''
else:
	vote='<span><span class="pl"> 评分人数</span>:%s</span><br>' %book[11]

m=cur.execute('select * from websites where id=%s' %book[13])
#more=list()
#if m==1:
#	more=cur.fetchone()
	
#more='<span><a href="%s"> 更多信息</a></span><br>' %more[1]
	
msg=MIMEMultipart()
msg.attach(MIMEText('<div class="subject clearfix"><div id="mainpic" class=""><img src="cid:0" style="width: 107px"></p></div><div id="info" class="">'+sm+zz+cbs+yzm+yz+cbn+ys+dj+zd+isbn+score+vote+'</div>',"html","utf-8"))

msg['From']=_format_addr(from_addr)
msg['To']=_format_addr(to_addr)
msg['Subject']=Header('来自乐程的问候......','utf-8').encode()

with open(book[12],'rb') as f:
	mime=MIMEBase('image','jpg',filename=book[12])
	mime.add_header('Content-Disposition','attachment',filename=book[12])
	mime.add_header('Content-ID','<0>')
	mime.add_header('X-Attachment-ID','0')
	mime.set_payload(f.read())
	encoders.encode_base64(mime)

msg.attach(mime)
import smtplib
server=smtplib.SMTP(smtp_server,25)
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()

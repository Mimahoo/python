#coding:utf-8
import re
import urllib
import urllib2
import MySQLdb
import cookielib
import sys
import time
import threading

#create table book_info(isbn char(20),sm char(100),zz char(100),cbs char(100),yzm char(150),yz char(100),cbn char(20),ys char(12),dj char(50),zd char(50),score char(5),vote char(8),pic char(50),url int)DEFAULT CHARSET=utf8;


conn=MySQLdb.connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='lcklbc1010',
	db='books'	
	)

cur=conn.cursor()
count=1
proxy=set()
ips=list()
lock=threading.Lock()

user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
headers={'User-Agent':user_agent}
data={}
data=urllib.urlencode(data)

def gethtml(url,ip):
	time.sleep(5)
	print 'getting '+url+'......'
	print 'proxy ip:'+ip
	p={'http':ip}
	proxy_support=urllib2.ProxyHandler(p)
	opener=urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)
	request=urllib2.Request(url,data,headers)
	try:
		page=urllib2.urlopen(request,None,2)
		html=page.read()
	except Exception, e:
		print e
		return ""
	return html
	
def geturl(html):
	book=list()
	reg='<a class="nbg"\n*?.*?href="(.*?\\.jpg)" title="([.a-zA-Z0-9\x00-\xff]*?)">' 
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0][0]
		print res[0][1]
		book.append(res[0][0])
		book.append(res[0][1])
	else:
		return book;
	reg='> 作者</span>:[.\x00-\xff]*?<a class.*?>([.\x00-\xff]*?)</a>' 
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='>出版社:</span> ([.\x00-\xff]*?)<'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='>原作名:</span> ([.\x00-\xff]*?)<'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='> 译者</span>:[.\x00-\xff]*?<a class.*?>([.\x00-\xff]*?)</a>' 
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='>出版年:</span> (([.0-9]|[\x00-\xff])*?)<br/*?>'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0][0]
		book.append(res[0][0])
	else:
		book.append("")
	reg='>页数:</span> ([0-9]*?)<br/*?>'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='>定价:</span> ([.0-9\x00-\xff]*?)<br/*?>'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='>装帧:</span> ([.\x00-\xff]*?)<br/*?>'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='>ISBN:</span> ([.0-9]*)<br/*?>'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		reg='>统一书号:</span> ([-0-9]*)<br/*?>'
		bookre=re.compile(reg)
		res=re.findall(bookre,html)
		book.append(res[0])
	reg='>豆瓣评分</div>[.\x00-\xff]*? ([.0-9]*?) </strong>'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	reg='<span property=.*?>([0-9]*?)</span>人评价'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	if len(res):
		print res[0]
		book.append(res[0])
	else:
		book.append("")
	return book

def test(i):
	try:
		ip={'http':ips[i]}
		proxy_support=urllib2.ProxyHandler(ip)
		opener=urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		url="http://book.douban.com/"
		headers={'User-Agent':user_agent}
		request=urllib2.Request(url,headers=headers)
		page=urllib2.urlopen(request,None,1)
		print "%s   OK" %ip
		lock.acquire()
		proxy.add(ips[i])
		lock.release()
	except Exception, e:
		return


def get_agent(count):
#	try:
	headers={'User-Agent':user_agent}
	url="http://www.66ip.cn/"+str(count)+".html"
	print url
	filename='cookie.txt'
	cookie = cookielib.MozillaCookieJar(filename)
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler=urllib2.HTTPCookieProcessor(cookie)
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	#此处的open方法同urllib2的urlopen方法，也可以传入request
	request=urllib2.Request(url,headers=headers)
	try:
		page = opener.open(request)
		html=page.read()
	except Exception, e:
		return 
	#print cookie
	#cookie.save(ignore_discard=True,ignore_expires=True)
	reg='<td>([\\.0-9]+?)</td>[\x00-\xff]*?.*?<td.*?>([0-9]*?)</td>'
	reg=re.compile(reg)
	res=re.findall(reg,html)
	for i in res:
		ips.append(i[0]+':'+i[1])

while 1:
	get_agent(count)
	count=(count+1)%100
	threads=[]
	for i in range(len(ips)):
		thread=threading.Thread(target=test,args=[i])
		threads.append(thread)
		thread.start()
#		test(i)
	for thread in threads:
		thread.join()
	
	if len(proxy)<1:
		ips=list()
		time.sleep(10)
		continue;
	print proxy
	for ip in proxy:
		tempset=set()
		cur.execute("select * from(select * from websites where visited=1 and finded=0) as temp limit 20")
		temp=cur.fetchmany(20)
		for val in temp:
			tempset.add((val[0],val[1]))

		for temp in tempset:
			time.sleep(2) 
			html=gethtml(temp[1],ip)
			res=geturl(html)
			if len(res):
				try:
					num=cur.execute('select * from book_info where isbn="%s"' %res[10])
				except Exception, e:
					print e
					continue;
				if num==1:
					continue;
				urllib.urlretrieve(res[0],'/home/lc/imgs/%s.jpg' %res[10])
				t='/home/lc/imgs/'+res[10]+'.jpg'
				try:
					cur.execute("insert into book_info values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)" %(res[10],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8],res[9],res[11],res[12],t,temp[0]))
					cur.execute("update websites set finded=1 where url='%s'" %temp[1])
				except Exception, e:
					print e
					continue;
				
				conn.commit()
			else:
				#cur.execute("delete from websites where url='%s'" %temp[1]);
				continue;
	time.sleep(10)
	proxy=set()
	ips=list()
conn.commit()
cur.close()
conn.close()



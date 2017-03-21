#coding:utf-8
import re
import urllib
import urllib2
import MySQLdb
import threading
import time
import cookielib

conn=MySQLdb.connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='lcklbc1010',
	db='books'	
	)

cur=conn.cursor()
count=2
proxy=set()
ips=list()
lock=threading.Lock()


user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
headers={'User-Agent':user_agent}
data={}
data=urllib.urlencode(data)

def gethtml(url,ip):
	time.sleep(2)
	print 'searching page '+url+'......'
	print 'proxy ip:'+ip
#	time.sleep(1.5)
	p={'http':ip}
	proxy_support=urllib2.ProxyHandler(p)
	opener=urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)
	request=urllib2.Request(url,headers=headers)
	try:
		page=urllib2.urlopen(request,None,3)
		html=page.read()#.decode('utf-8')
	except Exception, e:
		print e
	 	cur.execute('delete from websites where url="%s"' %url)
		return ""
	return html
	
def geturl(html):
	reg=r'https*://book.douban.com/subject/[0-9]*/'
	bookre=re.compile(reg)
	res=re.findall(bookre,html)
	return res
	
	
def test(i):
	try:
		ip={'http':ips[i]}
		proxy_support=urllib2.ProxyHandler(ip)
		opener=urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		url="http://members.3322.org/dyndns/getip"
		headers={'User-Agent':user_agent}
		request=urllib2.Request(url,headers=headers)
		page=urllib2.urlopen(request,None,1)
		
		print "%s   OK" %ip
#		raw_input('okkkkkkkkkkkkkkkkkkk')
		lock.acquire()
#		print 'aaaaaaaaaaa\n'+page.read()+'\naaaaaaaaaa'
		proxy.add(ips[i])
		lock.release()
	except Exception, e:
#		print "{%s}  error" %ips[i]
#		raw_input('errorrrrrrrrrrrrrrrr')
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
	except Exception, e:
		return 
	#print cookie
	#cookie.save(ignore_discard=True,ignore_expires=True)
	html=page.read()
#	print html
	reg='<td>([0-9][\\.0-9]+?)</td>[\x00-\xff]*?.*?<td.*?>([0-9]*?)</td>'
	#'<td>([0-9][\\.0-9]+?)</td>[\x00-\xff]*?.*?<td.*?>([0-9]*?)</td>'
	#data5u.com代理'<span><li>([\\.*0-9]*?)</li></span>[.\x00-\xff]*?<span style="width: 100px;"><li class="port GEGEA">([0-9]*?)</li>'
	#66代理'<td>([0-9][\\.0-9]+?)</td>[\x00-\xff]*?.*?<td.*?>([0-9]*?)</td>'
	#西刺代理'<td>([\\.0-9]+?)</td>[\x00-\xff]*?.*?<td.*?>([0-9]*?)</td>'
	reg=re.compile(reg)
	res=re.findall(reg,html)
#	print res
	for i in res:
		ips.append(i[0]+':'+i[1])
	#print ips 



while 1:
	
	tempset=set()
	get_agent(count)
	count=(count+1)%10
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
#	print proxy
	for ip in proxy:
		n=cur.execute("select * from(select * from websites where visited=0) as temp limit 20")
		temp=cur.fetchmany(20)
		#set(tempset)
		index=0
		#while index<n:
		for val in temp:
			tempset.add(val[1])
	
		for temp in tempset: 
			if temp=="":
				continue;
			html=gethtml(temp,ip)
			if html=="":
				continue;
			res=geturl(html)
			if not res:
				continue;
			cur.execute("update websites set visited=1 where url='%s'" %temp)
			s=set()
			for i in res:
				if i==temp:
					continue;
				s.add(i)
			s=s-tempset
			for i in s:
				sql='select * from websites where url="%s"' %i
				num=cur.execute(sql)
				if num==0:
					cur.execute('insert into websites values(NULL,"%s",0,0)' %i)
					print i+'       added!'
					conn.commit()
	time.sleep(10)
	proxy=set()
	ips=list()
conn.commit()
cur.close()
conn.close()



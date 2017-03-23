import re
import urllib
import urllib2
import MySQLdb
#coding:utf-8
#create table websites(id int primary key auto_increment,url char(50) not null,visited bool,count int);
#insert into websites values(NULL,'http://2345.com',0,0); 
conn=MySQLdb.connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='lcklbc1010',
	db='python'	
	)

cur=conn.cursor()

user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
headers={'User-Agent':user_agent}
data={}
data=urllib.urlencode(data)

def gethtml(url):
	print url
	request=urllib2.Request(url,data,headers)
	try:
		page=urllib2.urlopen(request,None,3)
	except Exception, e:
		cur.execute("delete from websites where url='%s'" %url)
		return ""
	try:
		html=page.read()#.decode('utf-8')
	except Exception, e:
		cur.execute("delete from websites where url='%s'" %url)
		return ""
	return html
	
def geturl(html):
	reg=r'((https*://)([0-9a-zA-Z]*\.)*([0-9a-zA-Z]+(\.[0-9a-zA-Z]+)+))/.*?'
	imgre=re.compile(reg)
	res=re.findall(imgre,html)
	print res
	return res

#file1=file("urls.txt","r+")
#file2=file("visited.txt","a")
#str1=file1.read()
#file1.truncate()
#str1=str1.split("\n")
visit_count=0
while visit_count<=6:
	tempset=set()
	n=cur.execute("select * from(select * from websites where visited=0 order by count desc)as temp limit 400")
	temp=cur.fetchmany(300)
	#set(tempset)
	index=0
	#while index<n:
	for val in temp:
	#	val=cur.fetchone()
	#	list(val)
		print val
		if val[2]==0:
			tempset.add(val[1])
		continue;
	
	for temp in tempset: 
		if temp=="":
			continue;
		html=gethtml(temp)
		if html=="":
			continue;
		res=geturl(html)
		cur.execute("update websites set visited=1 where url='%s'" %temp)
		if not res:
			continue;
		s=set()
		for i in res:
			print i
			#k=raw_input("y/n?")
			if i[1]+i[3]==temp:
				continue;
			s.add(i[1]+i[3])
		s=s-tempset
		print s
		for i in s:
			print i
			print type(i)
			sql='select * from websites where url="%s"' %i
			num=cur.execute(sql)
			print num
			if num==0:
				cur.execute('insert into websites values(NULL,"%s",0,0)' %i)
				conn.commit()
			else:
				cur.execute("update websites set count=(count+1) where url='%s'" %i)
				conn.commit()
	visit_count=1 + visit_count
conn.commit()
cur.close()
conn.close()

import re
import urllib
import urllib2
#coding:utf-8


user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
headers={'User-Agent':user_agent}
data={}
data=urllib.urlencode(data)

def gethtml(url):
	request=urllib2.Request(url,data,headers)
	try:
		page=urllib2.urlopen(request,None,5)
	except Exception, e:
		return ""
	try:
		html=page.read()#.decode('utf-8')
	except Exception, e:
		return ""
	return html
	
def geturl(html):
	reg=r'((https*://)([0-9a-zA-Z]*\.){0,1}([0-9a-zA-Z]+(\.[0-9a-zA-Z]+){1,2}))/.*?'
	imgre=re.compile(reg)
	res=re.findall(imgre,html)
	print res
	return res

file1=file("urls.txt","r+")
file2=file("visited.txt","a")
str1=file1.read()
file1.truncate()
str1=str1.split("\n")
print str1
	
for temp in str1: 
	if temp=="":
		continue;
	print temp
	html=gethtml(temp)
	if html=="":
		continue;
	res=geturl(html)
	
	if not res:
		continue;
	file2.write(temp+'\n')
	s=set()
	for i in res:
		
		#k=raw_input("y/n?")
		if i[1]+i[3]==temp:
			print i[1]+i[3]+" == "+temp
			continue;
		s.add(i[1]+i[3])
		print i[1]+i[3]
#	print '-----------'
	for i in s:
		print i
		file1.write(i+'\n')
file1.close()
file2.close()

#!/usr/bin/python
# -*- coding: utf-8 -*- 
import urllib2
import sys
import time

search_repo_url = "https://dev.aliyun.com/hubService/searchRepo.json?namePrefix=%s&sortProperty=downloads&page=1&pagesize=%d&isAuthentication=false"
get_repo_image_url = "https://dev.aliyun.com/hubService/getRepoImage.json?repoId=%d"

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
	"Referer": "https://dev.aliyun.com/hubService/searchRepo.json?namePrefix=redis&sortProperty=downloads&page=1&pagesize=10&isAuthentication=false"
}

def request(url):
	req = urllib2.Request(url, headers = headers)
	response = urllib2.urlopen(req)
	html = response.read()
	return eval(html.replace('false', 'False'))

#repo_name_space 是用户名 repo_name是镜像名 repo_name_space可以为空，repo_name不能为空
#根据用户名搜索
def search_for_repo_name_space(repo_name_space, pagesize = 2000):
	res_json = request(search_repo_url%(repo_name_space, pagesize))
	print ("%-10s %-10s %-10s %-10s"%("number", "repoId", "downloads", "repoName"))
	i = 0
	for res in res_json['data']['data']:
		if res.has_key('repoNamespace') and (res['repoNamespace'] == repo_name_space):
			i += 1
			print ("%-10s %-10s %-10s %-10s"%(i, res['repoId'], res['downloads'], res['repoNamespace'] + '/' + res['repoName']))
		#elif res['repoName'] == repo_name_space:
		#	print ("%-10s %-10s %-10s"%(i, res['repoId'], res['repoName']))

#TODO 根据镜像名搜索
def search_for_repo_name(repo_name, pagesize = 2000):
	pass

#获取镜像tag
def tags(id):
	res_json = request(get_repo_image_url%(id))
	print ("%-25s %-10s"%("update", "tag"))
	for data in res_json['data']:
		imageUpdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['imageUpdate'] / 1000))
		print ("%-25s %-10s"%(imageUpdate, data['tag']))

#
#

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print '%s [options] arg1'%(sys.argv[0])
		exit(0)
	if len(sys.argv) == 2:
		search_for_repo_name_space(sys.argv[1])
	elif sys.argv[1] == 'tag':
		tags(int(sys.argv[2]))
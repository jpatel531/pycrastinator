#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, web

def main(wf):
	wf.add_item(u'Hello World', u'Yo')
	wf.add_item(u'Get involved', u'Dench')
	wf.send_feedback()

def get_link_data(link):
	url = "https://readability.com/api/content/v1/parser?token=4310f16dcd78910cd084ddc1c1b2d008a603cbb5&url=%s" % link
	return web.get(url).json()


def add(wf):
	link = wf.args[1]

	link_data = get_link_data(link)
	title = link_data.get('title')
	word_count = str(link_data.get('word_count'))


	wf.add_item(title, word_count)
	wf.send_feedback()

if __name__ == '__main__':
	wf = Workflow()

	command = wf.args[0]

	if command == 'add':
		sys.exit(wf.run(add))
	else:	
		sys.exit(wf.run(main))
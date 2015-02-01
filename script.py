#!/usr/bin/python
# encoding: utf-8
import json
import sys
from workflow import Workflow, web


def main(wf):

	links = wf.stored_data('pycrastinator')
	for link in links:
		wf.add_item(
			title=link['title'], 
			subtitle=link['word_count'], 
			arg=link['link'], 
			valid= True, 
			icon=link['icon'])

	wf.send_feedback()

def get_link_data(link):
	url = "https://readability.com/api/content/v1/parser?token=4310f16dcd78910cd084ddc1c1b2d008a603cbb5&url=%s" % link
	return web.get(url).json()

def confirm(wf):
	link = wf.args[1]

	link_data = get_link_data(link)
	title = link_data.get('title')
	word_count = str(link_data.get('word_count'))
	icon = link_data.get('lead_image_url')

	data = {'link': link, 'title': title, 'word_count': word_count, 'icon': icon}

	json_data = json.dumps(data)

	wf.add_item(
		title=title, 
		subtitle=word_count, 
		arg=json_data,
		valid=True,
		icon=icon)

	wf.send_feedback()

def add(wf):
	data = wf.args[1]
	data = json.loads(data)

	store_data = wf.stored_data('pycrastinator')

	store_data.append(data)

	wf.store_data('pycrastinator', store_data)

	wf.add_item(title, word_count, icon)
	wf.send_feedback()

if __name__ == '__main__':
	wf = Workflow()
	wf.data_serializer = 'json'
	command = wf.args[0]

	if not wf.stored_data('pycrastinator'):
		wf.store_data('pycrastinator', [])

	if command == 'add':
		sys.exit(wf.run(add))

	elif command == 'confirm':
		sys.exit(wf.run(confirm))

	elif command == 'open':
		raise Exception(args[1])
	else:	
		sys.exit(wf.run(main))
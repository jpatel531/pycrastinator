#!/usr/bin/python
# encoding: utf-8

import json, sys, math
from workflow import Workflow, web

def main(wf):
	links = wf.stored_data('pycrastinator')

	links.sort(key=lambda link: link['time_to_read'])

	for link in links:
		wf.add_item(
			title=link['title'], 
			subtitle=link['time_to_read'], 
			arg=link['link'], 
			valid= True, 
			icon=link['icon'])

	wf.send_feedback()

def get_link_data(link):
	url = "https://readability.com/api/content/v1/parser?token=4310f16dcd78910cd084ddc1c1b2d008a603cbb5&url=%s" % link
	return web.get(url).json()

def confirm(wf):
	link = wf.args[1]

	try:
		link_data = get_link_data(link)
		title = link_data.get('title')
		word_count = link_data.get('word_count')
		icon = link_data.get('lead_image_url')

		time_length = int(math.ceil(word_count / 220.00))

		time_to_read = '%s mins read' % time_length

		data = {'link': link, 'title': title, 'word_count': word_count, 'icon': icon, 'time_to_read': time_to_read}

		json_data = json.dumps(data)

		wf.add_item(
			title=title, 
			subtitle=time_to_read, 
			arg=json_data,
			valid=True,
			icon=icon)

		wf.send_feedback()
	except:
		pass

def add(wf):
	data = wf.args[1]
	data = json.loads(data)

	store_data = wf.stored_data('pycrastinator')

	store_data.append(data)

	wf.store_data('pycrastinator', store_data)

	wf.add_item(title=data['title'], subtitle=data['time_to_read'], arg=data['title'], valid=True)
	wf.send_feedback()

def remove(wf):
	link = wf.args[1]
	data = wf.stored_data('pycrastinator')
	data = [item for item in data if item['link'] != link]
	wf.store_data('pycrastinator', data)


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

	elif command == 'remove':
		sys.exit(wf.run(remove))

	else:	
		sys.exit(wf.run(main))
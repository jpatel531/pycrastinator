#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow

def main(wf):

	wf.add_item(u'Hello World', u'Yo')

	wf.add_item(u'Get involved', u'Dench')

	wf.send_feedback()

if __name__ == '__main__':
	wf = Workflow()
	sys.exit(wf.run(main))
# -*- coding: utf-8 -*-

__all__ = ['startfoxdot']

from inspect import stack
import editor
import requests
import ui

def _show_output(text):
	view = _show_output.view
	console_view = _show_output.console_view
	console_view.text = text + console_view.text

	try:
		view.present('panel')
	except:
		if not view.on_screen:
			view.close()
			ui.delay(lambda: view.present('panel'), 0.1)


def _get_separator():
	for item in stack():
		if item.filename == __file__:
			continue
		return item.code_context[0]
	return ''


def _initextension():
	view = ui.View()
	view.name = 'FoxDot'
	view.background_color = 'white'

	console_view = ui.TextView(name='console_view')

	console_view.frame = view.frame
	console_view.flex = 'wh'
	console_view.font = ('Menlo', 10)
	console_view.editable = False
	console_view.selectable = True

	view.add_subview(console_view)
	view.present('panel')

	_show_output.view = view
	_show_output.console_view = console_view


def startfoxdot(hostname='foxdot.local', port=8000, timeout=1):
	try:
		_initextension.ready
	except AttributeError:
		_initextension()
		_initextension.ready = True

	block = _get_block(_get_separator())
	if block:
		response = requests.post(
			'http://' + hostname + ':' + str(port), data=block, timeout=timeout)
		_show_output(response.text)

	exit()


def _get_block(separator):
	text = editor.get_text()

	separator_start = text.find(separator) + len(separator)

	cursor_position = editor.get_line_selection()[0]
	if cursor_position <= separator_start:
		return ''

	block_start = text.rfind('\n\n', separator_start, cursor_position + 1)
	if block_start == -1:
		block_start = separator_start

	block_end = text.find('\n\n', cursor_position - 1)
	if block_end == -1:
		block_end = len(text)

	return text[block_start:block_end].strip()


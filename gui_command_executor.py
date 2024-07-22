#!/usr/bin/env python3

#
# gui_command_executor.py
#
# Date    : 2024-05-25
# Author  : Hirotoshi FUJIBE
# History :
#
# Copyright (c) 2024 Hirotoshi FUJIBE
#

# Import Libraries
import os
import subprocess
import flet as ft

# Constants
CMD_DIR = '.\\bin'
CMD_NAME = 'dummy_command.bat'
CMD_ENCODING = 'shift-jis'
DEBUG = False

# Windows Size
WINDOW_RATIO = 60
WINDOW_WIDTH = 16 * WINDOW_RATIO
WINDOW_HEIGHT = 10 * WINDOW_RATIO
LIST_SPACING = 5
LIST_PADDING = 10
TEXTBOX_LENGTH = 250


def write_message(page: ft.Page, list_view: ft.ListView, message: str) -> None:
    list_view.controls.append(ft.Text(message))
    page.update()
    return


# Execute Command
def execute_command(page: ft.Page, list_view: ft.ListView, text_value: str) -> None:

    list_view.clean()

    param1 = text_value.strip()
    if param1 == '':
        write_message(page, list_view, 'Parameter is not specified.')
        return

    write_message(page, list_view, 'call')

    proc = subprocess.Popen(
        [CMD_NAME, param1], cwd=CMD_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding=CMD_ENCODING, text=True, shell=True)

    if DEBUG:
        print('start of read stdout')

    while proc.poll() is None:

        line_string = proc.stdout.readline()
        if not line_string:
            break

        if DEBUG:
            print('stdout > %s' % line_string.strip())
        write_message(page, list_view, line_string.strip())

    if DEBUG:
        print('end of read stdout')

    proc.wait()
    ret = proc.returncode
    proc.terminate()

    if DEBUG:
        print('return : %d' % ret)
    write_message(page, list_view, 'exit : %d' % ret)

    return


# Main
def main(page: ft.Page) -> None:

    os.environ['PATH'] += ';' + CMD_DIR

    def yes_click(e):  # noqa
        page.window_destroy()

    def no_click(e):  # noqa
        confirm_dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text('Confirm'),
        content=ft.Text('Are you sure?'),
        actions=[
            ft.ElevatedButton('Yes', on_click=yes_click),
            ft.OutlinedButton('No', on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def window_event(e):
        if e.data == 'close':
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()
            return

    def click_execute_button(e):  # noqa
        text_value = str(compo_text.value)
        compo_execute_button.disabled = True
        compo_close_button.disabled = True
        execute_command(page, compo_list, text_value)
        compo_execute_button.disabled = False
        compo_close_button.disabled = False
        page.update()
        return

    def click_close_button(e):  # noqa
        page.window_destroy()
        return

    page.title = 'Command Executor'
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT
    page.window_prevent_close = True
    page.on_window_event = window_event

    compo_text = ft.TextField(label='Parameter', hint_text="Input command parameter",
                              value='', text_align=ft.TextAlign.LEFT, width=TEXTBOX_LENGTH)
    compo_execute_button = ft.FilledButton(text="Execute", on_click=click_execute_button)
    compo_close_button = ft.OutlinedButton(text="Close", on_click=click_close_button)
    compo_list = ft.ListView(expand=1, spacing=LIST_SPACING, padding=LIST_PADDING)

    page.add(
        ft.Row(
            [
                compo_text,
                compo_execute_button,
                compo_close_button,
            ]
        ),
        ft.Row(
            [
                compo_list,
            ]
        )
    )


# Goto Main
ft.app(target=main)

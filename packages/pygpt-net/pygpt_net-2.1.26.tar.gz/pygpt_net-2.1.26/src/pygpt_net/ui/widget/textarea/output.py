#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.03.09 07:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextBrowser, QMenu
from PySide6.QtGui import QDesktopServices, QAction, QIcon, QTextOption

from pygpt_net.utils import trans
import pygpt_net.icons_rc


class ChatOutput(QTextBrowser):
    def __init__(self, window=None):
        """
        Chat output

        :param window: main window
        """
        super(ChatOutput, self).__init__(window)
        self.window = window
        self.setReadOnly(True)
        self.setStyleSheet(self.window.controller.theme.style('font.chat.output'))
        self.value = self.window.core.config.data['font_size']
        self.max_font_size = 42
        self.min_font_size = 8
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        self.anchorClicked.connect(self.open_external_link)
        self.setWordWrapMode(QTextOption.WordWrap)

    def open_external_link(self, url):
        """
        Open external link

        :param url: url
        """
        extra_schemes = ['extra-delete', 'extra-edit', 'extra-copy', 'extra-replay', 'extra-audio-read', 'extra-join']

        # local file
        if not url.scheme().startswith('http') and url.scheme() not in extra_schemes:
            self.window.controller.files.open(url.toLocalFile())

        # extra actions
        elif url.scheme() == 'extra-delete':  # ctx item delete
            id = url.toString().split(':')[1]
            self.window.controller.ctx.extra.delete_item(int(id))
        elif url.scheme() == 'extra-edit':  # ctx item edit
            id = url.toString().split(':')[1]
            self.window.controller.ctx.extra.edit_item(int(id))
        elif url.scheme() == 'extra-copy':  # ctx item copy
            id = url.toString().split(':')[1]
            self.window.controller.ctx.extra.copy_item(int(id))
        elif url.scheme() == 'extra-replay':  # ctx regen response
            id = url.toString().split(':')[1]
            self.window.controller.ctx.extra.replay_item(int(id))
        elif url.scheme() == 'extra-audio-read':  # ctx audio read
            id = url.toString().split(':')[1]
            self.window.controller.ctx.extra.audio_read_item(int(id))
        elif url.scheme() == 'extra-join':  # ctx join
            id = url.toString().split(':')[1]
            self.window.controller.ctx.extra.join_item(int(id))

        else:
            # external link
            QDesktopServices.openUrl(url)

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: Event
        """
        menu = self.createStandardContextMenu()
        selected_text = self.textCursor().selectedText()

        if selected_text:
            # plain text
            plain_text = self.textCursor().selection().toPlainText()

            # audio read
            action = QAction(QIcon(":/icons/volume.svg"), trans('text.context_menu.audio.read'), self)
            action.triggered.connect(self.audio_read_selection)
            menu.addAction(action)

            # copy to
            copy_to_menu = QMenu(trans('text.context_menu.copy_to'), self)

            # input
            action = QAction(QIcon(":/icons/input.svg"), trans('text.context_menu.copy_to.input'), self)
            action.triggered.connect(
                lambda: self.window.controller.chat.common.append_to_input(selected_text))
            copy_to_menu.addAction(action)

            # notepad
            num_notepads = self.window.controller.notepad.get_num_notepads()
            if num_notepads > 0:
                for i in range(1, num_notepads + 1):
                    name = self.window.controller.notepad.get_notepad_name(i)
                    action = QAction(QIcon(":/icons/paste.svg"), name, self)
                    action.triggered.connect(lambda checked=False, i=i:
                                             self.window.controller.notepad.append_text(selected_text, i))
                    copy_to_menu.addAction(action)

            # calendar
            action = QAction(QIcon(":/icons/schedule.svg"), trans('text.context_menu.copy_to.calendar'), self)
            action.triggered.connect(
                lambda: self.window.controller.calendar.note.append_text(selected_text))
            copy_to_menu.addAction(action)

            menu.addMenu(copy_to_menu)

            # save as (selected)
            action = QAction(QIcon(":/icons/save.svg"), trans('action.save_as'), self)
            action.triggered.connect(
                lambda: self.window.controller.chat.common.save_text(plain_text))
            menu.addAction(action)
        else:
            # save as (all)
            action = QAction(QIcon(":/icons/save.svg"), trans('action.save_as'), self)
            action.triggered.connect(
                lambda: self.window.controller.chat.common.save_text(self.toPlainText()))
            menu.addAction(action)

        menu.exec_(event.globalPos())

    def audio_read_selection(self):
        """Read selected text (audio)"""
        self.window.controller.audio.read_text(self.textCursor().selectedText())

    def wheelEvent(self, event):
        """
        Wheel event: set font size

        :param event: Event
        """
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                if self.value < self.max_font_size:
                    self.value += 1
            else:
                if self.value > self.min_font_size:
                    self.value -= 1

            self.window.core.config.data['font_size'] = self.value
            self.window.core.config.save()
            option = self.window.controller.settings.editor.get_option('font_size')
            option['value'] = self.value
            self.window.controller.config.apply(
                parent_id='config', 
                key='font_size', 
                option=option,
            )
            self.window.controller.ui.update_font_size()
            event.accept()
        else:
            super(ChatOutput, self).wheelEvent(event)

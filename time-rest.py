#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2012 Deepin, Inc.
#               2011~2012 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
start_time = time.time()

import gtk 
import cairo
import threading
from dtk.ui.utils import color_hex_to_cairo
from daemon import Daemon
import sys

WORK_SECOND = 3600
REST_SECOND = 60
TEXT = "请休息 %s 秒，以保护眼睛！" % REST_SECOND

class ColorWidget(gtk.DrawingArea):
    '''
    class docs
    '''
	
    def __init__(self, color):
        '''
        init docs
        '''
        gtk.DrawingArea.__init__(self)
        self.color = color
        
        self.connect("expose-event", self.expose)
        
    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        
        cr.set_source_rgb(*color_hex_to_cairo(self.color))
        cr.rectangle(0, 0, rect.width, rect.height)
        cr.fill()

        cr.set_source_rgb(*color_hex_to_cairo("#FF0000"))
            
        cr.select_font_face("WenQuanYi Micro Hei", cairo.FONT_SLANT_NORMAL, 
            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(50)
        
        (x, y, width, height, dx, dy) = cr.text_extents(TEXT)
        cr.move_to(rect.width/2 - width/2, rect.height/2)
        cr.show_text(TEXT)
        
        return True

class FullScreenWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.connect('destroy', gtk.main_quit)
        
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
        self.set_size_request( gtk.gdk.screen_width(), gtk.gdk.screen_height())
        self.set_position(gtk.WIN_POS_CENTER)
        self.init_status_icon()
        widget = ColorWidget('#C7EDCC')
        self.add(widget)
        
    def init_status_icon(self):
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_stock(gtk.STOCK_INFO)
        self.status_icon.connect('popup-menu', self.pop_status_icon_menu)

    def pop_status_icon_menu(self, status_icon, button, activate_time):
        menu = gtk.Menu()

        about = gtk.MenuItem("About")
        quit = gtk.MenuItem("Quit")
        
        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", gtk.main_quit)
        
        menu.append(about)
        menu.append(quit)
        
        menu.show_all()
        
        menu.popup(
                None, 
                None, 
                gtk.status_icon_position_menu, 
                button, 
                activate_time, 
                self.status_icon
        )
    
    def show_about_dialog(self, widget):
        pass

class ListenTime(threading.Thread):
    def __init__(self, widget, hide_second, show_second):
        threading.Thread.__init__(self)
        self.widget = widget
        self.hide_second = hide_second
        self.show_second = show_second
 
    def run(self):
        while True:
            self.widget.hide()
            time.sleep(self.hide_second)
            self.widget.show_all()
            time.sleep(self.show_second)

class RunDaemon(Daemon):
    def _run(self):
        gtk.gdk.threads_init()
        win = FullScreenWindow()
        td = ListenTime(win, WORK_SECOND, REST_SECOND)
        td.setDaemon(True)
        td.start()
        gtk.main()

if __name__ == "__main__":
    daemon = RunDaemon('/tmp/time-rest-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

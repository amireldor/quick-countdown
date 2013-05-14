Quick-Countdown
===============

This is supposed to be some kind of multiple countdown timers application for
usage with online RTS games where you have to wait hours for stuff to be done,
such as tech research or building of units. You don't want your base to sit
idle doing nothing and you don't want to keep track of time when to check your
browser or whatever client there is when it's time to give new orders.
Quick-Countdown is supposed to help you.

Requirements
------------

Quick-Countdown uses wxPython and was written in Python 2.7 with wxWidget
version 2.8, but uses mostly basic stuff so it should be nice.

It uses `wx.SingleInstanceChecker` which works only under Windows and Unix
(see [documentation about it][wxSignalChecker]). I guess I can probably
disable this functionality with some flag but who will use this not under
Windows/Unix?

[wxSignalChecker]: http://docs.wxwidgets.org/2.8/wx_wxsingleinstancechecker.html

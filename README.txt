Quick-Countdown
===============

This uses wxPython and was written in Python 2.7 with wxWidget version 2.8, but
uses mostly basic stuff so it should be nice.

It uses `wx.SingleInstanceChecker` which works only under Windows and Unix
(see [documentation about it][wxSignalChecker]). I guess I can probably
disable this functionality with some flag but who will use this not under
Windows/Unix?

[wxSignalChecker]: http://docs.wxwidgets.org/2.8/wx_wxsingleinstancechecker.html

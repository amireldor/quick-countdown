#!/usr/bin/env python

import wx

class QuickCountdownFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title='Quick Countdown')

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Destroy()

def main():
    print 'Hello!'

    app = wx.App()
    main_frame = QuickCountdownFrame()
    main_frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()

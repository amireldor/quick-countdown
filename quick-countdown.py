#!/usr/bin/env python

import wx

# TODO: consider moving inside QuickCountdownFrame?
class ID(object):
    TEXTCTRL_ADD = 1
    LIST_TIMERS = 2
    RADIOBOX_SORT_ORDER = 3
    RADIOBOX_SORT_BY = 4
    BUTTON_SETTINGS = 5
    BUTTON_HELP = 6
    BUTTON_ADD = 7

class QuickCountdownFrame(wx.Frame):

    COMMON_SIZER_BORDER = 5

    DEFAULT_SIZE = (350, 500)

    def __init__(self):
        wx.Frame.__init__(self, None, title='Quick Countdown', size=self.DEFAULT_SIZE)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        panel = wx.Panel(self)

        self.textctrl_add = wx.TextCtrl(panel, ID.TEXTCTRL_ADD)
        self.button_add = wx.Button(panel, ID.BUTTON_ADD, 'Add')
        self.radiobox_sort_by = wx.RadioBox(panel, ID.RADIOBOX_SORT_BY, label="Sort by", choices=['Time', 'Added'], style=wx.RA_SPECIFY_COLS)
        self.radiobox_sort_order = wx.RadioBox(panel, ID.RADIOBOX_SORT_ORDER, label="Sort order", choices=['Asc', 'Desc'], style=wx.RA_SPECIFY_COLS)
        self.list_timers = wx.ListBox(panel, ID.LIST_TIMERS)
        self.button_settings = wx.Button(panel, ID.BUTTON_SETTINGS, 'Settings')
        self.button_help = wx.Button(panel, ID.BUTTON_HELP, 'Help')

        add_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_sizer.AddMany((
            (self.textctrl_add, 1, wx.ALL | wx.EXPAND, self.COMMON_SIZER_BORDER),
            (self.button_add, 0, wx.ALL, self.COMMON_SIZER_BORDER),
        ))

        sort_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sort_sizer.AddMany((
            (self.radiobox_sort_by, 1, wx.LEFT | wx.EXPAND, self.COMMON_SIZER_BORDER),
            (self.radiobox_sort_order, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, self.COMMON_SIZER_BORDER),
        ))

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.AddMany((
            (self.button_settings, 1, wx.ALL | wx.EXPAND, self.COMMON_SIZER_BORDER),
            (self.button_help, 0, wx.ALL, self.COMMON_SIZER_BORDER),
        ))

        vert_sizer = wx.BoxSizer(wx.VERTICAL)
        vert_sizer.AddMany((
            (add_sizer, 0, wx.ALL | wx.EXPAND, self.COMMON_SIZER_BORDER),
            (sort_sizer, 0, wx.ALL | wx.EXPAND, self.COMMON_SIZER_BORDER),
            (self.list_timers, 4, wx.ALL | wx.EXPAND, self.COMMON_SIZER_BORDER),
            (buttons_sizer, 0, wx.ALL | wx.EXPAND, self.COMMON_SIZER_BORDER),
        ))

        panel.SetSizer(vert_sizer)

        self.textctrl_add.SetFocus()

    def OnClose(self, event):
        self.Destroy()

def main():
    print 'Hello!'

    app = wx.App()

    # should this be called before `app = wx.App()`?
    single_checker  = wx.SingleInstanceChecker(name='quick-countdown-%s' % (wx.GetUserId()))
    if single_checker.IsAnotherRunning():
        print 'Another instance running (will probably implement a flag to allow multiple instances later)'
        # TODO: focus on other instance here
        exit()

    main_frame = QuickCountdownFrame()
    main_frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()

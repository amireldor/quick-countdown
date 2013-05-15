import wx
import re

def ParseTimerText(entered_text):
    """Parse text like '3h tank built' and return (seconds, message) with the parsed values.

    Examples for input:

        '29m Singing bowl' # m for minutes
        'Singing 2Days bowl'
        'Cat jumps 30s'
        '12h cat is 30h old' # 12 hours and not 30 coz '30h' comes after '12h' and thus has less importance
        '1d 2h 20m food is ready'
        '1 day 2 minutes 30s cat is dog'

    """
    seconds = 0
    minutes = 0
    hours = 0
    days = 0
    message = []

    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR

    parts = entered_text.split()
    digits_letter_pattern = re.compile('([\d]+)([dhms])', re.IGNORECASE)
    remember_number = None
    for x in parts:

        try:
            # does it start with '0'?
            if x[0] == '0':
                raise ValueError
                # TODO: we can probably add `x[0] == '-'` here and remove `number <= 0` later,
                # but need to see how it works with the code inside ValueError

            # is it an integer?
            number = int(x)

            if number <= 0:
                """negative numbers are considered part of the message"""
                message.append(x)
            else:
                if remember_number is not None:
                    """we already had a number, and we've found another number now!
                    so the previous number must have been part of the message."""
                    message.append(unicode(remember_number))
                else:
                    """we did not remember any number, this is the first lonely number we see.
                    let's remember it for next iteration"""
                    #remember_number = x
                    pass
                remember_number = number

        except ValueError:
            # it's not parsed as a pure integer, so check if it's like "hours" or "3s"

            interval = None
            value = None

            lower = x.lower()
            if lower.startswith('second'):
                interval = 's'
            elif lower.startswith('minute'):
                interval = 'm'
            elif lower.startswith('hour'):
                interval = 'h'
            elif lower.startswith('day'):
                interval = 'd'

            if interval is None:
                # we did not find "second" or "minutes", looks for the regex pattern
                matches = digits_letter_pattern.match(x)
                if matches:
                    value = int(matches.group(1))
                    if value <= 0:
                        value = None
                    interval = matches.group(2)[0].lower()
                #else:
                #    message.append(x)
            else:
                # we've found "second" or "minutes", use the remembered number as value
                if remember_number is not None:
                    value = remember_number
                    remember_number = None
                #else:
                #    message.append(x)

            if value is None:
                """we did not find any value to add so far,
                not in a "20m" or a remember_number of "20" and x of "minutes",
                so just add the `x` to the message"""
                if remember_number is not None:
                    """we had a pure number before `x`, so, add it as well"""
                    message.append(unicode(remember_number))
                    remember_number = None
                message.append(x)
            else:
                """we have a value, and we have an interval. all that is left is to assign them
                to the relevant variables, if that variable was not already set"""
                changed = False
                if interval == 's' and seconds == 0:
                    seconds = value
                    changed = True
                elif interval == 'm' and minutes == 0:
                    minutes = value
                    changed = True
                elif interval == 'h' and hours == 0:
                    hours = value
                    changed = True
                elif interval == 'd' and days == 0:
                    days = value
                    changed = True

                if not changed:
                    """hmm, we didn't change a thing,
                    e.g. `seconds` was already set to "10" and we met something like "32 seconds" or "10s".
                    because we give precedence to the first time values in the input,
                    we add the current string we met to `message`"""
                    if remember_number is not None:
                        """we had a pure number before `x`, so, add it as well"""
                        message.append(unicode(remember_number))
                        remember_number = None
                    message.append(x)


    if remember_number is not None:
        """this is for the case there's a number as the last part of the input string"""
        message.append(unicode(remember_number))

    seconds = seconds + MINUTE*minutes + HOUR*hours + DAY*days
    message = ' '.join(message)

    return seconds, message

# TODO: consider moving inside QuickCountdownFrame?
class ID(object):
    TEXTCTRL_ADD = 1
    LIST_TIMERS = 2
    RADIOBOX_SORT_ORDER = 3
    RADIOBOX_SORT_BY = 4
    BUTTON_SETTINGS = 5
    BUTTON_HELP = 6
    BUTTON_ADD = 7
    TIMER = 1000

class CountdownTimer(wx.Timer):
    """A timer with a seconds_left property indicating a countdown operation.
    Call the `Update()` method each iteration and check for `HasEnded()`.

    This is not complete as wx.Timer can also be called with some `Notify()`
    functionality but I don't know."""

    def __init__(self, parent, id=wx.ID_ANY, seconds=0):
        wx.Timer.__init__(self, parent, id)
        self.seconds_left = seconds

    def GetSecondsLeft(self):
        return self.seconds_left

    def Update(self):
        """Decrease one second and return whether the countdown ended.""" 
        self.seconds_left -= 1
        return self.HasEnded()

    def HasEnded(self):
        if self.seconds_left <= 0:
            return True

        return False

class MyCountdownTimer(CountdownTimer):
    """A countdown timer with all kinds of interesting stuff for our Quick-Countdown application.
    It has a `message` property for example!"""

    def __init__(self, parent, id=wx.ID_ANY, seconds=0, message=''):
        CountdownTimer.__init__(self, parent, id, seconds)
        self.message = message

    def GetMessage(self):
        return self.message

    def SetMessage(self, message):
        self.message = message

class NotCallableIterator(object):
    """An iterator of class methods"""
    def __init__(self, cls):
        self.index = 0
        self.items = [ getattr(cls, method) for method in dir(cls) if not callable(getattr(cls, method)) ]

    def next(self):
        try:
            self.index += 1
            return self.items[self.index-1]
        except IndexError:
            raise StopIteration

class MyTimersList(wx.ListBox):
    """A list box that shows the MyCountdownTimer()s we give it with the `timers` parameter on __init__"""

    class SORT_BY():
        ADDED = 1
        TIME = 2
        def __iter__(self):
            return NotCallableIterator(self)

    class SORT_ORDER(object):
        ASC = 1
        DESC = 2
        def __iter__(self):
            return NotCallableIterator(self)

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name="listBox", timers=None, sort_by=SORT_BY.ADDED, sort_order=SORT_ORDER.ASC):
        wx.ListBox.__init__(self, parent, id=id, pos=pos, size=size, style=style, validator=validator, name=name, choices=[])
        self.timers = timers

        self.sort_by = sort_by
        self.sort_order = sort_order

    def UpdateMyList(self):
        if self.sort_by == self.SORT_BY.ADDED:
            items = [ "%s - %s" % (x.GetSecondsLeft(), x.GetMessage()) for x in self.timers ]
            if self.sort_order == self.SORT_ORDER.DESC:
                print 'reverse'
                items.reverse()

        self.Set(items=items)

    def SetSortOrder(self, order):
        if order not in self.SORT_ORDER():
            raise KeyError
        self.sort_order = order

    def SetSortBy(self, by):
        if by not in self.SORT_BY():
            raise KeyError
        self.sort_by = by


class QuickCountdownFrame(wx.Frame):

    COMMON_SIZER_BORDER = 5
    DEFAULT_SIZE = (350, 500)

    # Widgets labels TO MyTimersList sort ID values
    SORT_BY = { 'Added': MyTimersList.SORT_BY.ADDED, 'Time': MyTimersList.SORT_BY.TIME }
    SORT_ORDER = { 'Asc': MyTimersList.SORT_ORDER.ASC, 'Desc': MyTimersList.SORT_ORDER.DESC }

    def __init__(self):
        wx.Frame.__init__(self, None, title='Quick Countdown', size=self.DEFAULT_SIZE)

        panel = wx.Panel(self)
        self.timers = []

        self.textctrl_add = wx.TextCtrl(panel, ID.TEXTCTRL_ADD, style=wx.TE_PROCESS_ENTER)
        self.button_add = wx.Button(panel, ID.BUTTON_ADD, 'Add')
        self.radiobox_sort_by = wx.RadioBox(panel, ID.RADIOBOX_SORT_BY, label="Sort by", choices=self.SORT_BY.keys(), style=wx.RA_SPECIFY_COLS)
        self.radiobox_sort_order = wx.RadioBox(panel, ID.RADIOBOX_SORT_ORDER, label="Sort order", choices=self.SORT_ORDER.keys(), style=wx.RA_SPECIFY_COLS)
        self.list_timers = MyTimersList(panel, ID.LIST_TIMERS, timers=self.timers, sort_order=MyTimersList.SORT_ORDER.DESC)
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

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextAddEnter, id=ID.TEXTCTRL_ADD)
        self.Bind(wx.EVT_BUTTON, self.OnTextAddEnter, id=ID.BUTTON_ADD)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxSortBy, id=ID.RADIOBOX_SORT_BY)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxSortOrder, id=ID.RADIOBOX_SORT_ORDER)

    def OnClose(self, event):
        self.Destroy()

    def OnTextAddEnter(self, event):
        entered_text =  self.textctrl_add.GetValue()

        seconds, message = ParseTimerText(entered_text)

        # create new timer
        countdown_timer = MyCountdownTimer(self, id=ID.TIMER, message=message, seconds=seconds)
        self.timers.append(countdown_timer)
        self.Bind(wx.EVT_TIMER, self.OnTimer, countdown_timer)
        countdown_timer.Start()

    def OnTimer(self, event):
        self.list_timers.UpdateMyList()

        timer = event.GetEventObject()
        if not timer.HasEnded():
            timer.Update()
        else:
            timer.Stop()

        #if timer.HasEnded():
        #    self.timers.remove(timer)
        #    del timer

    def OnRadioBoxSortOrder(self, event):
        selection = self.radiobox_sort_order.GetSelection()
        label = self.radiobox_sort_order.GetItemLabel(selection)

        self.list_timers.SetSortOrder(self.SORT_ORDER[label])

    def OnRadioBoxSortBy(self, event):
        selection = self.radiobox_sort_by.GetSelection()
        label = self.radiobox_sort_by.GetItemLabel(selection)

        self.list_timers.SetSortBy(self.SORT_BY[label])

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

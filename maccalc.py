#! /usr/bin/python

# (C) 2017 David Pye davidmpye@gmail.com
# GNU General Public Licence v3.0 or later

import math
import wx

class MainWidget(wx.Frame):

    volatiles = { 
        'Isoflurane' : 1.17,
        'Sevoflurane' : 1.80, 
        'Desflurane' : 6.6
#       'Xenon' : 72.0,
#       'Halothane': 0.75,
#       'Enflurane' : 1.63,
#       'Diethyl Ether': 3.2,
#       'Chloroform': 0.5,
#       'Methoxyflurane' : 0.16
    }

    #This is separate as it doesn't need appear in the pulldown list 
    Mac40N2O = 104.0;

    def __init__(self, parent, title):
        super(MainWidget, self).__init__(parent,title=title, 
                style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.InitUI()
        self.Show()
        
    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(5, 2)
    
        agelabel = wx.StaticText(panel, label="Patient age:");
        agentlabel = wx.StaticText(panel, label="Agent:")
        agentpclabel = wx.StaticText(panel, label="Agent %:")
        n2opclabel = wx.StaticText(panel, label="N2O %:")
        maclabel = wx.StaticText(panel, label="MAC"); 
        
        #These need visibility from other functions so they can be set etc.
        self.ageCB = wx.SpinCtrl(panel, value="40");
        self.agentCB = wx.ComboBox(panel, choices = sorted(self.volatiles.keys()), style = wx.CB_READONLY)
        self.agentCB.SetSelection(2)
        
        self.agentpcCB = wx.SpinCtrlDouble(panel, value="1.8")
        self.agentpcCB.SetDigits(2)
        self.agentpcCB.SetIncrement(0.1)
        self.n2opcCB = wx.SpinCtrl(panel,value="0")
        self.macCB = wx.SpinCtrlDouble(panel)
        self.macCB.SetDigits(2)
        self.macCB.SetIncrement(0.1)
        
        fgs.AddMany([(agelabel), (self.ageCB), (agentlabel), (self.agentCB), 
            (agentpclabel), (self.agentpcCB), (n2opclabel), (self.n2opcCB), 
            (maclabel), (self.macCB)])
        vbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        
        panel.SetSizer(vbox)
    
        #Event binding
        #If MAC box is changed, we need to recalculate the FiAgent.
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.recalcEtAgent, id=self.macCB.GetId())
        #If any of the other fields are touched, we need to recalculate the MAC
        self.Bind(wx.EVT_SPINCTRL, self.recalcMac, id=self.ageCB.GetId())
        self.Bind(wx.EVT_COMBOBOX, self.recalcMac, id=self.agentCB.GetId())
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.recalcMac, id=self.agentpcCB.GetId())
        self.Bind(wx.EVT_SPINCTRL, self.recalcMac, id=self.n2opcCB.GetId())

        #Calculate MAC for the default values.
        self.recalcMac(wx.EVT_SPINCTRL) #event is unimportant...

    def recalcMac(self, event):
        self.macCB.SetValue(self._MacFind(self.ageCB.GetValue(), self.agentCB.GetValue(),
            self.agentpcCB.GetValue(), self.n2opcCB.GetValue()))

    def recalcEtAgent(self, event):
        self.agentpcCB.SetValue(self._FiAgentFind(self.ageCB.GetValue(), self.agentCB.GetValue(),
            self.macCB.GetValue(), self.n2opcCB.GetValue()))
    
    def _MacFind(self, Age, volatile, FiAgent, FiN2O=0):
        N2OMac = FiN2O /  (self.Mac40N2O *  pow(10, (-0.00269 * (Age-40))))
        return N2OMac + (FiAgent /  (self.volatiles[volatile] *  pow(10, (-0.00269 * (Age-40)))))

    def _FiAgentFind(self, Age, volatile, Mac, FiN2O=0):
        N2OMac = FiN2O /  (self.Mac40N2O *  pow(10, (-0.00269 * (Age-40))))
        return (Mac - N2OMac) * (self.volatiles[volatile] *  pow(10, (-0.00269 * (Age-40))))

if __name__=='__main__':
    app = wx.App()
    MainWidget(None, title='MAC/Age Calculator')
    app.MainLoop()


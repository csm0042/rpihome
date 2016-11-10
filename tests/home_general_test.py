from unittest import TestCase
import datetime
import multiprocessing
from rpihome.rules import home_general


class TestHomeGeneral(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)         
        self.user = home_general.HomeGeneral()
        self.ip = "10.5.30.112"
        self.mac = "70:ec:e4:81:44:0f"

    def test_home_general_yes(self):
        self.user.yes = True
        self.assertEqual(self.user.yes, True)
        self.user.yes = False
        self.assertEqual(self.user.yes, False)
        self.user.yes = None
        self.assertEqual(self.user.yes, None)
        self.user.yes = 1
        self.assertEqual(self.user.yes, None)

    def test_home_general_mode(self):
        self.user.mode = 0
        self.assertEqual(self.user.mode, 0)
        self.user.mode = 1
        self.assertEqual(self.user.mode, 1)
        self.user.mode = 2
        self.assertEqual(self.user.mode, 2)
        self.user.mode = 3
        self.assertEqual(self.user.mode, 3)
        self.user.mode = 4
        self.assertEqual(self.user.mode, 4)
        self.user.mode = 5
        self.assertEqual(self.user.mode, 5)
        self.user.mode = 6
        self.assertEqual(self.user.mode, 2)
        self.user.mode = -1
        self.assertEqual(self.user.mode, 2)   

    def test_home_general_mac(self):
        self.user.mac = "hello"
        self.assertEqual(self.user.mac, "hello")  
        self.user.mac = 2.0
        self.assertEqual(self.user.mac, "00:00:00:00:00:00") 

    def test_home_general_ip(self):
        self.user.ip = "hello"
        self.assertEqual(self.user.ip, "192.168.1.1")  
        self.user.ip = "192.168.86.12"
        self.assertEqual(self.user.ip, "192.168.86.12")  
        self.user.ip = "dog"
        self.assertEqual(self.user.ip, "192.168.1.1")    

    def test_home_general_home_time(self):
        self.testDatetime = datetime.datetime.combine(datetime.date(2016,11,10), datetime.time(10,15))
        self.user.home_time = self.testDatetime
        self.assertEqual(self.user.home_time, self.testDatetime)  
        self.testDatetime = datetime.datetime.now()
        self.user.home_time = self.testDatetime
        self.assertEqual(self.user.home_time, self.testDatetime) 
        self.user.home_time = "hello"
        self.assertEqual(self.user.home_time, self.testDatetime)        

    def test_home_general_last_seen(self):
        self.testDatetime = datetime.datetime.combine(datetime.date(2016,11,10), datetime.time(10,15))
        self.user.last_seen = self.testDatetime
        self.assertEqual(self.user.last_seen, self.testDatetime)  
        self.testDatetime = datetime.datetime.now()
        self.user.last_seen = self.testDatetime
        self.assertEqual(self.user.last_seen, self.testDatetime) 
        self.user.last_seen = "hello"
        self.assertEqual(self.user.last_seen, self.testDatetime)  

    def test_home_general_last_arp(self):
        self.testDatetime = datetime.datetime.combine(datetime.date(2016,11,10), datetime.time(10,15))
        self.user.last_arp = self.testDatetime
        self.assertEqual(self.user.last_arp, self.testDatetime)  
        self.testDatetime = datetime.datetime.now()
        self.user.last_arp = self.testDatetime
        self.assertEqual(self.user.last_arp, self.testDatetime) 
        self.user.last_arp = "hello"
        self.assertEqual(self.user.last_arp, self.testDatetime)        

    def test_home_general_last_ping(self):
        self.testDatetime = datetime.datetime.combine(datetime.date(2016,11,10), datetime.time(10,15))
        self.user.last_ping = self.testDatetime
        self.assertEqual(self.user.last_ping, self.testDatetime)  
        self.testDatetime = datetime.datetime.now()
        self.user.last_ping = self.testDatetime
        self.assertEqual(self.user.last_ping, self.testDatetime) 
        self.user.last_ping = "hello"
        self.assertEqual(self.user.last_ping, self.testDatetime)    

    def test_home_general_dt(self):
        self.testDatetime = datetime.datetime.combine(datetime.date(2016,11,10), datetime.time(10,15))
        self.user.dt = self.testDatetime
        self.assertEqual(self.user.dt, self.testDatetime)  
        self.testDatetime = datetime.datetime.now()
        self.user.dt = self.testDatetime
        self.assertEqual(self.user.dt, self.testDatetime) 
        self.user.dt = "hello"
        self.assertEqual(self.user.dt, self.testDatetime) 

    def test_home_general_output(self):
        self.user.output = 1
        self.assertEqual(self.user.output, 1)
        self.user.output = "2"
        self.assertEqual(self.user.output, "2")
        self.user.output = 3
        self.assertEqual(self.user.output, 3)         

    def test_home_general_index(self):
        self.user.index = 1
        self.assertEqual(self.user.index, 1)
        self.user.index = "2"
        self.assertEqual(self.user.index, 1)
        self.user.index = 3
        self.assertEqual(self.user.index, 3)    

    def test_home_general_by_arp(self):
        self.mac = "70:ec:e4:81:44:0f"
        self.user.by_arp(mac=self.mac) 
        self.assertEqual(self.user.yes, True) 
        
        self.mac = "70:ec:e4:81:44:0a"
        self.user.last_seen = self.user.last_seen + datetime.timedelta(hours=-2)
        self.user.by_arp(mac=self.mac) 
        self.assertEqual(self.user.yes, False)                

    def test_home_general_by_ping(self):
        self.dt = datetime.datetime.now()
        
        self.ip = "10.5.30.112"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_ping(ip=self.ip)   
        self.assertEqual(self.user.yes, True) 
        
        self.ip = "192.168.86.12"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_ping(ip=self.ip)   
        self.assertEqual(self.user.yes, False)                  

    def test_home_general_by_arp_and_ping(self):
        self.dt = datetime.datetime.now()
        
        self.mac = "70:ec:e4:81:44:0f"
        self.ip = "10.5.30.112"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_arp_and_ping(mac=self.mac, ip=self.ip)  
        self.assertEqual(self.user.yes, True)   
        
        self.mac = "70:ec:e4:81:44:0a"
        self.ip = "10.5.30.112"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_arp_and_ping(mac=self.mac, ip=self.ip)  
        self.assertEqual(self.user.yes, True)    
        
        self.mac = "70:ec:e4:81:44:0a"
        self.ip = "192.168.86.12"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_arp_and_ping(mac=self.mac, ip=self.ip)  
        self.assertEqual(self.user.yes, False)                   

    def test_home_general_by_ping_w_delay(self):
        self.dt = datetime.datetime.now() + datetime.timedelta(hours=-5, days=-1)
        
        self.ip = "10.5.30.112"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_ping_with_delay(datetime=self.dt, ip=self.ip)         
        self.assertEqual(self.user.yes, True)  
        
        self.ip = "192.168.86.12"
        self.user.last_arp = self.user.last_ping = self.user.last_seen = self.dt + datetime.timedelta(hours=-2)
        self.user.by_ping_with_delay(datetime=self.dt, ip=self.ip) 
        self.assertEqual(self.user.yes, False)                                                                        

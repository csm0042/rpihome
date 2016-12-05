from unittest import TestCase
import datetime
import multiprocessing
from rpihome.home import home_user2


class TestHomeUser2(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)         
        self.user = home_user2.HomeUser2(self.testQueue)
        self.ip = "10.5.30.99"
        self.mac = "70:ec:e4:81:44:0f"

    def test_user2_mode_0(self):
        """ User mode==0 is force-away """
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(4,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(8,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(10,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(12,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(14,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(16,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(18,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(20,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=0, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(22,0)))
        self.assertEqual(self.user.yes, False)                  

    def test_user2_mode_1(self):
        """ User mode==1 is force-home """
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(4,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,0)))
        self.assertEqual(self.user.yes, True)    
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(8,0)))
        self.assertEqual(self.user.yes, True)  
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(10,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(12,0)))
        self.assertEqual(self.user.yes, True)    
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(14,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(16,0)))
        self.assertEqual(self.user.yes, True)    
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(18,0)))
        self.assertEqual(self.user.yes, True)  
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(20,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=1, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(22,0)))
        self.assertEqual(self.user.yes, True)  

    def test_user2_mode_2(self):
        """ User mode==2 is home/away based upon a typical schedule """
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(4,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,0)))
        self.assertEqual(self.user.yes, True)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(8,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(10,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(12,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(14,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(16,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(18,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(20,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(22,0)))
        self.assertEqual(self.user.yes, False) 
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(4,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(6,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(8,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(10,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(12,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(14,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(16,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(18,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(20,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(22,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(4,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(6,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(8,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(10,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(12,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(14,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(16,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(18,0)))
        self.assertEqual(self.user.yes, True)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(20,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,2), datetime.time(22,0)))
        self.assertEqual(self.user.yes, True) 
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(4,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(6,0)))
        self.assertEqual(self.user.yes, True)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(8,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(10,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(12,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(14,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(16,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(18,0)))
        self.assertEqual(self.user.yes, True)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(20,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,3), datetime.time(22,0)))
        self.assertEqual(self.user.yes, True) 
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(4,0)))
        self.assertEqual(self.user.yes, True)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(6,0)))
        self.assertEqual(self.user.yes, True)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(8,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(10,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(12,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(14,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(16,0)))
        self.assertEqual(self.user.yes, False)    
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(18,0)))
        self.assertEqual(self.user.yes, False)  
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(20,0)))
        self.assertEqual(self.user.yes, False)
        self.user.by_mode(mode=2, ip=self.ip, datetime=datetime.datetime.combine(datetime.date(2016,11,4), datetime.time(22,0)))
        self.assertEqual(self.user.yes, False)                                 

from mock import patch
from dataContract.stack import Stack
from dataContract.util import Util
from unittest import TestCase
import unittest
import mock
import random

class MyTestCase(unittest.TestCase):
    def test_addHost_name_empty(self):
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.emptyString, Util.emptyString, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == False 
    
    def test_addHost_component_null_name_equals_host(self):
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.randomString, None, Util.emptyString, Util.randomString)
    
        #assert
        assert res == True 
    
    def test_addHost_component_not_null_name_not_equals_host(self):
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.randomString, Util.randomString, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == True 
    
    def test_addHost_component_null_name_not_equals_host(self):
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.randomString, None, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == False 
       
    
    @mock.patch.object(Stack.Instance(), 'getRandomInt')
    def test_getRandomInt(self, getRandomInt_mock):
        #arrange
        s = Stack.Instance()
        getRandomInt_mock.return_value = 1
        
        #act
        res = s.getRandomInt(random.random())
    
        #assert
        assert res == 1
    

    def test_getHostList(self):
        #arrange
        s = Stack.Instance()
        s.hosts = {}
        
        #act
        res = s.getHostList()
        print 'res: ', res
    
        #assert
        assert res == []

    def test_updateServicesState(self):
         #arrange
        s = Stack.Instance()
        s.hosts = {}
        
        #act
        res = s.getHostList()
        print 'res: ', res
    
        #assert
        assert res == []

    def test_paramikoWrap(self):
        print 'test_paramikoWrap pass'
        #arrange
        s = Stack.Instance()
        
        #act
        res = s.paramikoWrap(Util.randomString, Util.randomString)
    
        #assert
        assert res == [1]

if __name__ == '__main__':
    unittest.main()

from mock import patch
from dataContract.stack import Stack
from dataContract.util import Util
from unittest import TestCase
import unittest
import mock
import random

#@mock.patch.object(Stack.Instance(), 'addHost')


class MyTestCase(unittest.TestCase):
    def test_addHost_name_empty():
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.emptyString, Util.emptyString, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == False 
    
    def test_addHost_component_null_name_equals_host():
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.randomString, None, Util.emptyString, Util.randomString)
    
        #assert
        assert res == True 
    
    def test_addHost_component_not_null_name_not_equals_host():
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.randomString, Util.randomString, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == True 
    
    def test_addHost_component_null_name_not_equals_host():
        #arrange
        s = Stack.Instance()
    
        #act
        res = s.addHost(Util.randomString, None, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == False 
    
    def test_addHost_exception():
        #arrange
        s = Stack.Instance()
    
        #act
        TestCase.assertRaises(Exception, s.addHost, Util.randomString, Util.randomString, Util.randomString, Util.randomString )
        res = s.addHost(Util.randomString, None, Util.emptyString, Util.emptyString)
    
        #assert
        assert res == False 
    
    
    
    
    @mock.patch.object(Stack.Instance(), 'getRandomInt')
    def test_getRandomInt(getRandomInt_mock):
        #arrange
        s = Stack.Instance()
        getRandomInt_mock.return_value = 1
        
        #act
        res = s.getRandomInt(random.random())
    
        #assert
        assert res == 1
    

    def test_getHostList():
         #arrange
        s = Stack.Instance()
        
        #act
        res = s.getHostList()
    
        #assert
        assert res == []
    

if __name__ == '__main__':
    MyTestCase('test_getHostList').run()


from mock import patch
from dataContract.stack import Stack
import mock
import random

@mock.patch.object(Stack.Instance(), 'addHost')
def test_getRandomInt(addHost_mock):
    s = Stack.Instance()
    addHost_mock.return_value = 1
    assert s.getRandomInt(random.random()) == 1

test_1()

@mock.patch.object(Stack.Instance(), 'getRandomInt')
def test_getRandomInt(getRandomInt_mock):
    s = Stack.Instance()
    getRandomInt_mock.return_value = 1
    assert s.getRandomInt(random.random()) == 1

test_1()


	

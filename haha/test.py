from mock import patch
from dataContract.stack import Stack
from dataContract.servicesParser import ServicesParser
import mock

@mock.patch.object(Stack, 'getRandomInt')
def test_1(getRandomInt_mock):
	h = Stack()
	assert t_mock is h.getRandomInt 

test_1()


	

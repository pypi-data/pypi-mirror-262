from unittest import TestCase

from bitcoin.address_listener.address_listener import AbstractAddressListener, AddressTxData, AddressTxType


class DummyAddressListener(AbstractAddressListener):
    def consume(self, address_tx_data):
        pass

    def __init__(self, address_to_listen: [str]):
        super().__init__(address_to_listen)


class TestAbstractAddressListener(TestCase):
    def test_filter_address_tx_data_one_address(self):
        address_listener = DummyAddressListener("3P4WqXDbSL")
        input_tx_data = [AddressTxData(tx_id="tx id", address="3P4WqXDbSL", type= AddressTxType.OUTPUT, _amount=1000)]
        address_tx_data = address_listener.filter_address_tx_data(input_tx_data)
        self.assertEqual(len(address_tx_data), len(input_tx_data))

    def test_filter_address_tx_data_multiple_addresses(self):
        address_listener = DummyAddressListener(["3P4WqXDbSL", "3P4WqXDbSL2"])
        input_tx_data = [AddressTxData(tx_id="tx id", address="3P4WqXDbSL", type= AddressTxType.OUTPUT, _amount=1000),
                         AddressTxData(tx_id="tx id", address="3P4WqXDbSL2", type= AddressTxType.OUTPUT, _amount=1000),
                            AddressTxData(tx_id="tx id", address="3P4WqXDbSL3", type= AddressTxType.OUTPUT, _amount=1000)]
        address_tx_data = address_listener.filter_address_tx_data(input_tx_data)
        self.assertEqual(len(address_tx_data), 2)
        self.assertEqual(address_tx_data[0], "3P4WqXDbSL")
        self.assertEqual(address_tx_data[1], "3P4WqXDbSL2")
        self.assertNotEquals(len(address_tx_data), len(input_tx_data))

    def test_filter_address_tx_data_empty_address_in_input(self):
        address_listener = DummyAddressListener("3P4WqXDbSL")
        input_tx_data = [AddressTxData(tx_id="tx id", address="", type= AddressTxType.OUTPUT, _amount=1000)]
        address_tx_data = address_listener.filter_address_tx_data(input_tx_data)
        self.assertEqual(len(address_tx_data), 0)
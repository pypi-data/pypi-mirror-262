import dataclasses
from abc import ABC, abstractmethod
from enum import Enum

from bitcoinlib.transactions import Transaction

from bitcoin.tx_listener.abstract_tx_listener import AbstractTxListener


class AddressTxType(Enum):
    INPUT = "input"
    OUTPUT = "output"


@dataclasses.dataclass
class AddressTxData:
    tx_id: str
    address: str
    type: AddressTxType
    # figure out the way to get amount in vin
    _amount: int = 0

    def get_amount(self):
        if self.type == AddressTxType.INPUT:
            return "Amount is not supported for input type, yet"
        return self._amount

    def amount_in_btc(self):
        if self.type == AddressTxType.INPUT:
            return "Amount is not supported for input type, yet"
        return self._amount / 100000000


class AbstractAddressListener(AbstractTxListener, ABC):
    DECIMAL_SCALE = 5

    def __init__(self, addresses_to_listen: {str}):
        self.addresses_to_listen = addresses_to_listen

    @abstractmethod
    def consume(self, subscribed_address, address_tx_data: [AddressTxData]):
        pass

    def filter_address_tx_data(self, address_tx_data: [AddressTxData]) -> [str]:
        filtered_address_tx_data = list(filter(lambda x: x.address in self.addresses_to_listen and x.address != "",
                                               address_tx_data))
        # get all address
        return list(set((map(lambda x: x.address, filtered_address_tx_data))))

    def on_tx(self, tx: Transaction):
        # get all address in the inputs and outputs along with the amount
        inputs = tx.inputs
        outputs = tx.outputs
        tx_id = tx.txid
        address_tx_data = []
        for input in inputs:
            address = input.address
            address_tx_data.append(AddressTxData(address=address,
                                                 type=AddressTxType.INPUT,
                                                 tx_id=tx_id))
        for output in outputs:
            amount = output.value
            address_tx_data.append(AddressTxData(address=output.address,
                                                 _amount=amount,
                                                 type=AddressTxType.OUTPUT,
                                                 tx_id=tx_id))

        # filter the address we are interested in
        addresses_for_events = self.filter_address_tx_data(address_tx_data)
        for address in addresses_for_events:
            self.consume(subscribed_address=address, address_tx_data=address_tx_data)

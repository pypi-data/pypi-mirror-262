from bitcoin.address_listener.address_listener import AbstractAddressListener, AddressTxData, AddressTxType


class SimpleAddressListener(AbstractAddressListener):
    def consume(self, address_tx_data: [AddressTxData]):
        for address_tx in address_tx_data:
            if address_tx.type == AddressTxType.OUTPUT:
                print(
                    f"Address {address_tx.address} received {address_tx.amount_in_btc()} BTC in tx {address_tx.tx_id}")

    def __init__(self, address):
        self.address = address
        super().__init__(address_to_listen=[address])

# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# Create a Record Data Class that consists of the `sender`, `receiver`, and `amount` attributes
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

# Modify the Existing Block Data Class to Store Record Data
@dataclass
class Block:
    # Rename the `data` attribute to `record`, and set the data type to `Record`
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    # Adding block and hash it
    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()

# Create the Chain class
@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    # Function responsible for searching winning hash, adding block to the chain, and validating the chain
    def proof_of_work(self, block):
        calculated_hash = block.hash_block()
        num_of_zeros = "0" * self.difficulty

        # Checking for winning hash
        while not calculated_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()

        print("Winning Hash", calculated_hash)
        return block

    # Adding block to the chain
    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    # Checking the chain
    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block(Record("Genesis", "None", 0.0), 0)])

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

# Add Relevant User Inputs to the Streamlit Interface

# Default sender name is "Neha"
sender_name = "Neha"

# Add an input area where you can get a value for `receiver` (Receiver Name)
receiver_name = st.text_input("Receiver Name")

# Add an input area where you can get a value for `customer_id` (Customer ID)
customer_id = st.text_input("Customer ID")

# Add an input area where you can get a value for `transaction_amount`
transaction_amount = st.number_input("Transaction Amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Update `new_block` to use the updated inputs
    new_block = Block(
        record=Record(sender=sender_name, receiver=f"{receiver_name} (ID: {customer_id})", amount=transaction_amount),
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

################################################################################
# Streamlit Code (continues)

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

# Visualization of the blocks
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

# Action - validate chain
if st.button("Validate Chain"):
    check = pychain.is_valid()
    if check:
        st.write("Blockchain is Valid")
    else:
        st.write("Blockchain is Invalid")

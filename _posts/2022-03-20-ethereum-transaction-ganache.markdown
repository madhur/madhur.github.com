---
layout: blog-post
title: "Execute a transaction in etherum using ganache"
excerpt: "Execute a transaction in etherum using ganache"
disqus_id: /2022/03/20/ethereum-transaction-ganache/
tags:    
    - Ehtereum
    - Ganache
    - Blockchain
---

Compared to [Bitcoin](https://bitcoin.org/en/), [Ethereum](https://ethereum.org/en/) provides a good set of development tools to get up and running with executing transactions in Ethereum [blockchain](https://www.blockchain.com/explorer).

Here is an example of a simple transaction done in ethereum using [Ganache](https://trufflesuite.com/ganache/index.html)

The same can easily be modified to point to [Infura](https://infura.io/)

```javascript
var Web3 = require('web3');
var EthereumTransaction = require('ethereumjs-tx').Transaction;
var web3 = new Web3('http://127.0.0.1:7545');

var sendingAddress = '0xaB549b951d2ebFd71B506bc14BF743A8879F5130';
var receivingAddress = '0x9E0F9ccA3B3FE51028660798c7bd6455bF9c3899';


web3.eth.getBalance(sendingAddress).then(console.log);
web3.eth.getBalance(receivingAddress).then(console.log);

var rawTransaction = {
    nonce: 1,
    to: receivingAddress, 
    gasPrice: 20000000,
    gasLimit: 30000,
    value: 1,
    data: "0x"
}


var privateKeySender = 'xxxxx';
var privateKeySenderHex = new Buffer(privateKeySender, 'hex')
var transaction = new EthereumTransaction(rawTransaction);
transaction.sign(privateKeySenderHex);


var serializedTransaction = transaction.serialize();
web3.eth.sendSignedTransaction(serializedTransaction);
```

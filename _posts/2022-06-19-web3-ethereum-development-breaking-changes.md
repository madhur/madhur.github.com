---
layout: blog-post
title: "Web3 ethereum development breaking changes"
excerpt: "Web3 ethereum development breaking changes"
disqus_id: /2022/06/19/web3-ethereum-development-breaking-changes/
tags:    
    - Web3
    - Ethereum
---

Web3 development scene is changing very fast with lot of breaking changes getting introduced every few months.
This makes it very difficult to follow any online tutorial which was written few months back.

This post itself will become obsolete after few months. As of this writing, I am using Solidity compiler version 0.8.15

```
pragma solidity ^0.8.4;
```

In this post, I will outline few of the breaking changes I have encountered when working with web3 and ethereum:



* `address` and `address payable` are two different data types.

```
address public manager;
address payable[] public players;
```

You can call `transfer` and `send` function only on `address payable` and not on `address`.


* Compiling the solidity contract

Compiling the solidity contract has changed in recent versions.


```javascript
const path = require("path");
const fs = require("fs");
const solc = require("solc");

const inboxPath = path.resolve(__dirname, "contracts", "Lottery.sol");
const source = fs.readFileSync(inboxPath, "utf8");

var input = {
  language: "Solidity",
  sources: {
    "Lottery.sol": {
      content: source,
    },
  },
  settings: {
    outputSelection: {
      "*": {
        "*": ["*"],
      },
    },
  },
};
var output = JSON.parse(solc.compile(JSON.stringify(input)));
module.exports.abi = output.contracts["Lottery.sol"]["Lottery"].abi;
module.exports.bytecode = output.contracts["Lottery.sol"]["Lottery"].evm.bytecode.object;
```

In order to deploy this contract:


```javascript
await new web3.eth.Contract(abi).deploy({data: bytecode, arguments: []})
```

* `keccak256` now takes only one argument 

```javascript
function random() public view returns (uint) {
       return uint(keccak256(block.difficulty, block.timestamp, players));
}
```

to 

```javascript
function random() public view returns (uint) {
       return uint(keccak256(abi.encodePacked(block.difficulty, block.timestamp, players)));
}
```

* The constructor function is now written with name `constructor` instead of function with name of contract

```javascript
constructor() {
       manager = msg.sender;
}
```
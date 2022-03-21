# Running a Lighthouse client for GBC

This document describes how to run Lighthouse beacon node for the Gnosis Beacon Chain.

## Assumptions
* This document assumes that you already have an xDai node available for your use (or public JSON RPC endpoint)
* You have a persistent linux VM with docker installed on it, which is accessible from the public internet via a fixed IP address. We recommend using a VM with at least 4 vCPU, 8 GB RAM, 100 GB SSD

## Configuration
1) Create an empty directory somewhere on the VM (e.g. `/opt/gbc`)
2) Clone the repository with all necessary configs:
```bash
cd /opt/gbc
git clone -b bn-wo-vc https://github.com/gnosischain/lighthouse-launch .
```
3) Create `.env` file from the example at `.env.example`. Put xDAI RPC url in the config and add a new line to define the parameter PUBLIC_IP with the valid external IP address of your VM. Other values can be left without changes.

## Running node
1) Run the following command to start the beacon node:
```bash
docker-compose up -d
```

## Getting metrics
1) The prometheus like metrics are available by `http://public_ip:5054/metrics`

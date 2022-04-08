# Running a Lighthouse client for GBC

This document describes how to run Lighthouse beacon node + Lighthouse validator for the Gnosis Beacon Chain.

See a similar repo with Prysm node setup - https://github.com/gnosischain/prysm-launch

## Assumptions
* This document assumes that you already have an xDai node available for your use (or public JSON RPC endpoint)
* You have already generated your validator accounts using the fork of the official deposit-cli - https://github.com/gnosischain/deposit-cli. You will need validator keystores and passwords for them to run the validator client.
* You might start your node and validator first, and only them make a deposit, once everything works.
* You have a persistent linux VM with docker installed on it, which is accessible from the public internet via a fixed IP address. We recommend using a VM with at least 4 vCPU, 8 GB RAM, 100 GB SSD

## Configuration
1) Create an empty directory somewhere on the VM (e.g. `/root/gbc`)
2) Clone the repository with all necessary configs:
```bash
cd /root/gbc
git clone https://github.com/gnosischain/lighthouse-launch .
```
3) Copy all validators keystore files to the `./keys/validator_keys` directory. Ensure that copied keystores are only used on a single VM instance.
4) Write keystore password to the `./keys/keystore_password.txt` file
5) Create `.env` file from the example at `.env.example`. Put the valid external IP address of your VM and an xDAI RPC url in the config. Other values can be left without changes.
6) Modify `./config/graffiti.yml`, if needed. (See https://lighthouse-book.sigmaprime.io/graffiti.html for file format description)

If it is required to send the node and validator logs to a remote syslog server the following actions can be done (it is assumed that the node and validator will be run by using the `docker-compose-syslog.yml` file with the `docker-compose` command in the instructions below).

7) Copy `./syslog/etc/logrotate.d/docker-logs` to `/etc/logrotate.d/`.
8) Copy `./syslog/etc/rsyslog.d/30-gbc-local.conf` and `./syslog/etc/rsyslog.d/35-gbc-remote-logging.conf` to `/etc/rsyslog.d/`.
9) Modify `target` and `port` in `/etc/rsyslog.d/35-gbc-remote-logging.conf` to point to a remote syslog server.
10) Restart the rsyslog service by `systemctl restart rsyslog`.

## Import of validator keys
1) Run the following command to import and all added keystore files:
```bash
docker-compose up validator-import
```

## Running node
1) Run the following command to start the beacon node:
```bash
docker-compose up -d node
docker-compose logs -f node
```

If you would like to run a slasher together with your node, you can run the following commands instead:
```bash
docker-compose up -d node-private-slasher
docker-compose logs -f node-private-slasher
```
This will run a node with the historical slasher db for private use only,
meaning that found slashings will NOT be broadcasted to other peers.

Alternatively, if you want to broadcast found slashings to other peers, (e.g. if you do not plan to run validators, or want to contribute to network health):
```bash
docker-compose up -d node-public-slasher
docker-compose logs -f node-public-slasher
```

2) Your node should find other peers and start syncing with the rest of the network

## Running validator
1) Run the following command to start the validator client:
```bash
docker-compose up -d validator
docker-compose logs -f validator
```

## Collecting metrics
1) Run the following command to start the prometheus server, it will allow to use grafana's dashboards (configured separately):
```bash
docker-compose up -d prometheus
```

If the node is run by `node-private-slasher` or `node-public-slasher`, replace `node` in `depends_on` section of the prometheus service in the docker compose file to specify proper set of services to run.

## Update repository to a newer version
Update repository configs to a newer version should be as easy as pulling new changes from the repo and restarting the node.
For example, the following sequence of commands should work in most of the cases. 
```bash
git pull
docker-compose down --remove-orphans
docker-compose up -d node validator prometheus
```

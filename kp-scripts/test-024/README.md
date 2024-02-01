# TX pre-genereation (program deployments)

Generate a large number of program deployments for a specific devnet size out of one program.

1) Set up a large aws machine (e.g., c7a.metal-48xl)
    * To connect to it, run ssh ubuntu@IP
2) Install snarkOS and the tx cannon
3) switch to the root user: sudo -i
3) Run 01_tx_pregeneration.py
    * The first time you run it, only create a very small number of txs in parallel, since it needs to download field elements and would do that in parallell
    * On c7a.metal-48xl, 8 txs in parallel is a good value
4) Download with 02_copy_transactions_from_aws.sh
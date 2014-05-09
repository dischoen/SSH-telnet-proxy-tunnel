SSH-telnet-proxy-tunnel
=======================

Tunnel SSH connections through a telnet tunnel

This script is based on tunnel.py by Urban Kaveus and Simon Josefsson.
I used tunnel.py for years to get out of our company network.
For quite some time now I am mostly working inside of virtual machines,
and I experienced problems: sometimes it worked,
sometimes it simply did not connect to the remote machine.

Since I do not speak perl, I converted the script to Python.
On the way, I also switched from fork() to select().

By the way, I used the script to get the initial repository from
github on my VM.

I would like to get your feedback on it.

## Requirements:

Your company telnet proxy should expect a connect string in this format:

    connect <hostname> [port]

## Usage:

1 Copy tunnel.py on your machine, e.g. in ~/bin and make it executable.
2 In your ~/.ssh/config:

    Host ext1
    HostName ext1_and_more.noip.me
    ProxyCommand $HOME/bin/tunnel.py proxy.company.net 23 %h %p

3 Use it:

    $ ssh ext1

I think, that's it.

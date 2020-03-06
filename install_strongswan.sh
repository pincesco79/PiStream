apt-get install -t jessie strongswan
apt-get install -t jessie libcharon-extra-plugins

#Edit /etc/ipsec.conf and add the following: 

config setup
    cachecrls=yes
    uniqueids=yes

conn ios
    keyexchange=ikev1
    authby=xauthpsk
    xauth=server
    left=%defaultroute
    leftsubnet=0.0.0.0/0
    leftfirewall=yes
    right=%any

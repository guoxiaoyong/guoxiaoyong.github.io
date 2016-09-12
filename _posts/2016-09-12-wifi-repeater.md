---
layout: post
title: "Make Your Laptop a WiFi Repeater"
date: 2016-09-12 09:42:26 +0800
categories: WiFi 
---

**Xiaoyong Guo**

I have a wireless cable modem provided by my ISP.
Although my apartment is rather small,
I still cannot connect to the network from my bedroom since the signal from the wireless cable modem is very weak.
So I decided to use my Gateway NE71B laptop as a WiFi repeater to extend the signal coverage.

My Gateway NE71B laptop is equipped with a Qualcomm Atheros AR9485 WiFi card and has Fedora 22 running on it.
Following is a list of softwares you need to setup a WiFi repeater.

1. iw
2. ifconfig 
3. hostapd
4. wpa_supplicant 
5. wpa_passphrase
6. iptables


Now we can start to configure the laptop to a WiFi repeater.
First you have to stop NetworkManager service,
otherwise it will conflict with the configurations you do to the wireless device.

```
service NetworkManager stop
```

Second, create two wireless interfaces called `sta` and `ap`. 
`sta` will run in station mode, and connect to my wireless cable modem,
and `ap` will run in AP mode, which acts as a access point.
Use `iw` tool to do these configurations as follows:

```
iw dev wlp3s0 del
iw phy0 interface add dev sta 
iw phy0 interface add dev ap
```

Note that I also delete the wireless device `wlp3s0`.
This step is not necessary.
I did it because I want to name the virtual wireless interface in my own way.
Like many other Linux distributions, Fedora used to give WiFi device names such as `wlan0`, `wlan1`.
This convention is changed.
Some of the reason for adopting the naming convention by Fedora 22 can be found 
[here](http://unix.stackexchange.com/questions/131224/how-does-fedora-name-wireless-interfaces)

Since the two network interfaces `sta` and `ap` have the same MAC address (the two have the same underlying physical device), 
you have to change one of them to a difference MAC address.
For my laptop, the two virtual WiFi interfaces 
have the same MAC address `44:6d:57:b5:dd:0b`,
so I changed one to `44:6d:57:b5:dd:0e`.

Next, you need to connect the interface `sta` to the wireless cable modem using the tool
`wpa_supplicant` and `wpa_passphrase`. Use `wpa_passphrase` to generate a configuration that
will be used by `wpa_supplicant` later. You can also create this file manually.


```
wpa_passphrase ssid password
```

which gives

```
network={
    ssid="ssid"
    #psk="password"
    psk=44116ea881531996d8a23af58b376d70f196057429c258f529577a26e727ec1b
}

```

Save the output to a file named `wpa_supplicant.conf`, and run the command

```
wpa_supplicant -B -D nl80211 -i sta -c wpa_supplicant.conf
```

Then the interface `sta` will be connected to the wireless cable modem.
After the wireless connection is established. We have to setup
the IP address of `sta`, the routing table and DNS entry in `/etc/resolv.conf`.
Of course we can do it manually. But a much easy way is to use `dhclient` to 
obtain the configuration parameters via DHCP protocol and then do all the settings automatically.
Simply run the command

```
dhclient sta
```

After `sta` is properly set, we need to bring up the `ap` interface using `hostapd`.
configure IP address of ap
First we have to write a configuration file for hostapd.
The following is a minimalist configuration file for hostapd.

```
interface=ap
ssid=myap
channel=11
hw_mode=g
ieee80211n=1
wpa=3
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
wpa_passphrase=mypasswd
```

Save the configuration to a file `hostapd.conf`, and run the command

```
hostapd -B hostapd.conf
```

to bring up the interface `ap`.
Then use `ifconfig` to assign an IP address for `ap`

```
ifconfig ap 192.168.10.1
```

Then we have to bring up dnsmasq to provide DHCP service.

```
dhcp-range=192.168.10.100,192.168.10.200,255.255.255.0,12h
```

```
dnsmasq -C dnsmasq.conf -l /tmp/dhcp.leases
```

Now WiFi clients can connect to this WiFi repeater.

The last step is to setup a NAT. This is quite simple, just run the command

```
iptables -t nat -A POSTROUTING -j MASQUERADE
```

## References
[hostapd.conf](https://w1.fi/cgit/hostap/plain/hostapd/hostapd.conf)


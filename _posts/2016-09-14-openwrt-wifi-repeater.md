---
layout: post
title: "WiFi Repeater Configuration using OpenWRT"
date: 2016-09-14 14:45:01 +0800
categories: C++
---

**Xiaoyong Guo**

I just found an old wireless router 
I flashed a openwrt I compiled for it more than a year ago. 
So I decided to configure it to a WiFi repeater.


## Step 1
Make changes to `/etc/config/wireless`,
you need an `AP` mode interface and
a `station` mode interface. 

```
config wifi-device  radio0
        option type     mac80211
        option channel  11
        option hwmode   11g
        option path     'pci0000:00/0000:00:11.0'
        option htmode   HT20

config wifi-iface
        option device   radio0
        option network  lan
        option mode     ap
        option ssid       'myssid'
        option encryption 'psk' 
        option key        'mypassword'
        
config wifi-iface
        option device   radio0
        option network  wlan
        option mode       sta
        option ssid       'ssid'
        option encryption 'psk'
        option key        'password'
```

## Step 2

Add one interface configuration in `/etc/config/network`

```
config interface 'wlan'
        option ifname 'wlan0'
        option proto 'dhcp'
```

This tells openwrt to use DHCP protocol to configure wlan0 interface.
Note that the `AP` interface's name is `wlan0-1`, while the `Station` interface's name is `wlan0`.

## Step 3

remove all firewall rules in `/etc/config/firewall`.

## Step 4

Add one line in `/etc/rc.local`

```
iptables -t nat -A POSTROUTING -j MASQUERADE
```

This is should be added to `/etc/firewall.user`. But somehow this does not work.



title: WiFi Repeater Configuration using OpenWRT
date: 2016-09-14 14:45:01 +0800
author: Xiaoyong Guo


I just found an old wireless router NetGear WNDR3700 from a storage box. 
The router is flashed to an openwrt firmware I compiled for it about 20 months ago. 
Since [use a laptop as a WiFi repeater]({filename}/blog/2016-09-12-wifi-repeater.md) is too heavy-handed.
So I decided to replace my laptop WiFi repeater with this wireless router.

This steps to configure a wireless router to a WiFi repeater are listed below.

**Step 1**: Make changes to `/etc/config/wireless`,
you need an `AP` mode interface and a `station` mode interface. 
Following is my `/etc/config/wireless` configuration file.


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

**Step 2**: Add one interface configuration in `/etc/config/network`

```
config interface 'wlan'
        option ifname 'wlan0'
        option proto 'dhcp'
```

This tells openwrt to use DHCP protocol to configure wlan0 interface.
Note that the interface name `wlan` should be consistent with the name given in `/etc/config/wireless`.
Using `iwconfig` and `ifconfig` tools you can see there are two wireless interfaces `wlan0` and `wlan0-1`,
and the `Station` interface's name is `wlan0`, so `AP` interface's name is `wlan0-1`. 

**Step 3**: Remove all firewall rules in `/etc/config/firewall`.

**Step 4**: Add one line in `/etc/rc.local`

```
iptables -t nat -A POSTROUTING -j MASQUERADE
```

This is should be added to `/etc/firewall.user`. But somehow this does not work.



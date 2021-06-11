# `lockss-installer` Release Notes

## Changes Since LOCKSS Installer version 2.0-alpha3

*   Switched Microk8s kubernetes to K3s kubernetes.
*   Support alternative kubernetes installs    
*   Add wait to start command that notifies when pods are reachable
*   Add solr user name and password
*   Add script to remove microk8s install and optionally snapd    
*   Add script to configure firewall on multiple linux systems
*   Add script to bring up a local dashboard
*   Enable SSL LCAP support

## 2.0.4.0

### Features

*   Add log file for install scripts
*   Notify user when pods are marked ready on start 
*   Notify user when deployments have exited on stop
*   Generate a k8s config file to support alternative k8s install
*   Enable SSL LCAP if keystores and password found in ~lockss/config/keys
*   Add logging support for pywb, openwayback and postgres

### Fixes

*   Speed up stop script
*   More robust firewall and dns checking
*   Impoved timezone support    
*   Improve script to generate alternate resolv.conf for core dns

### Security
*   Containers no longer run as root
*   User lockss no longer requires sudo privilages    
*   Firewall support reinstated
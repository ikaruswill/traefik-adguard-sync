# traefik-adguard-sync
A simple python script to sync your Traefik TLS certificates to AdGuardHome for DNS-over-TLS.

Meant to be used in a Kubernetes cluster with Traefik and AdGuardHome deployments, as a CronJob to periodically update TLS certs in AdGuardHome.

## Usage
1. Modify [cronjob.yml](https://raw.githubusercontent.com/ikaruswill/traefik-adguard-sync/master/deploy/cronjob.yml), to change the `PersistentVolumeClaim` names `traefik`, `adguard` to the ones you use.
2. Deploy!
import argparse
import base64
import json
import logging
import os

import yaml


def configure_yaml():
    def str_presenter(dumper, data):
        if len(data.splitlines()) > 1:  # check for multiline string
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    yaml.add_representer(str, str_presenter)


def read_traefik(traefik_path):
    logger.info('Reading Traefik configuration')
    with open(traefik_path, 'r') as f:
        acme_config = json.load(f)
    cert = base64.b64decode(
        acme_config['default']['Certificates'][0]['certificate']).decode('utf-8')
    private_key = base64.b64decode(
        acme_config['default']['Certificates'][0]['key']).decode('utf-8')
    return cert, private_key


def write_adguardhome(adguardhome_path, cert, key):
    logger.info('Reading AdGuardHome configuration')
    with open(adguardhome_path, 'r+') as f:
        adguardhome_config = yaml.load(f, Loader=yaml.Loader)
        adguardhome_config['tls']['certificate_chain'] = cert
        adguardhome_config['tls']['private_key'] = key
        f.seek(0)
        logger.info('Writing AdGuardHome configuration')
        yaml.dump(adguardhome_config, f)


def fix_permissions(adguardhome_path):
    logger.info('Fixing AdGuardHome permissions')
    # os.chmod(adguardhome_path, mode=0o644)
    # os.chown(adguardhome_path, uid=0, gid=0)



def run(traefik_path, adguardhome_path):
    logger.info('Initializing...')
    configure_yaml()
    cert, key = read_traefik(traefik_path)
    write_adguardhome(adguardhome_path, cert, key)
    fix_permissions(adguardhome_path)
    

def main():
    parser = argparse.ArgumentParser(
        prog='traefik-adguard-sync', 
        description='Sync TLS Certificates from Traefik to Adguard')
    parser.add_argument(
        '--traefik-path', 
        help='Path to traefik\'s acme.json file',
        default='/acme.json')
    parser.add_argument(
        '--adguardhome-path', 
        help='Path to AdGuard Home\'s AdGuardHome.yaml file',
        default='/AdGuardHome.yaml')
    args = parser.parse_args()
    run(**vars(args))

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    main()

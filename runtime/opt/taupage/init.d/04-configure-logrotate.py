#!/usr/bin/env python3

import logging
import sys
import os
import json
import taupage

CRON_TEMPLATE="*/{interval} * * * *   root    /usr/local/sbin/_logrotate"

def logrotate_interval(config):
    result = config.get('logrotate_interval_minutes')
    if result is not None:
        try:
            result = int(result)
            if result < 1 or result >= 60:
                raise ValueError("logrotate_interval_minutes must be between 1 and 59")
            return result
        except ValueError as e:
            logging.error("Invalid configuration for logrotate_interval_minutes")
            logging.exception(e)

def main():
    taupage.configure_logging()
    config = taupage.get_config()

    interval = logrotate_interval(config)
    if interval:
        logging.info("Reconfiguring logrotate to run every {} minutes".format(interval))
        with open("/etc/cron.d/logrotate", "w") as f:
            f.write(CRON_TEMPLATE.format(interval=interval))

if __name__ == '__main__':
    main()

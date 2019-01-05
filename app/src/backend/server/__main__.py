import os
import signal
import logging
import argparse
import pkg_resources

import bjoern

from backend.wsgi import application

from . argparse import Environment

logging.basicConfig()
logger = logging.getLogger('wsgi-server')


def configure_logger(opts):
    logger.setLevel(getattr(logging, opts.log_level.upper()))


def get_host_and_port(opts):
    host, port = opts.bind.split(':')
    return host, int(port)


def _get_wsgi_server_version():
    try:
        return pkg_resources.get_distribution('bjoern').version
    except pkg_resources.DistributionNotFound:
        return '<NotFound>'


def main_loop(opts):
    logger.info(
        'Starting bjoern wsgi server: {}'.format(_get_wsgi_server_version())
    )
    worker_pids = []
    host, port = get_host_and_port(opts)

    logger.info("Listening: {host}:{port}".format(host=host, port=port))
    bjoern.listen(application, host, port)
    for worker_id in range(opts.workers):
        pid = os.fork()
        if pid > 0:
            # in master
            worker_pids.append(pid)
        elif pid == 0:
            # in worker
            logger.info('registering worker-{}'.format(worker_id))
            bjoern.run()
            exit()

    try:
        for _ in range(opts.workers):
            os.wait()
    #: redundant, however it could be rewritten to use out of main signal
    except KeyboardInterrupt:
        for pid in worker_pids:
            os.kill(pid, signal.SIGINT)
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog='wsgi-server',
        description=(
            "WSGI server runner, note that it works only with libev "
            "integration (provided by bjoern wsgi server). So in case "
            "if you don't have libev or your would like to use something "
            "else consider to use gunicorn/uwsgi."
        )
    )
    parser.add_argument(
        '--bind', dest='bind', default='0.0.0.0:8000',
        action=Environment, env_name='WSGI_SERVER_BIND',
        help='address:port, default: %(default)s, env: WSGI_SERVER_BIND',
        type=str
    )
    parser.add_argument(
        '-w', '--workers', dest='workers', default=2, type=int,
        action=Environment, env_name='WSGI_SERVER_WORKERS',
        help='amount of workers, default: %(default)s; '
             'env: WSGI_SERVER_WORKERS'
    )
    parser.add_argument(
        '--log-level', dest='log_level', default='info',
        choices=('info', 'warning', 'debug', 'error', 'critical'),
        action=Environment, env_name='WSGI_SERVER_LOG_LEVEL',
        help='log level, default: %(default)s; env: WSGI_SERVER_LOG_LEVEL'
    )
    arguments = parser.parse_args()
    configure_logger(arguments)
    main_loop(arguments)


if __name__ == '__main__':
    main()

# coding: utf-8
import subprocess
import Queue
import time

from dext.settings import settings

from the_tale.amqp_environment import environment

from the_tale.common.utils.workers import BaseWorker
from the_tale.common import postponed_tasks
from dext.common.utils.logic import run_django_command


class Worker(BaseWorker):
    STOP_SIGNAL_REQUIRED = False

    def run(self):
        while not self.exception_raised and not self.stop_required:
            try:
                self.logger.info('wait for amqp command')
                cmd = self.command_queue.get(block=True, timeout=60)

                settings.refresh()
                self.process_cmd(cmd.payload)
            except Queue.Empty:
                self.logger.info('try to run command')
                settings.refresh()
                self.run_commands()


        while not self.exception_raised and not self.stop_required:
            cmd = self.command_queue.get(block=True)
            self.process_cmd(cmd.payload)

    def initialize(self):
        pass

    def cmd_initialize(self, worker_id):
        self.send_cmd('initialize', {'worker_id': worker_id})

    def process_initialize(self, worker_id):

        if self.initialized:
            self.logger.warn('WARNING: long commands already initialized, do reinitialization')

        postponed_tasks.autodiscover()

        self.initialized = True
        self.worker_id = worker_id

        self.logger.info('LONG COMMANDS INITIALIZED')

        environment.workers.supervisor.cmd_answer('initialize', self.worker_id)

    def _try_run_command_with_delay(self, cmd, settings_key, delay):
        if time.time() - float(settings.get(settings_key, 0)) > delay:
            settings[settings_key] = str(time.time())
            cmd()
            return True

        return False

    def run_commands(self):
        return


    def cmd_stop(self):
        return self.send_cmd('stop')

    def process_stop(self):
        self.initialized = False
        self.stop_required = True
        environment.workers.supervisor.cmd_answer('stop', self.worker_id)
        self.logger.info('LONG COMMANDS STOPPED')

    def _run_django_subprocess(self, name, cmd):
        self.logger.info('run %s command' % name)
        result = run_django_command(cmd)
        if result:
            self.logger.error('%s ENDED WITH CODE %d' % (name, result))
        else:
            self.logger.info('%s command was processed correctly' % name)

    def _run_system_subprocess(self, name, cmd):
        self.logger.info('run %s command' % name)
        result = subprocess.call(cmd)
        if result:
            self.logger.error('%s ENDED WITH CODE %d' % (name, result))
        else:
            self.logger.info('%s command was processed correctly' % name)

    def run_update_map(self):
        self.logger.info('update map')
        self._run_django_subprocess('update map', ['map_update_map'])
        environment.workers.supervisor.cmd_highlevel_data_updated()
        self.logger.info('map updated')


    def cmd_update_map(self):
        return self.send_cmd('update_map')

    def process_update_map(self):
        self.run_update_map()

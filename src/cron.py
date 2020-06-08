# ''' Trigger this script from cron.sh or source your venv and run'''
# from crontab import CronTab
# import os
# import platform

# VENV_PATH_EXECUTABLE = os.environ['VIRTUAL_ENV'] + '/bin/python'

# FILE_PATH = os.path.abspath(__file__).split('/')[:-1] # relative, removes last every time
# FILE_PATH = "/".join(FILE_PATH)

# LOG_FILE = os.getcwd() + '/cronlog.txt 2>&1'

# FILE_TARGET = '/watcher.py'
# FILE_TARGET = FILE_PATH + FILE_TARGET

# class CronManager:
#     def __init__(self):
#         self.cron = CronTab(user=True)

#     def add_job(self, cmd=None, comment='', user=True, minute=1):
#         ''' Adds a job to crontable. '''
#         cron_job = self.cron.new(command=cmd, comment=comment, user=user)
#         if CronManager.validity_check(cron_job) == True:
#             cron_job.minute.every(minute)
#             CronManager.enable_job(cron_job)
#             self.cron.write()
#             print(f"Adding Job: {cron_job}")
#             return True
#         return False

#     def show_all_jobs(self):
#         ''' Prints all jobs. '''
#         print(f"\n\t\t\t\t{'*'*25}ALL JOBS{'*'*25}\n{self.cron.render()}")

    # def get_all_jobs(self):
    #     ''' Returns all jobs. '''
    #     return self.cron

    # def find_job_by_comment(self, comment=None):
    #     ''' Returns job if found - no jobs should have same comment. '''
    #     for job in self.cron:
    #         if str(job.comment) == (comment):
    #             return job
    #     return None

    # @staticmethod
    # def validity_check(job):
    #     ''' Returns whether job command is valid. '''
    #     if job.is_valid() == True:
    #         return True
    #     return False

    # @staticmethod
    # def disable_job(cron_manager, job):
    #     print('Job Disabled')
    #     job.enable(False)
    #     cron_manager.cron.write()

    # @staticmethod
    # def enable_job(cron_manager, job):
    #     print('Job Enabled')
    #     job.enable(True)
    #     cron_manager.cron.write()

    # @staticmethod
    # def get_enable_status(job):
    #     print(f"Current Enabled Status: {job.is_enabled()}")
    #     return job.is_enabled()

    # @staticmethod
    # def remove_job(cron_manager, job):
    #     print(f'Job Removed: {job}')
    #     cron_manager.cron.remove(job)
    #     cron_manager.cron.write()

    # @staticmethod
    # def remove_all_jobs(cron_manager):
    #     print('All Jobs Removed.')
    #     cron_manager.cron.remove_all()
    #     cron_manager.cron.write()

    # @staticmethod
    # def run_job(job):
    #     ''' A dry run '''
    #     job_standard_output = job.run()
    #     print(f"job_standard_output --> {job_standard_output}")


# cron = CronManager()
# cron.add_job(cmd=f'{VENV_PATH_EXECUTABLE} {FILE_TARGET} >> {LOG_FILE}', comment='gmail lead watcher', minute=1)


# sudo crontab -u ec2-user -e


from log import get_logger
from datetime import datetime

log = get_logger(
    "cron.py",
    "'[%(levelname)s] [%(name)s] [%(asctime)s] [%(funcName)s::%(lineno)d] [%(message)s]'",
)

def run(event=None, context=None):
    log.info(f"Engine is running. Event --> {event}.")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    return "success"
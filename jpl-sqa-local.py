#!/usr/bin/env python3

import argparse
import logging
import os
import random
import subprocess
import sys
import yaml

# configure python logger
# options: DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
logger = logging.getLogger('__name__')
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')
logger.setLevel(20)

# SQA QC.Criteria:
# see https://indigo-dc.github.io/jenkins-pipeline-library/stable/2.0.0/user/config_file.html#sqa-criteria
qc_criteria = ["qc_style", "qc_coverage", "qc_functional", "qc_security", "qc_doc"]
# testing container name:
testing_container = "testing-" + str(random.randint(10000,20000))

def command_call(cmd):
    """ Function to call command-line in shell
    """
    logger.info(f"Executing: {cmd}")
    # constantly read Subprocess output while process is running
    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    with subprocess.Popen(
               cmd,
               shell=True,  # nosec
               stdout=subprocess.PIPE,
               env=dict(os.environ, **{"BUILD_TAG": testing_container}),
               text=True,
           ) as proc:
        for line in proc.stdout:
            print(line, end='') # cmd output line

    exit_status = proc.returncode
    logger.info(f"exit_status: {exit_status}")

    return exit_status


def main():
    """ The script to run SQA QC.Criteria tests locally
        using SQA configuration files
    """
    # let's check for 'docker compose'
    cmd = "docker compose version"
    exit_status = command_call(cmd)
    if exit_status != 0:
        logger.error("You probably need to install or update docker!")
        sys.exit()

    # read SQA config_file (default .sqa/config.yml)
    config = yaml.safe_load(open(args.sqa_config))

    # First create testing container:
    logger.info(f'Creating {testing_container} container for testing...')
    cmd = f"""docker compose -f {args.sqa_docker_compose} \
--project-directory $PWD up --build -d"""
    command_call(cmd)

    # Search for SQA QC.Criterion
    qc_criteria_search = qc_criteria
    if (args.qc_criterion != None) :
        qc_criteria_search = [args.qc_criterion]
    for cr in qc_criteria_search:
        if (cr in config['sqa_criteria']):
            logger.info(f"Found {cr} criteria...")
            qc_cr_dict = config['sqa_criteria'][cr]['repos']
            qc_cr_repo = list(qc_cr_dict.keys())[0]
            qc_cr_container = qc_cr_dict[qc_cr_repo]['container']
            if ('tox' in qc_cr_dict[qc_cr_repo]):
                tox_env = qc_cr_dict[qc_cr_repo]['tox']['testenv']
                tox_file = 'tox.ini'
                if 'tox_file' in qc_cr_dict[qc_cr_repo]['tox']:
                    tox_file = qc_cr_dict[qc_cr_repo]['tox']['tox_file']
                for e in tox_env:
                    cmd = f"""docker compose -f {args.sqa_docker_compose} \
--project-directory $PWD exec -T {qc_cr_container} tox -c {tox_file} -e {e}"""
                    command_call(cmd)

            if ('commands' in qc_cr_dict[qc_cr_repo]):
                commands = qc_cr_dict[qc_cr_repo]['commands']
                for c in commands:
                    cmd = f"""docker compose -f {args.sqa_docker_compose} \
--project-directory $PWD exec -T {qc_cr_container} {c}"""
                    command_call(cmd)

    # Remove created .tox folder
    answer = input(f"[INFO] Do you want to remove .tox folder \
to save space? Enter 'y' or 'n': ")
    if answer.lower() == "y":
        logger.info(f"Removing .tox folder ...")
        cmd = f"docker exec -ti {testing_container} rm -rf .tox"
        exit_code = command_call(cmd)
        if exit_code == 0:
            logger.info(f".tox folder is successfully removed!")
    elif answer.lower() == "n":
        logger.info(f".tox folder remains on the system")
    else: print("Please enter 'y' or 'n'.")

    # Remove created container
    answer = input(f"[INFO] Do you want to remove \
testing container {testing_container}? Enter 'y' or 'n': ")
    if answer.lower() == "y":
        logger.info(f"Stopping container {testing_container} ...")
        cmd = f"docker stop {testing_container}"
        command_call(cmd)
        cmd = f"docker rm {testing_container}"
        exit_code = command_call(cmd)
        if exit_code == 0:
            logger.info(f"Container {testing_container} successfully removed!")
    elif answer.lower() == "n":
        logger.info(f"Container {testing_container} continues to run")
    else: print("Please enter 'y' or 'n'.")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run SQA QC.Criteria tests locally')
    parser.add_argument("--sqa-config", type=str, default=".sqa/config.yml",
		help="SQA config file (default: %(default)s)")
    parser.add_argument("--sqa-docker-compose", type=str, default=".sqa/docker-compose.yml",
		help="SQA docker-compose file (default: %(default)s)")
    parser.add_argument("--qc-criterion", type=str,
		help=f"(optional) Select one QC Criterion to be tested. Must be listed in the SQA Config file (one of {qc_criteria})")


    args = parser.parse_args()
    main()

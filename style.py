#! /usr/bin/python3

import argparse
import configparser
import os
import re
import stat
import subprocess
import sys


LOG_WARNINGS = True

ARG_CONFIG_FILE = 'config_file'
ARG_TEMPLATES_DIR = 'templates_dir'
ARG_REFRESH_SCRIPT = 'refresh_script'

C_       = '\033[0m'
C_RED    = '\033[31m'
C_YELLOW = '\033[33m'

def print_message(level, msg, suffix, out_file=sys.stdout):
    print('{}: {}. {} ...'.format(level, msg, suffix), file=out_file)

def quit(msg, *args):
    print_message('{}ERROR{}'.format(C_RED, C_), msg.format(*args), 'Quitting', sys.stderr)
    exit(1)

def warn(msg, *args):
    LOG_WARNINGS and print_message('{}WARNING{}'.format(C_YELLOW, C_), msg.format(*args), 'Skipping')

def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--' + ARG_CONFIG_FILE, default='./theme_config.ini', help='config INI file used for template substitutions')
    parser.add_argument('-t', '--' + ARG_TEMPLATES_DIR, default='./templates/', help='directory containing templates to configure')
    parser.add_argument('-r', '--' + ARG_REFRESH_SCRIPT, help='refresh script to run after distributing templates to allow for changes to take effect')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppress warnings (will still show errors)')
    args = parser.parse_args()
    global LOG_WARNINGS
    if args.quiet: LOG_WARNINGS = False
    return vars(args)

def load_colors(filename):
    try:
        parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        return parser.read(filename) and parser
    except: return None

def get_template_files(templates_dirname):
    try: return map(lambda f: os.path.join(templates_dirname, f), os.listdir(templates_dirname))
    except: return None

def load_template(template_filename):
    try:
        with open(template_filename, 'r') as f:
            template_lines = f.readlines()
        if not template_lines: return (None, None)

        params = {}
        i = 0
        line = template_lines[i].strip()
        while not all(c == '-' for c in line):
            (param_name, param_data) = re.split('\s*=\s*', line)
            params[param_name] = param_data
            i += 1
            line = template_lines[i].strip()
        template = ''.join(template_lines[i+1:])
        return (template, params)
    except: return (None, None)

def required_params_present(params):
    REQUIRED_TEMPLATE_PARAMS = ['destination', 'executable']
    POSITIVES=['true', 'y', 'yes', '1']
    if not all(param_name in params for param_name in REQUIRED_TEMPLATE_PARAMS): return False

    params['executable'] = any(val == params['executable'].lower() for val in POSITIVES)
    return True

def replace_placeholders_with_data(template, data):
    def replace_on_match(match):
        section = 'DEFAULT'
        if match.group(1): section = match.group(1)[:-1]
        return data[section][match.group(2)]
    try:
        return re.sub(r'{{(\w*?:)?(\w*?)}}', replace_on_match, template)
    except KeyError as e: return None

def make_file_executable(filename):
    try: os.chmod(filename, os.stat(filename).st_mode | stat.S_IEXEC)
    except: return None

def save_configured_resource(resource_str, destination, make_executable=False):
    destination = destination.replace('~', os.path.expanduser('~'))
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'w') as fout:
        fout.write(resource_str)
    make_executable and make_file_executable(destination)

def refresh(refresh_script):
    try:
        refresh_script and subprocess.call(refresh_script)
        return True
    except: return None

def main():
    args = parse_arguments()

    theme_config = load_colors(args[ARG_CONFIG_FILE])
    not theme_config and quit("Invalid config file '{}'", args[ARG_CONFIG_FILE])

    template_files = get_template_files(args[ARG_TEMPLATES_DIR])
    not template_files and quit("Invalid templates dir '{}'", args[ARG_TEMPLATES_DIR])

    for template_filename in template_files:
        (template, params) = load_template(template_filename)
        if template and required_params_present(params):
            themed_res = replace_placeholders_with_data(template, theme_config)
            if themed_res:
                save_configured_resource(themed_res, params['destination'], params['executable'])
            else: warn("Invalid placeholder {} found in template '{}'", e, template_filename)
        else: warn("Invalid or malformed parameters in template '{}'", template_filename)

    if args[ARG_REFRESH_SCRIPT]:
        not refresh(args[ARG_REFRESH_SCRIPT]) and warn("Failed to reload using script '{}'", args[ARG_REFRESH_SCRIPT])
    else:
        warn("No reload script specified. Please reload any necessary changes manually")

if __name__ == '__main__':
    main()

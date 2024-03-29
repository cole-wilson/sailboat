from sailboat import Plugin, get_plugin, PluginNotFound
import enlighten
import os
import glob
import shutil
import re
import requests
import traceback
import blessed
import sys
import time
import colorama

colorama.init()  # For Windows
from semver import VersionInfo
from semver import compare


class Build(Plugin):
    _type = "core"
    description = "build your project for release."

    def run(self, **kwargs):
        manager = enlighten.get_manager()
        term = blessed.Terminal()
        if len(self.options) > 0 and self.options[0] == 'help':
            print(
                "usage: sail build [version (or) increment] [plugins ...]\n\tThis command builds your project using the "
                "sailboat.toml file.\n\tValid options for version:\n\t\t- Valid semver.org string: set that as "
                "version\n\t\t- `major`: increments the major version by one.\n\t\t- `minor`: increments the minor "
                "version by one.\n\t\t- `patch`: increments the patch version by one.\n\t\t- `pre`: increments the "
                "prerelease version by one.\n\t\t- None: increments build version by one.")
            return
        # Get Version =====================================================================================
        if 'latest_build' not in self.data:
            self.data['latest_build'] = '0.0.1'
        if len(self.options) >= 1:  # Something provided
            if VersionInfo.isvalid(self.options[0]):
                version = self.options[0]
            elif self.options[0].startswith('maj'):
                version = str(VersionInfo.parse(self.data['latest_build']).bump_major())
            elif self.options[0].startswith('min'):
                version = str(VersionInfo.parse(self.data['latest_build']).bump_minor())
            elif self.options[0].startswith('pat'):
                version = str(VersionInfo.parse(self.data['latest_build']).bump_patch())
            elif self.options[0].startswith('+') or self.options[0].startswith('build'):
                version = str(VersionInfo.parse(self.data['latest_build']).bump_build())
            else:
                print('Unknown version `{}`'.format(self.options[0]))
                return
            if '.pre' in self.options[0] or '.dev' in self.options[0]:
                version = str(VersionInfo.parse(self.data['latest_build']).bump_prerelease())

        else:
            try:
                latestcommit = os.popen('git rev-parse --short HEAD').read().replace('\n', '')
            except KeyboardInterrupt:
                latestcommit = "build"
            if latestcommit in self.data['latest_build']:
                version = str(VersionInfo.parse(self.data['latest_build']).bump_build())
            else:
                version = str(VersionInfo.parse(self.data['latest_build']).replace(build=latestcommit + ".1"))
        if compare(version, self.data['latest_build']) == -1 and not (
                self.options[0].startswith('pre') or self.options[0].startswith('dev')):
            if input(
                    term.red + f'You are building a version ({version}) that comes before the previously built version ({self.data["latest_build"]}). Do you wish to continue? [y/n]' + term.normal)[
                0] == 'n' or ('-y' in self.options or '--no-interaction' in self.options):
                print()
                return
        status_format = '{program}{fill}{current}{fill}{version}'
        status_bar = manager.status_bar(status_format=status_format, color='white_on_blue', program=self.data['name'],
                                        current='building directory structure', version=version)
        print('\nPreparing to build version {}\n'.format(version))
        self.data['latest_build'] = version
        if len(self.options[1:]) == 0:
            notdones = [*self.data['build'].keys()]
        else:
            notdones = self.options[1:]
        progress_bar = manager.counter(total=len(notdones) + 3, desc='Build', unit='jobs', color="grey")
        prebuild = progress_bar.add_subcounter('white')
        postbuild = progress_bar.add_subcounter('darkgrey')
        # =====================================================================================
        if not os.path.isfile('.gitignore'):
            open('.' + os.sep + '.gitignore', 'w+', encoding="utf8").write(
                self.getResource('resources' + os.sep + 'gitignore.template').read().replace('/', os.sep))
        source_dir = os.getcwd()
        target_dir = self.data["short_name"] + os.sep
        types = ('*.py', *self.data['resources']["data_files"])
        file_names = []
        for files in types:
            file_names.extend(glob.glob(files))
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        for file_name in file_names:
            if file_name in ("setup.py", "sailboat.toml", self.data['resources']['file']):
                continue
            shutil.move(os.path.join(source_dir, file_name), target_dir + os.sep + file_name)
        for filename in glob.glob(target_dir + os.sep + 'LICE*'):
            shutil.copyfile(filename, 'LICENSE')
        if not os.path.isfile(target_dir + '__init__.py'):
            open(target_dir + '__init__.py', 'w+', encoding="utf8").write('# This file must exist, empty or not')
        if self.data['resources']['file'] != "" and not os.path.isfile(
                self.data['short_name'] + os.sep + '__main__.py') and os.path.isfile(self.data['resources']['file']):
            try:
                os.rename(self.data['resources']['file'], self.data['short_name'] + os.sep + '__main__.py')
            except:
                pass
        time.sleep(0.1);
        status_bar.update(current="scanning imports")
        prebuild.update()
        # =====================================================================================
        print('Scanning module imports...')
        if 'no_import' not in self.data['resources']:
            self.data['resources']['no_import'] = []
        mods = []
        for x in glob.glob(self.data['short_name'] + os.sep + '*.py'):
            f = open(x, encoding="utf8")
            b = f.read()
            f.close()
            mods += re.findall('^import[ ]+(.*)', b, re.M)
            mods += re.findall('^from[ ]+(.*) import', b, re.M)
        modules = []
        for x in set(mods):
            modules.append(x.split('.')[0])
        for module in set(modules):
            if module not in self.data['resources']['no_import'] and (
                    module != self.data['short_name'] and module not in sys.builtin_module_names and module not in
                    self.data['resources']['modules']):
                print('Checking for {} on PyPi...'.format(module))
                response = requests.get("https://pypi.python.org/pypi/{}/json".format(module))
                if response.status_code == 200:
                    self.data['resources']['modules'].append(module)
                else:
                    self.data['resources']['no_import'].append(module)
        time.sleep(0.1);
        status_bar.update(current="removing previous builds")
        prebuild.update()
        # =====================================================================================
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            pass
        dones = []
        for build_plugin in progress_bar(notdones):
            if build_plugin not in self.options and (
                    '_run' in self.data['build'][build_plugin] and not self.data['build'][build_plugin]['_run']):
                continue
            if build_plugin in dones:
                continue
            if build_plugin not in self.data['build'].keys():
                continue
            elif '_needs' in self.data['build'][build_plugin]:
                if isinstance(self.data['build'][build_plugin]['_needs'], str):
                    self.data['build'][build_plugin]['_needs'] = [self.data['build'][build_plugin]['_needs']]
                for x in self.data['build'][build_plugin]['_needs']:
                    if x not in dones:
                        notdones.append(build_plugin)
                        build_plugin = x
            print(term.cyan + term.underline + build_plugin + term.normal + term.nounderline + "\n\n")
            time.sleep(0.2);
            status_bar.update(current=build_plugin)
            try:
                plugin_type, job = get_plugin(build_plugin, plugin_type="build")
                job = job(
                    data=self.data,
                    options=[],
                    name=build_plugin,
                    prefix=self.prefix,
                    version=version
                )
            except PluginNotFound:
                sys.exit(f'You seem to have added the {build_plugin} plugin, but it does not appear to be installed!')
            try:
                job.run()
            except KeyboardInterrupt:
                print('\n\nUser has aborted at step {}.\n\n'.format(build_plugin))
                sys.exit(0)
            except BaseException as error:
                print('\n\nError at step {}:\n\n\t{}\n\n'.format(build_plugin, self.red(traceback.print_exc())))
                sys.exit(1)
            self.data[job._type][build_plugin] = job.data[job._type][build_plugin]
            dones.append(build_plugin)
        time.sleep(0.1);
        status_bar.update(current="running develop")
        print(self.section('Finishing up...'))
        os.system('python3 setup.py develop')
        postbuild.update()
        print(self.section('Built files:'))
        for x in glob.glob(f'.{os.sep}dist{os.sep}*{os.sep}*') +\
                 glob.glob(f'.{os.sep}dist{os.sep}*'):
            print(x)
        time.sleep(0.2);
        status_bar.update(current='Finished Build!')
        manager.stop()

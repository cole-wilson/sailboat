# Copyright 2020 Cole Wilson and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above
# copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
import os
import sys
import stat
import glob
import shutil
import requests
import time
from semver import VersionInfo
from sailboat import Plugin, refresh_plugins
import colorama

colorama.init()  # For Windows


class Actions(Plugin):
    description = "Generate a GH Actions workflow file."
    _type = "build"
    _release = True

    def release(self):
        os.system(f"""git init;
git add .;
git config --global credential.helper "cache --timeout=3600";
git config user.name "{self.data["author"]}";
git config user.email "{self.data["email"]}";
git commit -m "{self.data['release-notes']}";
git tag v{self.version};
git remote add origin https://github.com/{self.data['git']['github']}.git||echo origin already added;
git push -u origin master --tags;
""")

    def run(self, **kwargs):
        linux = ""
        mac = ""
        windows = ""
        plugins = refresh_plugins()
        for x in self.data['build']:
            if 'windows' in plugins['build'][x]['default_os']:
                windows = windows + " " + x
            if 'linux' in plugins['build'][x]['default_os']:
                linux = linux + " " + x
            if 'mac' in plugins['build'][x]['default_os']:
                mac = mac + " " + x

        with self.getResource(f'resources{os.sep}sailboat.yml.template') as temp:
            new = temp.read().format(
                linux=linux,
                mac=mac,
                windows=windows,
                l="#" if linux == "" else "",
                m="#" if mac == "" else "",
                w="#" if windows == "" else "",
                **self.data,
                dependencies=" ".join(self.data['resources']['modules'])
            )
            try:
                f = open(f'.github{os.sep}workflows{os.sep}sailboat.yml', 'w+', encoding="utf8")
            except FileNotFoundError:
                os.mkdir('.github')
                os.mkdir(f'.github{os.sep}workflows')
                f = open(f'.github{os.sep}workflows{os.sep}sailboat.yml', 'w+', encoding="utf8")
            f.write(new)
            f.close()

        print('Workflow generated. Remember to push twice in order for new workflow to take effect.')


class PyPi(Plugin):
    _type = "build"
    _release = True

    def release(self):
        print("Please make sure that you have a https://pypi.org/ account.")
        try:
            import twine
        except ModuleNotFoundError:
            input('Press enter to continue installing `twine`. Press ctrl+c to exit.')
            os.system('python3 -m pip install --user --upgrade twine || python3 -m pip install --upgrade twine')
            try:
                import twine
            except ModuleNotFoundError:
                os.system('pip3 install --user --upgrade twine || pip3 install --upgrade twine')
        print('\u001b[4m\u001b[1;36mPyPi Credentials:\u001b[0m')
        os.system('python3 -m twine upload dist' + os.sep + 'pypi' + os.sep + '*')

    def wizard(self):
        print(self.section('Terminal Commands:'))
        if 'commands' in self.data[self._type][self.name]:
            print(self.blue('Commands: ') + str(self.data[self._type][self.name]['commands']))
        elif input(self.blue('Does your project have any terminal commands associated with it? [y/n]: '))[0] == 'y':
            self.storeData('commands', {})
            print(self.red(
                '`runs:` must be follow the rule \u001b[4m`module.function_name`\u001b[0m\033[1;31m, or be blank, '
                'which runs the main project file as a script. \n\nIt is recommended to use function wrappers.\n\nAn '
                'example would be:\n\t- name: test_command\n\t  runs: file.test\nThis would run the test() function in '
                'file.py\n\nPress ctrl+c to stop asking.'))
            while True:
                try:
                    n = input(self.blue('\t- name: '))
                    mod = input(self.blue('\t  runs: '))
                    self.data[self._type][self.name]['commands'][n] = mod
                    print()
                except KeyboardInterrupt:
                    print('\nDone!\n\n')
                    break
        else:
            self.data[self._type][self.name]['commands'] = {}

        print(self.section('Entry points:'))
        if 'entry_points' in self.data[self._type][self.name]:
            print(self.blue('Entry points: ') + str(self.data[self._type][self.name]['entry_points']))
        elif input(self.blue('Does your project have any entry points associated with it? [y/n]: '))[0] == 'y':
            self.storeData('entry_points', {})
            while True:
                try:
                    group = input('\t- Group name: ')
                    if group not in self.data[self._type][self.name]['entry_points']:
                        self.data[self._type][self.name]['entry_points'][group] = {}
                    while True:
                        try:
                            name = input('\t\t- Entrypoint Name: ')
                            locator = input('\t\t  Locator: ')
                            self.data[self._type][self.name]['entry_points'][group][name] = locator
                            print()
                        except KeyboardInterrupt:
                            print('\n')
                            break
                except KeyboardInterrupt:
                    print('\n')
                    break
        else:
            self.storeData('entry_points', {})

    def run(self, **kwargs):
        # ============== Create bin Script ===============================================
        try:
            os.mkdir('bin')
        except FileExistsError:
            pass
        bins = []
        for commandname in self.getData('commands').keys():
            if self.getData('commands')[commandname] == '':
                open("bin" + os.sep + commandname, 'w+').write(
                    f"#!" + os.sep + "usr" + os.sep + "bin" + os.sep + f"env bash\npython3 -m {self.data['short_name']}"
                                                                       f" $@")
                bins.append('bin' + os.sep + commandname)
        # ============== Generate setup.py ===============================================
        print('\n\n\u001b[4m\u001b[1;36mGenerating setup.py\u001b[0m')
        if 'custom_setup' in self.data:
            cu = str(self.data['custom_setup'])
        else:
            cu = str({})
        with self.getResource('resources/setup.py.template') as datafile:
            template = datafile.read()

        entries = {'console_scripts': []}
        for commandname in self.getData('commands').keys():
            if self.getData('commands')[commandname] != "":
                modname = ".".join(self.getData('commands')[commandname].split('.')[:-1])
                funcname = self.getData('commands')[commandname].split('.')[-1]
                entries['console_scripts'].append(
                    commandname + "=" + self.data["short_name"] + "." + modname + ":" + funcname)

        for entry_point_group in self.getData('entry_points').keys():
            if entry_point_group not in entries:
                entries[entry_point_group] = []
            for entry_point_name in self.getData('entry_points')[entry_point_group]:
                entries[entry_point_group].append(
                    entry_point_name + "=" + self.getData('entry_points')[entry_point_group][entry_point_name])

        try:
            pyv = self.version.split('+')[0]
        except IndexError:
            pyv = self.version

        setup = template.format(
            **self.data,
            **self.data['resources'],
            cu=cu,
            bins=bins,
            version=pyv,
            entry_points=entries
        )
        open('setup.py', 'w+').write(setup)

        # ============== Generate pypi files ===============================================
        print('\n\n\u001b[4m\u001b[1;36mGenerating PyPi files...\u001b[0m')
        os.system('python3 .' + os.sep + 'setup.py bdist_wheel sdist -d dist' + os.sep + 'pypi')
        try:
            shutil.rmtree('build')
        except FileNotFoundError:
            pass
        for x in glob.glob('dist' + os.sep + '*.whl'):
            os.rename(x, x.replace('dist' + os.sep, 'dist' + os.sep + 'pypi' + os.sep))
        for x in glob.glob('*.egg-info'):
            shutil.rmtree(x)


class Homebrew(Plugin):
    _type = "build"
    _release = True
    _order = 200

    def release(self):
        self.options = self.options[0]
        if "pypi" in self.options or len(self.options) == 0:
            print('Must wait 20 seconds for pypi files to upload before creating Homebrew formula...\n')
            for i in range(0, 20):
                time.sleep(1)
                sys.stdout.write(u"\u001b[1000D" + str(20 - (i + 1)).zfill(2) + " seconds left.\t")
                sys.stdout.flush()
            print()
        try:
            shutil.rmtree('homebrew-taps')
        except FileNotFoundError:
            pass
        f = open('dist' + os.sep + 'homebrew' + os.sep + self.data['name'] + '.rb')
        old_formula = f.read()
        f.close()
        f = open('dist' + os.sep + 'homebrew' + os.sep + self.data['name'] + '.rb', 'w+')
        req = requests.get('https://pypi.org/pypi/{}/json'.format(self.data['short_name'])).json()
        version_py = req['info']['version']
        url = req['releases'][version_py][0]['url']
        sha256 = req['releases'][version_py][0]['digests']['sha256']
        if not (url.endswith('.tar.gz') or url.endswith('.zip')):
            try:
                url = req['releases'][version_py][1]['url']
                sha256 = req['releases'][version_py][1]['digests']['sha256']
            except KeyError:
                url = "error"
                sha256 = "error"
        f.write(old_formula.format(pyhosted=url, sha256=sha256, version=version_py))
        f.close()
        if 'github' in self.data['git']:
            username = self.data['git']['github'].split('/')[0]
        else:
            username = input('Your GitHub username: ')
        print('\u001b[4m\u001b[1;36mHomebrew Release:\u001b[0m')
        if 'brew' not in self.data['git'] and len(
                os.popen(f'git ls-remote https://github.com/{username}/homebrew-taps').read()) < 4:
            print('Creating new repo')
            print(
                'To create a homebrew formula, you must first setup a GitHub repository called '
                '"homebrew-taps".\n\nPlease go to https://github.com/new and create a repo called `homebrew-taps`.')
            input('Press enter when done.')
            os.mkdir('homebrew-taps')
            os.chdir('homebrew-taps')
            os.system(
                f'git init;echo "# homebrew-taps" >> README.md;git remote add origin https://github.com/{username}/'
                f'homebrew-taps.git')
            os.chdir('..')
        else:
            print('Cloning existing repo')
            os.system(f'git clone https://github.com/{username}/homebrew-taps.git')
        shutil.copy('dist' + os.sep + 'homebrew' + os.sep + self.data['name'] + '.rb',
                    'homebrew-taps' + os.sep + self.data['name'] + '.rb')
        # input()
        os.system(
            f'cd homebrew-taps;'
            f'git add .;'
            f'git config --global credential.helper "cache --timeout=3600";'
            f'git config user.name "{self.data["author"]}";'
            f'git config user.email "{self.data["email"]}";'
            f'git commit -m "{self.data["release-notes"]}";'
            f'git commit --amend -m "{self.data["release-notes"]}";'
            f'echo git tag v{self.version};'
            f'git push origin master --tags;'
            f'cd ..'
        )
        self.data['git']['brew'] = username + "/homebrew-taps"
        try:
            shutil.rmtree('homebrew-taps')
        except FileNotFoundError:
            pass

    def run(self, **kwargs):
        retmp = '   resource "{name}" do\n      url "{url}"\n      sha256 "{sha256}"\n   end\n'
        resources = ''
        for module_name in self.data['resources']['modules']:
            req = requests.get('https://pypi.org/pypi/{}/json'.format(module_name)).json()
            versionPy = req['info']['version']
            url = req['releases'][versionPy][0]['url']
            sha256 = req['releases'][versionPy][0]['digests']['sha256']
            if not (url.endswith('.tar.gz') or url.endswith('.zip')):
                try:
                    url = req['releases'][versionPy][1]['url']
                    sha256 = req['releases'][versionPy][1]['digests']['sha256']
                except:
                    continue
            resources += retmp.format(name=module_name, url=url, sha256=sha256)
        os.makedirs('dist' + os.sep + 'homebrew')
        f = open('dist' + os.sep + 'homebrew' + os.sep + '{name}.rb'.format(name=self.data['name']), 'w+')
        f.write(self.getResource('resources' + os.sep + "brew.rb").read().format(
            **self.data,
            resources2=resources,
            version=self.version
        ))
        f.close()


class PyInstaller(Plugin):
    _type = "build"
    setup = {
        "type::int": "Select one of the following:\n\t1. My app needs a console window to display input and "
                     "output.\n\t2. My app should provide it's own windows.\n>>> ",
        "mac::bool": "Would you like to generate a Mac app for your project? ",
        "windows::bool": "Would you like to generate a Windows app for your project? ",
        "unix::bool": "Would you like to generate a Unix executable for your project? ",
    }
    _os = "windows mac linux"

    def wizard(self):
        super().wizard()
        if 'bundle_id' not in self.getData():
            self.storeData('bundle_id',
                           "com." + self.data['author'].lower().replace(' ', '') + "." + self.data['short_name'])

    def run(self, **kwargs):
        version = VersionInfo.parse(self.version)
        self.version = str(
            VersionInfo(major=version.major, minor=version.minor, patch=version.patch, prerelease=version.prerelease))
        if not (self.getData('mac') or self.getData('windows') or self.getData('unix')):
            return
        try:
            import PyInstaller.__main__
        except:
            print('Installing PyInstaller...')
            os.system('pip3 install pyinstaller')
            import PyInstaller.__main__

        mods = []
        for x in self.data['resources']['modules']:
            mods.append('--hidden-import')
            mods.append(x)

        datafiles = []
        for x in self.data['resources']['data_files']:
            for g in glob.glob(self.data['short_name'] + os.sep + x):
                datafiles.append('--add-data')
                datafiles.append(g + os.pathsep + "." + os.sep + os.sep.join(
                    g.replace(self.data['short_name'] + os.sep, '').split(os.sep)[:-1]))
        typ = '--nowindowed' if self.getData('type') == 1 else '--noconsole'
        if sys.platform.startswith('dar') and 'icns' in self.data['resources']:
            ico = ["--icon", self.data['resources']['icns']]
        if sys.platform.startswith('win') and 'ico' in self.data['resources']:
            ico = ["--icon", self.data['resources']['ico']]

        else:
            ico = []

        osname = "macos" if sys.platform.startswith('darwin') else sys.platform
        options = [
            self.data['short_name'] + os.sep + '__main__.py',
            '--onefile',
            '--name',
            self.data['short_name'] + '-' + self.version + '-' + osname,
            '--distpath',
            '.' + os.sep + 'dist' + os.sep + 'pyinstaller',
            *(self.getData('options') if 'options' in self.data2 else []),
            *mods,
            *datafiles,
            typ,
            *ico,
            '--osx-bundle-identifier',
            self.getData('bundle_id')
        ]
        print(options)
        PyInstaller.__main__.run(options)
        print('removing *.spec files')
        for specfile in glob.glob('*.spec'):
            os.remove(specfile)
        # MAC APP BUNDLE==============
        for appbundle in glob.glob('dist/pyinstaller/*.app'):
            print(appbundle)
            shutil.rmtree(appbundle)  # We don't want the .app file PyInstaller made!
        print('\n\n\u001b[4m\u001b[1;36mGenerating Mac .app bundle...\u001b[0m')
        if self.getData('mac') and sys.platform.startswith('dar'):
            os.chdir('dist')

            os.mkdir(self.data['name'])
            os.chdir(self.data['name'])

            os.mkdir('Contents')
            os.chdir('Contents')

            os.mkdir('MacOS')
            os.mkdir('Resources')

            infoPlist = open('Info.plist', 'w+')
            infoPlist.write(self.getResource('resources' + os.sep + 'info.plist.xml').read().format(
                **self.data,
                execname=self.data['name'].replace('_', ''),
                **self.data['build'],
                version=self.version,
                bundle_id=self.getData('bundle_id')
            ))
            infoPlist.close()

            os.rename('./../../pyinstaller/' + self.data["short_name"] + "-" + self.version + "-macos",
                      'MacOS/' + self.data['name'].replace('_', ''))
            if self.getData('type') == 1:
                os.rename('MacOS/' + self.data['name'].replace('_', ''), 'MacOS/main')
                with open('MacOS/' + self.data['name'].replace('_', ''), 'w+') as f:
                    f.write(f'#!/bin/bash\n'
                            'DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"\n'
                            'open -a Terminal ${DIR}/main')
                # with open('MacOS/runner', 'w+') as f:
                #     f.write(f'#!/bin/bash\n'
                #             'DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"\n'
                #             '${DIR}/main')
                st = os.stat('MacOS/' + self.data['name'].replace('_', ''))
                os.chmod('MacOS/' + self.data['name'].replace('_', ''), st.st_mode | stat.S_IEXEC)
            if "icns" in self.data['resources'] and os.path.isfile("./../../../"+self.data['resources']["icns"]):
                shutil.copy('./../../../' + self.data['resources']["icns"], 'Resources/icon.icns')

            os.chdir('./../../..')
            os.rename('./dist/' + self.data['name'], './dist/pyinstaller/' + self.data['name'] + ".app")
        else:
            print('not generating mac .app bundle because on {} not mac.'.format(sys.platform))
        # ============== Generate Installer Package ===============================================
        print('\n\n\u001b[4m\u001b[1;36mGenerating Installer Package...\u001b[0m')
        if not (self.getData('windows') or self.getData('unix') or self.getData('mac')):
            pass
        elif sys.platform.startswith('darwin'):  # MAC
            try:
                import dmgbuild
            except ModuleNotFoundError:
                print('Installing dmgbuild')
                os.system('pip3 install dmgbuild')
                import dmgbuild
            del dmgbuild
            if not os.path.isdir('build'):
                os.mkdir('build')
            open('build' + os.sep + 'settings.py', 'w+').write(
                self.getResource('resources' + os.sep + 'settings.py.template').read().format(
                    **self.data,
                    version=self.version,
                    icns="" if not "icns" in self.data['resources'] else self.data['resources']['icns'],
                    keywo=", ".join(self.data['keywords']),
                    ddimage=self.prefix + 'resources' + os.sep + 'dragdrop.png'
                ))
            os.system(
                f'dmgbuild -s .{os.sep}build{os.sep}settings.py "{self.data["name"]} Installer" ./dist/pyinstaller/{self.data["short_name"] + "-" + self.version + "-macos"}.dmg')

        else:
            print(f'Installer creation not yet supported for {sys.platform}!')

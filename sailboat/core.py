from sailboat import Plugin, refresh_plugins, get_plugin, PluginNotFound
import os
import glob
import sys
import traceback
import colorama
from semver import VersionInfo

colorama.init()  # For Windows


class QuickStart(Plugin):
    _type = "core"
    description = "Get your project up and running."

    def runPlugin(self, plug, plugins, opts=[]):
        plugin_type, b = get_plugin(plug)
        temp = b(
            data=self.data,
            options=opts,
            name=plug,
            prefix=self.prefix,
            version=None
        )
        temp.run(plugins=plugins)
        return temp.data

    def run(self, plugins={}, **kwargs):
        input(
            'This quickstart command will get you started on your project.\nFirst, it will set up the config file and your GitHub settings. Then it will add suggested plugins for your project!\n\nPress enter to continue, and ctrl+c to skip a step.')
        for plug in ['wizard', 'git']:
            print("\n\n" + self.red(plug) + "\n" + (len(plug) * "-") + "\n")
            self.data = self.runPlugin(plug, plugins)
        print()
        print("\n\n" + self.red('plugins') + "\n" + (len('plugins') * "-") + "\n")
        pypi = "pypi" if (input('Would you like to generate pypi files for your project? [Y/n]') + "y")[
                             0] == 'y' else ""
        pyinstaller = "pyinstaller" if \
        (input('Would you like to generate pyinstaller files for your project? [Y/n]') + "y")[0] == 'y' else ""
        homebrew = "homebrew" if (input('Would you like to generate homebrew files for your project? [Y/n]') + "y")[
                                     0] == 'y' else ""
        combined = f"{pypi} {pyinstaller} {homebrew}"
        if len(combined) > 0:
            print()
            self.runPlugin('add', plugins, opts=[*combined.split()])

        print('Your project is set up, run `sail build` to build, or `sail add <plugin>` to add a new plugin.')


class ManagePlugins(Plugin):
    _type = "core"
    description = "plugin manager."

    def autocomplete(self):
        return ['a', 'b']

    def run(self, plugins={}, **kwargs):
        if self.options == []:
            print("usage: sail plugins [refresh]\n\n\trefresh: reload previously installed plugins.")
        elif self.options == ['refresh'] or self.options == ['-r']:
            refresh_plugins();
            print('Done!')
        elif self.options == ['list']:
            print('Build:')
            for x in self.data['build']:
                print('\t- ' + x)
            print('Release:')
            for x in self.data['release']:
                print('\t- ' + x)
            print('Command:')
            for x in self.data['command']:
                print('\t- ' + x)

        else:
            print('sailboat: error: invalid option `{}`.'.format(self.options[0]))


class Develop(Plugin):
    _type = "core"
    description = "run your project without building it."

    def run(self, plugins={}, **kwargs):
        if os.path.isfile('setup.py'):
            os.system('python setup.py develop')
        else:
            self.info("Can't find setup.py. Create one using sail build.")


class Wizard(Plugin):
    _type = "core"
    description = "configure your project or a plugin."
    setup = {  # Top Level Setup
        "name::str": "Full name of your project: ",
        "short_name::str": "Short name of your project: ",
        "email::str": "Email for your project: ",
        "author::str": "Your name(s): ",
        "short_description::str": "Short description of your project: ",
        "description::str": "Long description of your project: ",
        "url::str": "Home URL of your project",
        "keywords::str": "Your project's keywords, seperated with a space.",
    }

    def wizard(self):
        super().wizard()
        lt = "BSD-2-Clause/BSD-3-Clause/Apache-2.0/LGPL-2.0/LGPL-2.1/LGPL-3.0/GPL-2.0/GPL-3.0/CCDL-1.0/GNU LGPL/MIT/Other SPDX License ID"
        licen = len(glob.glob('.' + os.sep + 'LICENS*')) > 0
        if licen:
            if 'license' not in self.data:
                print(self.term.cyan + 'You seem to have a license file in your project, but what type is it?')
                for license in lt.split(os.sep + ''):
                    print(f'\t- {license}')
                self.data['license'] = input(">>>" + self.term.normal + " ")
            else:
                print(self.blue('License') + ' {}'.format(self.data['license']))
        else:
            self.data['license'] = "none"
        print(self.section('Resource Settings:'))
        if 'resources' not in self.data:
            self.data['resources'] = {}
        questions = {
            "icns": "Mac .icns icon for your project, leave blank if none",
            "data_files": "List of all data files for your project seperated with spaces. * counts as wildcard",
            "modules": "Space seperated list of modules required for your project",
            "file": "Main python file of your project. Leave blank if none"
        }
        for key in questions:
            if key in self.data['resources']:
                print(self.blue(questions[key]) + ': ' + str(self.data['resources'][key]))
            else:
                if key in ('modules', 'data_files'):
                    self.data['resources'][key] = input(self.blue(questions[key]) + ": ").split()
                else:
                    self.data['resources'][key] = input(self.blue(questions[key]) + ": ")
        self.data['name'] = self.data['name'].replace(' ', '_')
        self.data['short_name'] = self.data['short_name'].replace(' ', '_')

        print(self.red(
            'Be sure to prefix any paths to any resources with ' + self.term.underline + '4m`os.path.dirname(os.path.abspath(__file__))+os.sep`' + self.term.nounderline + self.term.red + ' to make sure that they use the correct path and not the current directory.'))

    def run(self, plugins={}):
        if self.options == []:
            self.wizard()
            for tt in ['command', 'build', 'release']:
                for x in self.data[tt]:
                    print(self.section(x.title() + ":"))
                    plugin_type, b = get_plugin(x)
                    b = b(
                        data=self.data,
                        options=[],
                        name=x,
                        prefix=self.prefix,
                        version=None
                    )
                    try:
                        b.wizard()
                    except KeyboardInterrupt:
                        print('Abborted by user')
                    except BaseException:
                        print(traceback.print_exception(*sys.exc_info()))
                        print(
                            'Error in `{}` wizard script:\n\t{}'.format(x, traceback.print_exception(*sys.exc_info())))
                    self.data[tt][x] = b.data[tt][x]

        else:
            for x in self.options:
                try:
                    plugin_type, temp = get_plugin(x)
                except PluginNotFound:
                    print("Couldn't find the {} plugin.".format(x))
                    continue
                temp = temp(
                    data=self.data,
                    options=[],
                    name=x,
                    prefix=self.prefix,
                    version=None
                )
                try:
                    temp.wizard()
                except KeyboardInterrupt:
                    print('Abborted by user')
                except BaseException as e:
                    print('Error in `{}` wizard script:\n\t{}'.format(x, e))
                self.data[plugin_type][x] = temp.data[plugin_type][x]


class Git(Plugin):
    _type = "core"
    description = "Manage Git for your project."

    def run(self, plugins={}, **kwargs):
        if self.options == ['push']:
            a = input("Message: ").replace('"', r'"')
            os.system(f'git add .;git commit -a -m "{a}";git push;')
            return
        if 'github' not in self.data['git']:
            uname = input('GitHub username: ')
            if input('Do you have a GitHub repository for this project yet?')[0] == 'y':
                self.data['git']['github'] = uname + '/' + input('GitHub repo name: ')
            else:
                print('Go to https://github.com/new and create a repo.')
                self.data['git']['github'] = uname + '/' + input('GitHub repo name: ')
            os.system(f"""git init;
git add .;
git config --global credential.helper "cache --timeout=3600";
git config user.name "{self.data["author"]}";
git config user.email "{self.data["email"]}";
git commit -m "Initial Commit :rocket:";
git remote add origin https://github.com/{self.data['git']['github']}.git;
git push -u origin master;
""")
        print(
            'Your GitHub repo is setup. To update your repo, type:\n\n\tgit add .;git commit -a -m "Your message here";git push;\n\nin your terminal, or `sail git push`')


class Release(Plugin):
    _type = "core"
    description = "Release your project."

    def run(self, **kwargs):
        plugins = refresh_plugins()
        self.data['release-notes'] = input('Release Title: ')
        # print('Release description: (^c to exit)')
        # try:
        # 	while True:
        # 		"\n" + self.data['release-notes'] += input('> ')
        # except KeyboardInterrupt:
        # 		print('\n')
        version = VersionInfo.parse(self.data['latest_build'])
        version = str(
            VersionInfo(major=version.major, minor=version.minor, patch=version.patch, prerelease=version.prerelease))
        runs = {}
        if self.options == []:
            for x in self.data['release']:
                if x in plugins['release']:
                    runs[x] = plugins['release'][x]['order']
            for x in self.data['build']:
                if x in plugins['build']:
                    if plugins['build'][x]['release']:
                        runs[x] = plugins['build'][x]['order']
            for x in self.data:
                if x in plugins['core']:
                    if plugins['core'][x]['release']:
                        runs[x] = plugins['core'][x]['order']

        else:
            for x in self.options:
                if x in self.data['release'] and x in plugins['release']:
                    runs[x] = plugins['release'][x]['order']
                elif x in self.data['build']:
                    if plugins['build'][x]['release']:
                        runs[x] = plugins['build'][x]['order']
                elif x in self.data:
                    if plugins['core'][x]['release']:
                        runs[x] = plugins['core'][x]['order']

                else:
                    print('sailboat: error: {} is not a valid release plugin.'.format(x))
                    return
        runstemp = []
        for x in runs:
            runstemp.append(f"{runs[x]}::{x}")
        runstemp.sort()
        runs = []
        for x in runstemp:
            order, name = x.split('::')
            runs.append(name)
        input(f'Press enter to release version {version} the following ways:\n\t- ' + '\n\t- '.join(runs) + '\n\n>>>')
        dones = []
        for release_plugin in runs:
            if release_plugin in dones:
                continue
            print(self.section(release_plugin + ":"))
            plugin_type, temp = get_plugin(release_plugin)
            temp = temp(
                data=self.data,
                options=[self.options],
                name=release_plugin,
                prefix=self.prefix,
                version=version
            )
            temp.release()
            if temp._type == 'core':
                self.dat = temp.data
            else:
                self.data[temp._type][release_plugin] = temp.data[temp._type][release_plugin]
            dones.append(release_plugin)
        print()
        self.data['latest_release'] = version


class Remove(Plugin):
    _type = "core"
    description = "remove a plugin from you project."

    def run(self, **kwargs):
        if len(self.options) < 1:
            print('usage: sail remove [plugin ...]\n\n\tRemoves plugins from project.')
            return
        for option in self.options:
            t, _ = get_plugin(option)
            try:
                del self.data[t][option]
                print('removed {}'.format(option))
            except KeyError:
                print('couldn`t find {}, therfore not removed.'.format(option))


class Add(Plugin):
    _type = "core"
    description = "add a plugin to your project."

    def run(self, **kwargs):
        # get all availbile plugin
        done = []
        if len(self.options) == 0:
            print('''usage: sail add [plugins ...]

	Install PLUGINS to current project.
	''')
        from pkg_resources import iter_entry_points
        for point in iter_entry_points('sailboat_plugins'):
            if (point.name in self.data['build'] or point.name in self.data['command'] or point.name in self.data[
                'release']) and point.name in self.options:
                print('{} already added'.format(point.name))
                continue
            if point.name in self.options:
                done.append(point.name)
                temp = point.load()
                run = temp(data=self.data, options=[], name=point.name, prefix=self.prefix)
                print(self.section(f'{point.name} [{run._type}]:{run.description}.'))
                if point.name not in self.data[run._type]:
                    self.data[run._type][point.name] = {}
                if run._type == 'core':
                    print(
                        'BE WARNED: THIS PLUGIN TYPE IS REGISTERED AS "core", which means it has unfiltered access to your project`s data. Please be 100% sure you want to do this.')
                run.data = self.data
                try:
                    run.wizard()
                    run.add()
                except KeyboardInterrupt:
                    print('Aborted by user')
                except BaseException as e:
                    print('Error in `{}` wizard script:\n\t{}'.format(point.name, e))
                data = run.data
                self.data[run._type][point.name] = data[run._type][point.name]
                print('added {}'.format(point.name))
        for x in self.options:
            if x not in done and (
                    x not in self.data['build'] and x not in self.data['command'] and x not in self.data['release']):
                print('error: could not find {}, please make sure you have downloaded it.'.format(x))
        refresh_plugins()
        return self.data

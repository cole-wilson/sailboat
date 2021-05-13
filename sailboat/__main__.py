import sys
import os
import toml
import json
import colorama
import blessed
import sailboat

colorama.init()  # For Windows
prefix = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))) + os.sep
term = blessed.Terminal()


def main(argv=()) -> None:
    """Program entry point for all of the sail/sailboat terminal program."""
    # Move to project root, check for sailboat.toml, and then read it.
    if argv is None:
        argv = []
    if not argv:
        argv = sys.argv
    ordinal_path = os.getcwd()
    while not os.path.isfile('sailboat.toml') and os.getcwd().count(os.sep) > 2:
        os.chdir('..')
    if not os.path.isfile('sailboat.toml'):
        needs_setup = True
        data = {}
        os.chdir(ordinal_path)
    else:
        needs_setup = False
        with open('sailboat.toml', 'r', encoding="utf8") as file:
            data = toml.loads(file.read())
            if data == {}:
                needs_setup = True

    # Add required sections to data.
    for required_section in ("command", "build", "release", "git"):
        if required_section not in data:
            data[required_section] = {}

    # Search for options in argv
    switches = []
    for index, value in enumerate(argv[1:]):
        if value.startswith('--'):
            switches.append(value[2:])
        elif value.startswith('-'):
            switches.extend(value[1:])
        else:
            start_index = index
            options = [argv[0], *argv[1:][start_index:]]
            break
    else:
        options = [argv[0]]

    plugins = json.loads(open(prefix + 'plugins.json').read())

    if 'version' in switches or 'v' in switches:
        print('Sailboat version {}\n\nHelp:\ncontact cole@colewilson.xyz\nor make an issue at cole-wilson/sailboat'
              .format(sailboat.__version__))
        sys.exit(0)
    if 'refresh' in switches or 'r' in switches or plugins == {} or (len(plugins.keys()) != 4):
        print("Refreshing plugins list (this could take a couple seconds...)")
        plugins = sailboat.refresh_plugins()
        print('Done!\n')
    helptext = "usage: " + sys.argv[0].split(os.sep)[
        -1] + " [options ...] [subcommand] [subcommand options ...]\n\n\tcore commands:"
    for command in plugins['core'].keys():
        if plugins['core'][command]['show']:
            helptext += "\n\t\t- " + term.cyan + command + term.normal + ": " + plugins['core'][command][
                'description'].capitalize()
    helptext += "\n\t\t- " + term.cyan + "help" + term.normal + ": Display this message."
    if len(plugins['command'].keys()) != 0:
        helptext += "\n\n\tother commands:"
    for command in plugins['command'].keys():
        if plugins['command'][command]['show'] and command in data['command']:
            helptext += "\n\t\t- " + term.cyan + command + term.normal + ": " + plugins['command'][command][
                'description'].capitalize()

    helptext += "\n"

    if len(options) < 2:
        print(helptext)
        return
    if needs_setup:
        command = 'quickstart'
    else:
        command = options[1]
    if command == 'help':# or 'help' in options or 'h' in options:
        print(helptext)
        return

    try:
        plugin_type, temp = sailboat.get_plugin(command)
    except sailboat.PluginNotFound:
        print('sailboat: error: {} is not a valid command. Please make sure you have installed it.'.format(command))
        return
    if plugin_type != 'core' and command not in data['build'] and command not in data['release'] and command not in \
            data['command']:
        print(
            'sailboat: error: {} *is* a valid command, but it isn\'t installed on this project. Install it with the '
            '`add` command.'.format(
                command))
        return
    temp = temp(
        data=data,
        options=options[2:],
        name=command,
        prefix=prefix
    )
    ##############################
    temp.run()  # Run the plugin!
    ##############################
    if plugin_type == 'core':
        data = temp.data
    else:
        data[plugin_type][command] = temp.data[plugin_type][command]

    basic_data = {}
    resources = {'resources': {}}
    commands = {'command': {}}
    builds = {'build': {}}
    release = {'release': {}}
    other = {}

    with open('sailboat.toml', 'w+') as f:
        for key in data.keys():
            if not isinstance(data[key], dict):
                basic_data[key] = data[key]
            elif key == 'resources' and len(data[key].values()) > 0:
                resources['resources'] = data[key]
            elif key == 'command' and len(data[key].values()) > 0:
                commands['command'] = data[key]
            elif key == 'build' and len(data[key].values()) > 0:
                builds['build'] = data[key]
            elif key == 'release' and len(data[key].values()) > 0:
                release['release'] = data[key]
            elif key not in ('build', 'release', 'command', 'resources'):
                other[key] = data[key]
        resources = resources if resources != {'resources': {}} else {}
        commands = commands if commands != {'command': {}} else {}
        builds = builds if builds != {'build': {}} else {}
        release = release if release != {'release': {}} else {}
        other = other if other != {'other': {}} else {}
        o = [*map(toml.dumps, [basic_data, resources, commands, builds, release, other])]
        out = r"""#            _  _  _                _   
#  ___ __ _ (_)| || |__  ___  __ _ | |_ 
# (_-</ _` || || || '_ \/ _ \/ _` ||  _|
# /__/\__,_||_||_||_.__/\___/\__,_| \__|
                                      
# Basic Setup:
{}

# Resource Setup:
{}

# Plugin Commands:
{}

# Build Routines:
{}

# Release Routines:
{}

# Other:
{}

# Thank you for using Sailboat!"""
        if '_comments' in data and not data['_comments']:
            print()
            out = "{}\n{}\n{}\n{}\n{}\n{}\n"
        out = out.format(o[0], o[1], o[2], o[3], o[4], o[5])
        f.write(out)


if __name__ == "__main__":
    main(argv=sys.argv)

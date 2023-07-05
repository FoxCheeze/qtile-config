import os
import subprocess

from libqtile import backend, bar, hook, extension, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

colors: dict[str, str] = {
    'bg': '#1e1e2e',
    'bgalt': '#313244',
    'bgdim': '#11111b',
    'ex01': '#f38ba8',
    'ex02': '#ff7a37',
    'ex03': '#b4befe',
    'ex04': '#73b9ff',
    'ex05': '#94e2d5',
    'ft': '#f5c2e7',
    'ftalt': '#cba6f7',
    'ftdim': '#a6adc8',
    'hl': '#f5c2e7',
    'hlalt': '#94e2d5',
    'hldim': '#b4befe',
}
mod = 'mod4'
terminal = 'alacritty'
scr_temp = '3600K'

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    Key([mod], 'h', lazy.layout.left(), desc='Move focus to left'),
    Key([mod], 'l', lazy.layout.right(), desc='Move focus to right'),
    Key([mod], 'j', lazy.layout.down(), desc='Move focus down'),
    Key([mod], 'k', lazy.layout.up(), desc='Move focus up'),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, 'shift'],
        'h',
        lazy.layout.shuffle_left(),
        desc='Move window to the left',
    ),
    Key(
        [mod, 'shift'],
        'l',
        lazy.layout.shuffle_right(),
        desc='Move window to the right',
    ),
    Key(
        [mod, 'shift'],
        'j',
        lazy.layout.shuffle_down(),
        desc='Move window down',
    ),
    Key([mod, 'shift'], 'k', lazy.layout.shuffle_up(), desc='Move window up'),
    Key(
        [mod, 'control'],
        'h',
        lazy.layout.grow_left(),
        desc='Grow window to the left',
    ),
    Key(
        [mod, 'control'],
        'l',
        lazy.layout.grow_right(),
        desc='Grow window to the right',
    ),
    Key(
        [mod, 'control'], 'j', lazy.layout.grow_down(), desc='Grow window down'
    ),
    Key([mod, 'control'], 'k', lazy.layout.grow_up(), desc='Grow window up'),
    Key(
        [mod, 'control'],
        't',
        lazy.window.toggle_floating(),
        desc='Toggle window from or to float',
    ),
    Key([mod], 'n', lazy.layout.normalize(), desc='Reset all window sizes'),
    Key(
        [mod, 'shift'],
        'Return',
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack',
    ),
    Key([mod], 'Return', lazy.spawn(terminal), desc='Launch terminal'),
    Key([mod], 'Tab', lazy.next_layout(), desc='Toggle between layouts'),
    Key([mod], 'w', lazy.window.kill(), desc='Kill focused window'),
    Key([mod, 'control'], 'r', lazy.reload_config(), desc='Reload the config'),
    Key([mod, 'control'], 'q', lazy.shutdown(), desc='Shutdown Qtile'),
    Key(
        [mod],
        'r',
        lazy.spawncmd(),
        desc='Spawn a command using a prompt widget',
    ),
    Key(
        [mod],
        'o',
        lazy.run_extension(
            extension.DmenuRun(
                background=colors['bg'],
                dmenu_bottom=True,
                dmenu_ignorecase=True,
                dmenu_lines=1,
                dmenu_prompt='♥',
                foreground=colors['ft'],
                fontsize=10,
                selected_background=colors['bg'],
                selected_foreground=colors['ft'],
            )
        ),
    ),
    Key([], 'XF86Tools', lazy.spawn('emacs ~/.config/qtile/config.py')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl -- set-sink-mute 3 toggle')),
    Key(
        [],
        'XF86AudioRaiseVolume',
        lazy.spawn('pactl -- set-sink-volume 3 +5%'),
    ),
    Key(
        [],
        'XF86AudioLowerVolume',
        lazy.spawn('pactl -- set-sink-volume 3 -5%'),
    ),
    Key(
        [],
        'XF86Search',
        lazy.spawn(f'redshift -Po -l 0:0 -t {scr_temp}:{scr_temp}'),
    ),
    Key(['control'], 'XF86Search', lazy.spawn('redshift -Po -l 0:0 -x')),
    Key([mod], 'c', lazy.hide_show_bar()),
    Key([mod], 'f', lazy.spawn('dolphin')),
]

groups = [Group(i) for i in '123456789']

for group in groups:
    keys.extend(
        [
            Key(
                [mod],
                group.name,
                lazy.group[group.name].toscreen(),
                desc='Switch to group {}'.format(group.name),
            ),
            Key(
                [mod, 'shift'],
                group.name,
                lazy.window.togroup(group.name),
                desc='Switch to & move focused window to group {}'.format(
                    group.name
                ),
            ),
        ]
    )

layouts = [
    layout.Max(),
    layout.Columns(
        border_focus=colors['hl'],
        border_focus_stack=[colors['hl'], colors['hldim']],
        border_normal=colors['bgdim'],
        border_on_single=True,
        border_width=4,
        margin=[5, 10, 5, 10],
    ),
]

widget_defaults = dict(
    background=colors['bg'],
    font='sans',
    fontsize=13,
    foreground=colors['ft'],
    padding=0,
)
extension_defaults = widget_defaults.copy()

heart_text = widget.TextBox(
    '♥',
    background=None,
    fontsize=14,
    padding=5,
)
separator_text = widget.TextBox(
    '⌇',
    foreground=colors['hlalt'],
    fontsize=32,
    padding=5,
    margin=[5, 5, 5, 5],
)

screens = [
    Screen(
        bottom=bar.Bar(
            [
                heart_text,
                widget.GroupBox(
                    highlight_method='text',
                    active=colors['ft'],
                    inactive=colors['bg'],
                    this_current_screen_border=colors['ex04']
                ),
                separator_text,
                widget.Prompt(),
                widget.Chord(
                    chords_colors={},
                    name_transform=lambda name: name.upper(),
                ),
                widget.TaskList(
                    background=None,
                    border=None,
                    borderwidth=0,
                    padding_y=4,
                    parse_text=lambda s: '',
                    theme_mode='preferred',
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.WidgetBox(
                    widgets=[widget.Systray(background=None)],
                    background=colors['bg'],
                    foreground=colors['ft'],
                    close_button_location='right',
                    text_open='  ●',
                    text_closed='●  ',
                ),
                separator_text,
                widget.Clock(
                    background=colors['bg'],
                    foreground=colors['ft'],
                    format='%Y年 %m月 %d日 | %H:%M - %a',
                ),
                separator_text,
                widget.PulseVolume(update_interval=0.02),
                heart_text,
            ],
            20,
            background=colors['bg'],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        'Button1',
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        'Button3',
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([mod], 'Button2', lazy.window.bring_to_front()),
]


def check_godot():
    p = subprocess.Popen(r'ps -e | grep -i godot', shell=True)
    p.communicate()
    code = p.returncode

    if code != 0:
        return Match(title='non_existent_window_blabla')

    return Match(wm_class='Godot_Editor')


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        check_godot(),
    ]
)


@hook.subscribe.startup_once
def auto_start():
    # Run auto script
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([script])

    # Night mode (blue light filter)
    subprocess.Popen(
        f'redshift -Po -l 0:0 -t {scr_temp}:{scr_temp}', shell=True
    )

    # Wallpapper
    subprocess.Popen(
        f'/run/media/iago-carvalho/Storage/Personal/iago-damasceno/images/wallpaperppoi/kimi-no-na-wa/3.jpg',
        shell=True,
    )

    # Open apps at start
    startup_apps = ['cadence', 'fcitx5', 'firefox', 'qbittorrent']

    for app in startup_apps:
        subprocess.Popen([app])


auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'

"""
Name: help_text
Desc: the help text for kaartmaker
"""
import click
from kaartmaker.constants import VERSION
from os import environ
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


RECORD = environ.get("KAARTMAKER_SCREENSHOT", False)


def pretty_choices(default_list: list):
    """
    Takes a list of default choices and surrounds them with a meta markup tag
    and join them with a comma for a pretty return "Choices" string.
    Example: pretty_choices(['beep', 'boop']) returns:
             'Choices: [meta]beep[/meta], [meta]boop[/meta]'
    """
    defaults = '[/meta], [meta]'.join(default_list)
    return 'Choices: [meta]' + defaults + '[/meta]'


def options_help():
    """
    Help text for all the options/switches for main()
    Returns a dict.
    """
    region_choices = pretty_choices([
        "world", "europe", "africa", "asia", "oceania", "western asia",
        "central asia", "eastern asia", "caribbean", "north america",
        "south america", "central america"
        ])
    help_dict = {
        'region':
        f'Region for map generation. {region_choices}',

        'csv':
        'pass in a csv file with columns: NAME_EN and VOTE. vote must be YES|NO'
        ' or AGAINST|IN FAVOR',

        'save_geojson':
        'save a geojson for the given region',

        'save_png':
        'save a png for the given region',

        'version':
        f'Print the version of kaartmaker (v{VERSION})',

        'title':
        'Title to print above legend in generated map',

        'source':
        'Source link to include in subtitle.',

        'reverse_colors':
        'Reverse colors to use blue for NO|AGAINST and orange for YES|IN FAVOR',

        'use_sub_units':
        'Use sub units instead of sovereignty. Useful to distinguish '
        'countries of the UK. e.g. Scotland, Wales, Northern Ireland, british virgin islands,'
        ' instead of just the UK',

        'legend_countries':
        "Commas separated list of countries to use for the map legend. "
        '(Otherwise, we pick them for you by vote type.)'
        }

    return help_dict


class RichCommand(click.Command):
    """
    Override Clicks help with a Rich-er version.

    This is from the Textualize/rich-cli project, link here:
        https://github.com/Textualize/rich-cli
    """

    def format_help(self, ctx, formatter):

        class OptionHighlighter(RegexHighlighter):
            highlights = [r"(?P<switch>\-\w)",
                          r"(?P<option>\-\-[\w\-]+)",
                          r"(?P<unstable>[b][e][t][a])",
                          r"(?P<skl_title>[s][m][o][l]\-[k][8][s]\-[l][a][b])"]

        highlighter = OptionHighlighter()

        console = Console(theme=Theme({"option": "light_slate_blue",
                                       "switch": "sky_blue2",
                                       "meta": "light_steel_blue",
                                       "skl_title": "cornflower_blue"}),
                          highlighter=highlighter, record=RECORD)

        title ="🗺️ [cornflower_blue]kaartmaker[/]\n"
        desc = ("\n[steel_blue][i]Create maps of regions' voting patterns.\n")

        console.print(title + desc, justify="center")

        console.print("[steel_blue]Usage:[/] kaartmaker [option][OPTIONS]\n")

        options_table = Table(highlight=True, box=None, show_header=False,
                              row_styles=["", "dim"],
                              padding=(1, 1, 0, 0))

        for param in self.get_params(ctx):

            if len(param.opts) == 2:
                opt1 = highlighter(param.opts[1])
                opt2 = highlighter(param.opts[0])
            else:
                opt2 = highlighter(param.opts[0])
                opt1 = Text("")

            if param.metavar:
                opt2 += Text(f" {param.metavar}",
                             style="bold light_steel_blue")

            options = Text(" ".join(reversed(param.opts)))
            help_record = param.get_help_record(ctx)
            if help_record is None:
                help = ""
            else:
                help = Text.from_markup(param.get_help_record(ctx)[-1],
                                        emoji=False)

            if param.metavar:
                options += f" {param.metavar}"

            if "help" in opt1:
                opt1 = "-h"
                opt2 = "--help"

            options_table.add_row(opt1, opt2, highlighter(help))

        url = ("♥ docs: [link=https://github.com/smal-hack/kaartmaker]"
               "github.com/small-hack/kaartmaker[/link]")
        console.print(Panel(options_table,
                            border_style="light_steel_blue",
                            title="ʕ ᵔᴥᵔʔ Options",
                            title_align="left",
                            subtitle_align="right",
                            subtitle=url))

        # I use this to print a pretty svg at the end sometimes
        if RECORD:
            console.save_svg("examples/help_text.svg", title="term")

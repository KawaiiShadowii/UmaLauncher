import enum
from loguru import logger
import gui
import util
import constants
import settings_elements as se

TABLE_HEADERS = {
    "fac": "Facility",
    "speed": "Speed",
    "stamina": "Stamina",
    "power": "Power",
    "guts": "Guts",
    "wiz": "Wisdom",
    "ss_match": "SS Match"
}

class Colors(enum.Enum):
    """Defines the colors used in the helper table.
    """
    ALERT = "red"
    WARNING = "orange"
    GOOD = "lightgreen"


class Cell():
    def __init__(self, value="", bold=False, color=None, percent=False, title="", style="text-overflow: clip;white-space: nowrap;overflow: hidden;"):
        self.value = value
        self.bold = bold
        self.color = color
        self.percent = percent
        self.style = style
        self.title = title

    def to_td(self):
        style = self.style
        if self.bold:
            style += "font-weight:bold;"
        if self.color:
            style += f"color:{self.color};"
        if style:
            style = f" style=\"{style}\""
        
        title = self.title
        if title:
            title = title.replace('\n','')
            title = f" title=\"{title}\""
        return f"<td{style if style else ''}{title if title else ''}>{self.value}{'%' if self.percent else ''}</td>"


class Row():
    long_name = None
    short_name = None
    description = None
    settings = None
    cells = None

    dialog = None
    style = None

    """Defines a row in the helper table.
    """
    def __init__(self):
        self.dialog = None
        self.style = None
        self.disabled = False

    def _generate_cells(self, command_info) -> list[Cell]:
        """Returns a list of cells for this row.
        """
        cells = [Cell(self.short_name)]

        for command in command_info:
            cells.append(Cell())
        
        return cells

    def get_cells(self, command_info) -> list[Cell]:
        """Returns the value of the row at the given column index.
        """
        return self._generate_cells(command_info)

    def display_settings_dialog(self, parent):
        """Displays the settings dialog for this row.
        """
        settings_var = [self.settings]
        self.dialog = gui.UmaPresetSettingsDialog(parent, settings_var, window_title="Change row options")
        self.dialog.exec()
        self.dialog = None
        self.settings = settings_var[0]
    
    def to_tr(self, command_info):
        td = ''.join(cell.to_td() for cell in self.get_cells(command_info))
        return f"<tr{self.get_style()}>{td}</tr>"
    
    def get_style(self):
        if self.style:
            return f" style=\"{self.style}\""
        return ""
    
    def to_dict(self, row_types):
        return {
            "type": row_types(type(self)).name,
            "settings": self.settings.to_dict() if self.settings else {}
        }


class PresetSettings(se.Settings):
    def __init__(self):
        self.s_energy_enabled = se.Setting(
            "Show energy",
            "Displays energy in the event helper.",
            True,
            se.SettingType.BOOL,
            priority=10
        )
        self.s_skillpt_enabled = se.Setting(
            "Show skill points",
            "Displays skill points in the event helper.",
            False,
            se.SettingType.BOOL,
            priority=9
        )
        self.s_fans_enabled = se.Setting(
            "Show fans",
            "Displays fans in the event helper.",
            False,
            se.SettingType.BOOL,
            priority=8
        )
        self.s_schedule_enabled = se.Setting(
            "Show schedule countdown",
            "Displays the amount of turns until your next scheduled race. (If there is one.)",
            True,
            se.SettingType.BOOL,
            priority=7
        )
        self.s_scenario_specific_enabled = se.Setting(
            "Show scenario specific elements",
            "Show scenario specific elements in the event helper. \n(Grand Live tokens, Grand Masters fragments, Project L'Arc aptitude/supporter points & expectation gauge)",
            True,
            se.SettingType.BOOL,
            priority=6
        )


class Preset():
    name = None
    rows = None
    initialized_rows: list[Row] = None
    row_types = None

    gm_fragment_dict = util.get_gm_fragment_dict()
    gl_token_dict = util.get_gl_token_dict()

    def __init__(self, row_types):
        self.settings = PresetSettings()

        self.row_types = row_types
        if self.rows:
            self.initialized_rows = [row.value() for row in self.rows]
        else:
            self.initialized_rows = []

    def __iter__(self):
        return iter(self.initialized_rows)
    
    def __gt__(self, other):
        return self.name > other.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    def display_settings_dialog(self, parent):
        settings_var = [self.settings]
        self.dialog = gui.UmaPresetSettingsDialog(parent, settings_var, window_title="Toggle elements")
        self.dialog.exec()
        self.dialog = None
        self.settings = settings_var[0]
    
    def generate_overlay(self, main_info, command_info):
        html_elements = []

        if self.settings.s_energy_enabled.value:
            html_elements.append(self.generate_energy(main_info))

        if self.settings.s_skillpt_enabled.value:
            html_elements.append(self.generate_skillpt(main_info))

        if self.settings.s_fans_enabled.value:
            html_elements.append(self.generate_fans(main_info))
        
        if self.settings.s_schedule_enabled.value:
            html_elements.append(self.generate_schedule(main_info))

        if self.settings.s_scenario_specific_enabled.value:
            html_elements.append(self.generate_gm_table(main_info))
            html_elements.append(self.generate_gl_table(main_info))
            html_elements.append(self.generate_arc(main_info))

        html_elements.append(self.generate_table(command_info))

        # html_elements.append("""<button id="btn-skill-window" onclick="window.await_skill_window();">Open Skills Window</button>""")

        return ''.join(html_elements)
    
    def generate_energy(self, main_info):
        return f"<div id=\"energy\"><b>Energy:</b> {main_info['energy']}/{main_info['max_energy']}</div>"
    
    def generate_skillpt(self, main_info):
        return f"<div id=\"skill-pt\"><b>Skill Points:</b> {main_info['skillpt']:,}</div>"

    def generate_fans(self, main_info):
        return f"<div id=\"fans\"><b>Fans:</b> {main_info['fans']:,}</div>"
    
    def generate_table(self, command_info):
        if not command_info:
            return ""

        table_header = ''.join(f"""<th style="text-overflow: clip;white-space: nowrap;overflow: hidden;">{TABLE_HEADERS[header]}</th>""" for header in ["fac"] + [command for command in command_info])
        table = [f"<tr>{table_header}</tr>"]

        for row in self.initialized_rows:
            if not row.disabled:
                table.append(row.to_tr(command_info))

        thead = f"<thead>{table[0]}</thead>"
        tbody = f"<tbody>{''.join(table[1:])}</tbody>"
        return f"<table id=\"training-table\">{thead}{tbody}</table>"

    def generate_gm_table(self, main_info):
        if main_info['scenario_id'] != 5:
            return ""
        
        header = "<tr><th colspan=\"8\">Fragments</th></tr>"
    
        frag_tds = []
        for index, fragment_id in enumerate(main_info['gm_fragments']):
            frag_tds.append(f"<td style=\"{'outline: 1px solid red; outline-offset: -1px;' if index in (0, 4) else ''}\"><img src=\"{self.gm_fragment_dict[fragment_id]}\" height=\"32\" width=\"30\" style=\"display:block; margin: auto; width: auto; height: 32px;\" /></td>")
        
        frag_tr = f"<tr>{''.join(frag_tds)}</tr>"

        return f"<table id=\"gm-fragments\"><thead>{header}</thead><tbody>{frag_tr}</tbody></table>"

    def generate_gl_table(self, main_info):
        if main_info['scenario_id'] != 3:
            return ""
        
        top_row = []
        bottom_row = []

        for token_type in constants.GL_TOKEN_LIST:
            top_row.append(f"<th><img src=\"{self.gl_token_dict[token_type]}\" height=\"32\" width=\"31\" style=\"display:block; margin: auto; width: auto; height: 32px;\" /></th>")
            bottom_row.append(f"<td>{main_info['gl_stats'][token_type]}</td>")
        
        top_row = f"<tr>{''.join(top_row)}</tr>"
        bottom_row = f"<tr>{''.join(bottom_row)}</tr>"

        return f"<table id=\"gl-tokens\"><thead>{top_row}</thead><tbody>{bottom_row}</tbody></table>"
    
    def generate_schedule(self, main_info):
        cur_turn = main_info['turn']
        next_race = None
        for race in main_info['scheduled_races']:
            if race['turn'] >= cur_turn:
                next_race = race
                break
        
        if not next_race:
            return ""
        
        turns_left = next_race['turn'] - cur_turn
        text = f"<p><b>{turns_left} turn{'' if turns_left == 1 else 's'}</b> until</p>"
        img = f"<img width=100 height=50 src=\"{next_race['thumb_url']}\"/>"

        fan_warning = ""

        if main_info['fans'] < next_race['fans']:
            fans_needed = next_race['fans'] - main_info['fans']
            fan_warning = f"""<p style="color: orange; margin: 0;"><b>{fans_needed} more</b> fans needed!</p>"""

        return f"""<div id="schedule" style="display: flex; flex-direction: column; justify-content: center; align-items: center;"><div id="schedule-race-container" style="display: flex; align-items: center; gap: 0.5rem;">{text}{img}</div>{fan_warning}</div>"""

    def generate_arc(self, main_info):
        if main_info['scenario_id'] != 6 or main_info['turn'] < 3:
            return ""

        gauge_str = str(main_info['arc_expectation_gauge'] // 10)
        gauge_str2 = str(main_info['arc_expectation_gauge'] % 10)
        return f"<div id=\"arc\"><b>Aptitude Points:</b> {main_info['arc_aptitude_points']:,} - <b>Supporter Points:</b> {main_info['arc_supporter_points']:,} - <b>Expectation Gauge:</b> {gauge_str}.{gauge_str2}%</div>"

    def to_dict(self):
        return {
            "name": self.name,
            "settings": self.settings.to_dict(),
            "rows": [row.to_dict(self.row_types) for row in self.initialized_rows] if self.initialized_rows else []
        }
    
    def import_dict(self, preset_dict):
        if "name" in preset_dict:
            self.name = preset_dict["name"]
        if "settings" in preset_dict:
            self.settings.import_dict(preset_dict["settings"])
        if "rows" in preset_dict:
            self.initialized_rows = []
            for row_dict in preset_dict["rows"]:
                row_object = self.row_types[row_dict["type"]].value()
                if row_object.settings:
                    row_object.settings.import_dict(row_dict["settings"])
                self.initialized_rows.append(row_object)

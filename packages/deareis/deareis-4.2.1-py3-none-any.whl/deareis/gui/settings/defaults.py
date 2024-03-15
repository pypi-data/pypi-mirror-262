# DearEIS is licensed under the GPLv3 or later (https://www.gnu.org/licenses/gpl-3.0.html).
# Copyright 2023 DearEIS developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The licenses of DearEIS' dependencies and/or sources of portions of code are included in
# the LICENSES folder.

from typing import (
    Callable,
    List,
)
from pyimpspec import (
    get_default_num_procs,
    set_default_num_procs,
)
import dearpygui.dearpygui as dpg
from deareis.utility import calculate_window_position_dimensions
from deareis.tooltips import attach_tooltip
import deareis.tooltips as tooltips
from deareis.data.plotting import PlotExportSettings
from deareis.data import (
    DRTSettings,
    FitSettings,
    SimulationSettings,
    TestSettings,
    ZHITSettings,
)
from deareis.config import (
    DEFAULT_TEST_SETTINGS,
    DEFAULT_ZHIT_SETTINGS,
    DEFAULT_DRT_SETTINGS,
    DEFAULT_FIT_SETTINGS,
    DEFAULT_SIMULATION_SETTINGS,
    DEFAULT_PLOT_EXPORT_SETTINGS,
)
from deareis.gui.kramers_kronig import SettingsMenu as TestSettingsMenu
from deareis.gui.zhit import SettingsMenu as ZHITSettingsMenu
from deareis.gui.drt import SettingsMenu as DRTSettingsMenu
from deareis.gui.fitting import SettingsMenu as FitSettingsMenu
from deareis.gui.simulation import SettingsMenu as SimulationSettingsMenu
from deareis.gui.plotting.export import SettingsMenu as PlotExportSettingsMenu
from deareis.signals import Signal
import deareis.signals as signals


def section_spacer():
    dpg.add_spacer(height=8)


def general_settings(label_pad: int, state):
    with dpg.collapsing_header(label="General", default_open=True):
        auto_backup_interval: int = dpg.generate_uuid()
        num_procs_input: int = dpg.generate_uuid()

        def update_auto_backup_interval(value: int):
            state.config.auto_backup_interval = value
            set_default_num_procs(value)

        with dpg.group(horizontal=True):
            dpg.add_text("Auto-backup interval".rjust(label_pad))
            attach_tooltip(tooltips.general.auto_backup_interval)
            dpg.add_input_int(
                default_value=state.config.auto_backup_interval,
                label="actions",
                min_value=0,
                min_clamped=True,
                step=0,
                on_enter=True,
                callback=lambda s, a, u: update_auto_backup_interval(a),
                width=-54,
                tag=auto_backup_interval,
            )

        def update_num_procs(value: int):
            state.config.num_procs = value

        with dpg.group(horizontal=True):
            dpg.add_text("Number of processes".rjust(label_pad))
            attach_tooltip(tooltips.general.num_procs.format(get_default_num_procs()))
            dpg.add_input_int(
                default_value=state.config.num_procs,
                min_value=0,
                min_clamped=True,
                step=0,
                on_enter=True,
                callback=lambda s, a, u: update_num_procs(a),
                width=-54,
                tag=num_procs_input,
            )
        section_spacer()


def kramers_kronig_tab_settings(label_pad: int, state) -> Callable:
    with dpg.collapsing_header(label="Kramers-Kronig tab", default_open=True):
        settings_menu: TestSettingsMenu = TestSettingsMenu(
            state.config.default_test_settings,
            label_pad,
            limited=True,
        )
        with dpg.group(horizontal=True):
            dpg.add_text("".rjust(label_pad))
            dpg.add_button(
                label="Restore defaults",
                callback=lambda s, a, u: settings_menu.set_settings(
                    DEFAULT_TEST_SETTINGS,
                ),
            )
        section_spacer()

    def callback():
        settings: TestSettings = settings_menu.get_settings()
        state.config.default_test_settings = settings
        signals.emit(Signal.APPLY_TEST_SETTINGS, settings=settings)

    return callback


def zhit_tab_settings(label_pad: int, state) -> Callable:
    with dpg.collapsing_header(label="Z-HIT analysis tab", default_open=True):
        settings_menu: ZHITSettingsMenu = ZHITSettingsMenu(
            state.config.default_zhit_settings,
            label_pad,
        )
        with dpg.group(horizontal=True):
            dpg.add_text("".rjust(label_pad))
            dpg.add_button(
                label="Restore defaults",
                callback=lambda s, a, u: settings_menu.set_settings(
                    DEFAULT_ZHIT_SETTINGS,
                ),
            )
        section_spacer()

    def callback():
        settings: ZHITSettings = settings_menu.get_settings()
        state.config.default_zhit_settings = settings
        signals.emit(Signal.APPLY_ZHIT_SETTINGS, settings=settings)

    return callback


def drt_tab_settings(label_pad: int, state) -> Callable:
    with dpg.collapsing_header(label="DRT analysis tab", default_open=True):
        settings_menu: DRTSettingsMenu = DRTSettingsMenu(
            state.config.default_drt_settings,
            label_pad,
        )
        with dpg.group(horizontal=True):
            dpg.add_text("".rjust(label_pad))
            dpg.add_button(
                label="Restore defaults",
                callback=lambda s, a, u: settings_menu.set_settings(
                    DEFAULT_DRT_SETTINGS
                ),
            )
        section_spacer()

    def callback():
        settings: DRTSettings = settings_menu.get_settings()
        state.config.default_drt_settings = settings
        signals.emit(Signal.APPLY_DRT_SETTINGS, settings=settings)

    return callback


def fitting_tab_settings(label_pad: int, state) -> Callable:
    with dpg.collapsing_header(label="Fitting tab", default_open=True):
        settings_menu: FitSettingsMenu = FitSettingsMenu(
            state.config.default_fit_settings,
            label_pad,
        )
        with dpg.group(horizontal=True):
            dpg.add_text("".rjust(label_pad))
            dpg.add_button(
                label="Restore defaults",
                callback=lambda s, a, u: settings_menu.set_settings(
                    DEFAULT_FIT_SETTINGS,
                ),
            )
        section_spacer()

    def callback():
        settings: FitSettings = settings_menu.get_settings()
        state.config.default_fit_settings = settings
        signals.emit(Signal.APPLY_FIT_SETTINGS, settings=settings)

    return callback


def simulation_tab_settings(label_pad: int, state) -> Callable:
    with dpg.collapsing_header(label="Simulation tab", default_open=True):
        settings_menu: SimulationSettingsMenu = SimulationSettingsMenu(
            state.config.default_simulation_settings,
            label_pad,
        )
        with dpg.group(horizontal=True):
            dpg.add_text("".rjust(label_pad))
            dpg.add_button(
                label="Restore defaults",
                callback=lambda s, a, u: settings_menu.set_settings(
                    DEFAULT_SIMULATION_SETTINGS,
                ),
            )
        section_spacer()

    def callback():
        settings: SimulationSettings = settings_menu.get_settings()
        state.config.default_simulation_settings = settings
        signals.emit(Signal.APPLY_SIMULATION_SETTINGS, settings=settings)

    return callback


def plotting_tab_settings(label_pad: int, state) -> Callable:
    with dpg.collapsing_header(label="Plotting tab - Export plot", default_open=True):
        settings_menu: PlotExportSettingsMenu = PlotExportSettingsMenu(
            state.config.default_plot_export_settings,
            label_pad,
            refresh_callback=None,
        )
        with dpg.group(horizontal=True):
            dpg.add_text("".rjust(label_pad))
            dpg.add_button(
                label="Restore defaults",
                callback=lambda s, a, u: settings_menu.set_settings(
                    DEFAULT_PLOT_EXPORT_SETTINGS,
                ),
            )
        section_spacer()

    def callback():
        settings: PlotExportSettings = settings_menu.get_settings()
        state.config.default_plot_export_settings = settings
        state.plot_exporter.set_settings(settings)

    return callback


class DefaultsSettings:
    def __init__(self, state):
        self.settings_update_callbacks: List[Callable] = []
        self.create_window(state)
        self.register_keybindings()

    def register_keybindings(self):
        self.key_handler: int = dpg.generate_uuid()
        with dpg.handler_registry(tag=self.key_handler):
            dpg.add_key_release_handler(
                key=dpg.mvKey_Escape,
                callback=self.close,
            )

    def create_window(self, state):
        x: int
        y: int
        w: int
        h: int
        x, y, w, h = calculate_window_position_dimensions(390, 540)
        self.window: int = dpg.generate_uuid()
        with dpg.window(
            label="Settings - defaults",
            modal=True,
            pos=(x, y),
            width=w,
            height=h,
            no_resize=True,
            on_close=self.close,
            tag=self.window,
        ):
            label_pad: int = 24
            general_settings(label_pad, state)
            self.settings_update_callbacks.append(
                kramers_kronig_tab_settings(label_pad, state)
            )
            self.settings_update_callbacks.append(zhit_tab_settings(label_pad, state))
            self.settings_update_callbacks.append(drt_tab_settings(label_pad, state))
            self.settings_update_callbacks.append(
                fitting_tab_settings(label_pad, state)
            )
            self.settings_update_callbacks.append(
                simulation_tab_settings(label_pad, state)
            )
            self.settings_update_callbacks.append(
                plotting_tab_settings(label_pad, state)
            )
        signals.emit(Signal.BLOCK_KEYBINDINGS, window=self.window, window_object=self)

    def close(self):
        for callback in self.settings_update_callbacks:
            callback()
        if dpg.does_item_exist(self.window):
            dpg.delete_item(self.window)
        if dpg.does_item_exist(self.key_handler):
            dpg.delete_item(self.key_handler)
        signals.emit(Signal.UNBLOCK_KEYBINDINGS)


def show_defaults_settings_window(state):
    DefaultsSettings(state)

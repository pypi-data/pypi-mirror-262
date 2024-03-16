import pickle

import pygame
import pygame_gui

from racingenv import resource_dir
from racingenv.physics.simulation import Simulation
from racingenv.renderer.resourcemanager import ResourceManager
from racingenv.renderer.simulationrenderer import SimulationRenderer
from racingenv.physics.car import Action


def transform_action(action):
    if action & Action.FORWARD != 0 and action & Action.RIGHT != 0:
        return 4
    elif action & Action.FORWARD != 0 and action & Action.LEFT != 0:
        return 5
    elif action & Action.FORWARD != 0:
        return 0
    elif action & Action.BACKWARD != 0:
        return 1
    elif action & Action.LEFT != 0:
        return 2
    elif action & Action.RIGHT != 0:
        return 3
    else:
        return 6


class PhysicsEditor:
    def __init__(self, physics_settings=None):
        self.width = 1920
        self.height = 1080
        self.draw_debug = False
        self.running = True

        pygame.init()
        pygame.display.set_caption("RLRacer Physics Editor")
        self.screen = pygame.display.set_mode([self.width, self.height])

        self.clock = pygame.time.Clock()

        self.manager = pygame_gui.UIManager((self.width, self.height))

        if physics_settings is not None:
            self.physics_settings = physics_settings
        else:
            self.physics_settings = {
                "max_velocity": 7.5,
                "acceleration": 0.16,
                "drag": 0.48,
                "max_lateral_velocity": 1.2,
                "lateral_acceleration": 0.144,
                "lateral_drag": 0.48,
                "angular_velocity": 6.0,
                "drift_threshold": 2.5
            }

        self.resource_manager = ResourceManager(resource_dir + '/Resources/Textures/', True)
        self.simulation = Simulation(self.resource_manager, self.physics_settings, 8)
        self.simulation.reset()
        self.renderer = SimulationRenderer("human", 960, 960)
        self.action = Action.NONE

        self.ui_window = pygame_gui.elements.UIWindow(rect=pygame.Rect(50.0, 50.0, 425.0, 950.0),
                                                      manager=self.manager, window_display_title="Physics settings")

        self.velocity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 10.0, 350.0, 50.0),
            start_value=self.physics_settings["max_velocity"],
            value_range=(1.0, 25.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.1)
        self.velocity_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 50.0, 350.0, 50.0),
            text="Max Velocity: {0:.1f}".format(self.physics_settings["max_velocity"]),
            manager=self.manager,
            container=self.ui_window)

        self.acceleration_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 110.0, 350.0, 50.0),
            start_value=self.physics_settings["acceleration"],
            value_range=(0.001, 5.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.001)
        self.acceleration_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 150.0, 350.0, 50.0),
            text="Acceleration: {0:.3f}".format(self.physics_settings["acceleration"]),
            manager=self.manager,
            container=self.ui_window)

        self.drag_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 210.0, 350.0, 50.0),
            start_value=self.physics_settings["drag"],
            value_range=(0.0, 5.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.01)
        self.drag_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 250.0, 350.0, 50.0),
            text="Drag: {0:.2f}".format(self.physics_settings["drag"]),
            manager=self.manager,
            container=self.ui_window)

        self.lateral_velocity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 310.0, 350.0, 50.0),
            start_value=self.physics_settings["max_lateral_velocity"],
            value_range=(0.0, 20.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.01)
        self.lateral_velocity_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 350.0, 350.0, 50.0),
            text="Max Lateral Velocity: {0:.2f}".format(self.physics_settings["max_lateral_velocity"]),
            manager=self.manager,
            container=self.ui_window)

        self.lateral_acceleration_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 410.0, 350.0, 50.0),
            start_value=self.physics_settings["lateral_acceleration"],
            value_range=(0.0, 2.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.001)
        self.lateral_acceleration_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0.0, 450.0, 350.0, 50.0),
            text="Lateral Acceleration: {0:.3f}".format(self.physics_settings["lateral_acceleration"]),
            manager=self.manager,
            container=self.ui_window)

        self.lateral_drag_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 510.0, 350.0, 50.0),
            start_value=self.physics_settings["lateral_drag"],
            value_range=(0.0, 5.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.001)
        self.lateral_drag_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 550.0, 350.0, 50.0),
            text="Lateral Drag: {0:.3f}".format(self.physics_settings["lateral_drag"]),
            manager=self.manager,
            container=self.ui_window)

        self.angular_velocity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 610.0, 350.0, 50.0),
            start_value=self.physics_settings["angular_velocity"],
            value_range=(0.1, 25.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.1)
        self.angular_velocity_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 650.0, 200.0, 50.0),
            text="Max Angular Velocity: {0:.1f}".format(self.physics_settings["angular_velocity"]),
            manager=self.manager,
            container=self.ui_window)

        self.drift_threshold_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(25.0, 710.0, 350.0, 50.0),
            start_value=self.physics_settings["drift_threshold"],
            value_range=(0.1, 25.0),
            manager=self.manager,
            container=self.ui_window,
            click_increment=0.1)
        self.drift_threshold_slider_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(25.0, 750.0, 350.0, 50.0),
            text="Drift Threshold: {0:.1f}".format(self.physics_settings["drift_threshold"]),
            manager=self.manager,
            container=self.ui_window)

        self.export_settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(25.0, 810.0, 350.0, 50.0),
            text="Export Settings",
            manager=self.manager,
            container=self.ui_window
        )

        self.export_settings_dialog = pygame_gui.windows.UIFileDialog(
            rect=pygame.Rect(50.0, 50.0, 500.0, 400.0),
            manager=self.manager
        )
        self.export_settings_dialog.hide()

    def main(self):
        self.running = True

        while self.running:
            self.update()
            self.render()

            if not self.simulation.player.alive:
                self.simulation.reset()

    def process_events(self):
        time_delta = self.clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.action |= Action.FORWARD
                elif event.key == pygame.K_s:
                    self.action |= Action.BACKWARD
                elif event.key == pygame.K_a:
                    self.action |= Action.LEFT
                elif event.key == pygame.K_d:
                    self.action |= Action.RIGHT
                elif event.key == pygame.K_TAB:
                    self.draw_debug = not self.draw_debug
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.action ^= Action.FORWARD
                elif event.key == pygame.K_s:
                    self.action ^= Action.BACKWARD
                elif event.key == pygame.K_a:
                    self.action ^= Action.LEFT
                elif event.key == pygame.K_d:
                    self.action ^= Action.RIGHT
            elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                self.process_slider_events(event)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.export_settings_button:
                    self.export_settings_dialog.show()
            elif event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                with open('Resources/Physics/', 'wb+') as f:
                    pickle.dump(self.physics_settings, f)

            self.manager.process_events(event)

        self.manager.update(time_delta)
        self.simulation.player.update_physics_settings(self.physics_settings)

    def process_slider_events(self, event):
        if event.ui_element == self.velocity_slider:
            self.velocity_slider_label.set_text("Velocity: {0:.2f}".
                                                format(self.velocity_slider.current_value))
            self.physics_settings["max_velocity"] = round(self.velocity_slider.current_value, 2)
        elif event.ui_element == self.acceleration_slider:
            self.acceleration_slider_label.set_text("Acceleration: {0:.3f}".
                                                    format(self.acceleration_slider.current_value))
            self.physics_settings["acceleration"] = round(self.acceleration_slider.current_value, 3)
        elif event.ui_element == self.drag_slider:
            self.drag_slider_label.set_text("Drag: {0:.3f}".
                                            format(self.drag_slider.current_value))
            self.physics_settings["drag"] = round(self.drag_slider.current_value, 3)
        elif event.ui_element == self.lateral_velocity_slider:
            self.lateral_velocity_slider_label.set_text("Max Lateral Velocity: {0:.2f}".
                                                        format(self.lateral_velocity_slider.current_value))
            self.physics_settings["max_lateral_velocity"] = round(self.lateral_velocity_slider.current_value, 2)
        elif event.ui_element == self.lateral_acceleration_slider:
            self.lateral_acceleration_slider_label.set_text("Lateral Acceleration: {0:.3f}".format(
                self.lateral_acceleration_slider.current_value))
            self.physics_settings["lateral_acceleration"] = round(self.lateral_acceleration_slider.current_value, 3)
        elif event.ui_element == self.lateral_drag_slider:
            self.lateral_drag_slider_label.set_text("Lateral Drag: {0:.3f}".
                                                    format(self.lateral_drag_slider.current_value))
            self.physics_settings["lateral_drag"] = round(self.lateral_drag_slider.current_value, 3)
        elif event.ui_element == self.angular_velocity_slider:
            self.angular_velocity_slider_label.set_text("Max Angular Velocity: {0:.2f}".
                                                        format(self.angular_velocity_slider.current_value))
            self.physics_settings["angular_velocity"] = round(self.angular_velocity_slider.current_value, 2)
        elif event.ui_element == self.drift_threshold_slider:
            self.drift_threshold_slider_label.set_text("Drift Threshold: {0:.2f}".
                                                       format(self.drift_threshold_slider.current_value))
            self.physics_settings["drift_threshold"] = round(self.drift_threshold_slider.current_value, 2)

    def update(self):
        self.process_events()
        self.simulation.step(transform_action(self.action))
        self.renderer.camera.set(self.simulation.player.position.x - self.renderer.camera.viewport.width / 2.0,
                                 self.simulation.player.position.y - self.renderer.camera.viewport.height / 2.0)

    def render(self):
        self.renderer.render(self.simulation, self.draw_debug, self.screen)
        self.manager.draw_ui(self.screen)

        pygame.display.flip()



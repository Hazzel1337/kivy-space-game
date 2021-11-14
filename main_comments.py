import shapely
from kivy.app import App
from kivy.graphics.context_instructions import Scale, Translate, Color, PushMatrix, Rotate, PopMatrix
from kivy.graphics.fbo import Fbo
from kivy.graphics.gl_instructions import ClearColor, ClearBuffers
from kivy.graphics.transformation import Matrix
from kivy.graphics.vertex_instructions import Rectangle, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
import random
from random import randint, choice, choices
from kivy.properties import NumericProperty
from kivy.vector import Vector
from shapely.geometry import Polygon
from shapely.affinity import rotate
import numpy as np

from rotabox import Rotabox

# test_poly = sympy.Polygon(p1, p2, p3, p4) #makes a polygon
# c1 = Circle((0, 0), 5)

from pipe import Pipe



class Floatlayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class arrow(GridLayout):


    def __init__(self, **kwargs):
        super(arrow, self).__init__(**kwargs)







class Projectile2(Image):


    max_travel_distance = 100
    already_travled = Vector(0, 0)


    def __init__(self, start_pos, target_pos, **kwargs):
        super(Projectile, self).__init__(**kwargs)
        self.pos = start_pos
        self.target_pos = target_pos
        self.angle = Vector(1, 0).angle(self.target_pos)  * -1
        self.calc_move_me()
        self.source = "Shot1/shot1_4.png"
        self.size_hint = (None, None)
        self.size = (64, 64)


    def calc_move_me(self):

        fuss = Vector(self.pos)

        # to get the middle of the ship, instead of topleft/topright
        fuss.x = fuss.x + self.size[0] * 0.5
        fuss.y = fuss.y + self.size[1] * 0.5

        spitze = Vector(self.target_pos)
        self.waypoint = spitze
        self.travel_vec = spitze - fuss

    def move_me(self):
        self.pos = Vector(self.pos) + self.travel_vec.normalize()
        self.already_travled += self.travel_vec.normalize()

    def update_hitbox(self):
        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])



class Projectile(Rotabox):





    def __init__(self, start_pos, target_pos, **kwargs):
        super(Projectile, self).__init__(**kwargs)
        self.pos = start_pos
        self.target_pos = target_pos
        self.target_vec = Vector(self.target_pos) - Vector(self.pos)
        self.angle = Vector(1, 0).angle(self.target_vec) *-1 #90° imagined Vector
        self.calc_move_me()

        self.max_travel_distance = 100
        self.already_travled = Vector(0, 0)

        self.animcounter = 0
        self.source1 = "Shot1/shot1_1.png"
        self.source2 = "Shot1/shot1_2.png"
        self.source3 = "Shot1/shot1_3.png"
        self.source4 = "Shot1/shot1_4.png"
        self.source_l = [self.source1, self.source2, self.source3, self.source4]
        self.add_widget(Image(source=self.source_l[0]))

        self.custom_bounds = [
        [(0.031, 0.469), (0.031, 0.516), (0.094, 0.594), (0.203, 0.672),
         (0.328, 0.719), (0.737, 0.722), (0.938, 0.516), (0.938, 0.453),
         (0.797, 0.328), (0.766, 0.344), (0.672, 0.297), (0.438, 0.281),
         (0.344, 0.297), (0.328, 0.281), (0.25, 0.359)]]
        self.draw_bounds = 1

        #for removing it
        self.i_am_done = False





    def calc_move_me(self):

        fuss = Vector(self.pos)

        # to get the middle of the ship, instead of topleft/topright
        fuss.x = fuss.x + self.size[0] * 0.5
        fuss.y = fuss.y + self.size[1] * 0.5

        spitze = Vector(self.target_pos)
        self.waypoint = spitze
        self.travel_vec = spitze - fuss

    def move_me(self):
        self.pos = Vector(self.pos) + self.travel_vec.normalize()
        self.already_travled += self.travel_vec.normalize()
        if abs(self.already_travled.x) >= abs(self.travel_vec.normalize().x * 300) and abs(self.already_travled.y) >= abs(self.travel_vec.normalize().y * 300):
            #print(self.already_travled)
            #print(self.travel_vec.normalize() * 300)
            if self.parent:
                self.parent.ids["ship"].projectile_list.remove(self)
                self.parent.remove_widget(self)



    def update_hitbox(self):
        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])

    def animate_ontime(self, time_passed):  # needs to have that to be scheduled

        if self.animcounter < len(self.source_l) - 1:
            self.animcounter += 1
            self.children[0].source = self.source_l[self.animcounter]





class Background(Widget):
    bg0 = ObjectProperty(None)
    bg1 = ObjectProperty(None)
    bg2 = ObjectProperty(None)
    bg3 = ObjectProperty(None)
    bg4 = ObjectProperty(None)


    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)



        # keyboard


        # self._keyboard = Window.request_keyboard(
        #     self._keyboard_closed, self, 'text')
        # if self._keyboard.widget:
        #     # If it exists, this widget is a VKeyboard object which you can use
        #     # to change the keyboard layout.
        #     pass
        # self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # background texture ?

        self.bg0 = Image(source="bg/bg0.png").texture
        self.bg1 = Image(source="bg/bg1.png").texture
        self.bg2 = Image(source="bg/bg2.png").texture
        self.bg3 = Image(source="bg/bg3.png").texture
        self.bg4 = Image(source="bg/bg4.png").texture
        self.bgtextures_avail_list = [self.bg0, self.bg1]

        # self.bg0.uvsize = self.bg0.size
        self.bg0.wrap = "repeat"

        # Create textures
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

        self.bg_list = self.make_bg()
        self.draw_bg(self.bg_list)

    def on_size(self, *args):

        self.bg_list = self.make_bg()
        self.animate_bg(self.bg_list)
        self.draw_bg(self.bg_list)

        self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (self.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        self.cloud_texture.uvpos = (
        (self.cloud_texture.uvpos[0] + time_passed / 2.0) % Window.width, self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = (
        (self.floor_texture.uvpos[0] + time_passed) % Window.width, self.floor_texture.uvpos[1])

        # Redraw the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)

    def make_bg(self):
        # make rectangles for background

        bg_l = []

        for w in range(int(Window.width / self.bg0.size[0]) + 1):
            for h in range(int(Window.height / self.bg0.size[1]) + 1):
                bg_l.append(Rectangle(pos=(0 + (w * 200), 0 + (h * 200)), size=(200, 200), texture=self.bg0))

        return bg_l
        # add them to the bg canvas

    def draw_bg(self, bg_l):
        self.canvas.clear()

        with self.canvas.before:
            for rect in bg_l:
                self.canvas.add(rect)


        self.canvas.ask_update()

    def animate_bg(self, bg_list):  # needs to have that to be scheduled
        # chose tile to change
        for rect in bg_list:
            if random.randint(0, 10) > 5:
                rect.texture = random.choice(self.bgtextures_avail_list)

    def change_bg_on_time(self, timepassed):  # needs to have that to be scheduled
        self.animate_bg(self.bg_list)
        self.draw_bg(self.bg_list)

    # def _keyboard_closed(self):
    #     #print('My keyboard have been closed!')
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None
    #
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     #print('The key', keycode, 'have been pressed')
    #     #print(' - text is %r' % text)
    #     #print(' - modifiers are %r' % modifiers)
    #
    #     # Keycode is composed of an integer + a string
    #     # If we hit escape, release the keyboard
    #     if keycode[1] == 'escape':
    #         keyboard.release()
    #
    #     # Return True to accept the key. Otherwise, it will be used by
    #     # the system.
    #     return True
    #
    # def draw_projectiles(self):
    #     pass


        # for p in self.parent.ids["ship"].projectile_list:
        #     self.parent.add_widget(p)
        #
        #
        #     with self.canvas.before:
        #         self.canvas.add(p)
        #
        #
        # self.canvas.ask_update()



class Ship(Image):
    velocity = NumericProperty(0)
    acceleration = NumericProperty(5)
    waypoint = (0, 0)
    travelvec = (0, 0)
    traveled_already = Vector(0, 0)
    up = NumericProperty(1)
    #movement
    move_up_boolean = False
    move_down_boolean = False
    move_left_boolean = False
    move_right_boolean = False
    #projectiles
    projectile_list =[]


    def __init__(self, **kwargs):
        super(Ship, self).__init__(**kwargs)

        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])

        self.source = "Ship1.png"
        self.size_hint = (None, None)
        self.size = (64, 64)




        #self.hitbox = sympy.Polygon(self.p1, self.p2, self.p3, self.p4)


    def update_hitbox(self):

        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])
        self.hitbox = shapely.affinity.rotate(self.hitbox, angle=90)
        #print(self.children)

    def rotate(self):
        #kivy part
        with self.canvas.before:
            PushMatrix()
            Rotate(origin=self.center, angle=90)

        with self.canvas.after:
            PopMatrix()


        self.hitbox = shapely.affinity.rotate(self.hitbox, angle=90)
        #print(self.children)


    def on_touch_down(self, touch):

        if len(self.projectile_list) < 100:
            self.projectile_list.append(Projectile(self.center, touch.pos))
            self.parent.add_widget(self.projectile_list[-1])

            Clock.schedule_interval(self.projectile_list[-1].animate_ontime, 0.2)
            #p_ = Vector(self.pos)
            #print(p_.angle(touch.pos))


        self.source = "Ship1.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "Ship1.png"
        super().on_touch_up(touch)

    def move_up(self, widget):
        if widget.state == "down":
            self.move_up_boolean = True
        else:
            self.move_up_boolean = False


    def move_down(self, widget):
        if widget.state == "down":
            self.move_down_boolean = True
        else:
            self.move_down_boolean = False


    def move_left(self, widget):
        if widget.state == "down":
            self.move_left_boolean = True

        else:
            self.move_left_boolean = False


    def move_right(self, widget):
        if widget.state == "down":
            self.move_right_boolean = True

        else:
            self.move_right_boolean = False

    def move_topleft(self, widget):
        if widget.state == "down":
            self.move_left_boolean = True
            self.move_up_boolean = True

        else:
            self.move_left_boolean = False
            self.move_up_boolean = False

    def move_downleft(self, widget):
        if widget.state == "down":
            self.move_left_boolean = True
            self.move_down_boolean = True

        else:
            self.move_left_boolean = False
            self.move_down_boolean = False

    def move_topright(self,widget):
        if widget.state == "down":
            self.move_right_boolean = True
            self.move_up_boolean = True

        else:
            self.move_right_boolean = False
            self.move_up_boolean = False

    def move_downright(self,widget):
        if widget.state == "down":
            self.move_right_boolean = True
            self.move_down_boolean = True

        else:
            self.move_right_boolean = False
            self.move_down_boolean = False








class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        #print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #print('The key', keycode, 'have been pressed')
        #print(' - text is %r' % text)
        #print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True



class MainApp(App):
    pipes = []
    GRAVITY = 300
    was_colliding = False




    def check_collision(self):
        bird = self.root.ids.bird
        # Go through each pipe and check if it collides
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True
                # Check if bird is between the gap
                if bird.y < (pipe.pipe_center - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (pipe.pipe_center + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 96:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.root.ids.bird.pos = (20, (self.root.height - 96) / 2.0)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1


    def next_frame(self, time_passed):
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_textures(time_passed)
        self.ship_moveme()


        for p in self.root.ids.ship.projectile_list:
            p.move_me()

            if p.collide_widget(self.root.ids.ship):

                with self.root.ids.background.canvas:
                    Color(1, 0, 0, 1, mode='rgba')
                    #Rectangle(pos=p.pos, size=p.size)



            with self.root.ids.background.canvas:
                Color(1, 0, 0, 1, mode='rgba')
                Line(pos=self.root.ids.ship.p1, points=(self.root.ids.ship.p1,self.root.ids.ship.p2,self.root.ids.ship.p3,self.root.ids.ship.p4,self.root.ids.ship.p1), width=1)

                Rectangle(pos=self.root.ids.ship.pos, size=self.root.ids.ship.size)
                #Rectangle(pos=p.pos, size=p.size)
                #Rectangle(pos=point_to_check, size=(10, 10))
                #Color(0, 1, 0, 1, mode='rgba')

                #Rectangle(pos=self.root.ids.ship.pos, size=self.root.ids.ship.size)
                #Rectangle(pos=point_to_check2, size=(10, 10))
                #Ellipse(pos=(self.root.ids.ship.center_x -25, self.root.ids.ship.center_y -25), size= (50,  50))

                #Rectangle(pos=p.pos, size=(p.pos[0], p.pos[1]))
                #Rectangle(pos=(self.root.ids.ship.center_x , self.root.ids.ship.center_y ), size=(50,  50))

            self.root.ids.background.canvas.ask_update()



        self.root.ids.background.draw_projectiles()

        #self.root.ids.ship.collide_widget(self.root.ids)




              # #print(abs(Vector(self.root.ids.ship.pos).distance(self.root.ids.ship.waypoint)))
        # if abs(self.root.ids.ship.traveled_already.x) < abs(self.root.ids.ship.travel_vec.x) and abs(self.root.ids.ship.traveled_already.y) < abs(self.root.ids.ship.travel_vec.y):
        #     self.root.ids.ship.pos = Vector(self.root.ids.ship.pos) + self.root.ids.ship.travel_vec.normalize()
        #     self.root.ids.ship.traveled_already += self.root.ids.ship.travel_vec.normalize()
        # print(self.root.ids.bird.pos[1])



    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        #Clock.schedule_interval(self.move_bird, 1/60.)

        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

        Clock.schedule_interval(self.root.ids.background.change_bg_on_time, 1)



        # Create the pipes
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(96 + 100, self.root.height - 100)
            pipe.size_hint = (None, None)
            pipe.pos = (Window.width + i*distance_between_pipes, 96)
            pipe.size = (64, self.root.height - 96)

            self.pipes.append(pipe)
            self.root.add_widget(pipe)


        #print(self.root.walk)
        #print(self.root.ids)

        # Move the pipes
        #Clock.schedule_interval(self.move_pipes, 1/60.)

    def move_pipes(self, time_passed):
        # Move pipes
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # Check if we need to reposition the pipe at the right side
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width

    def ship_moveme(self):
        ship = self.root.ids.ship

        if ship.move_up_boolean:
            ship.center_y += 1
        elif ship.move_down_boolean:
            ship.center_y -=1

        if ship.move_left_boolean:
            ship.center_x -= 1
        elif ship.move_right_boolean:
            ship.center_x +=1




if __name__ == '__main__':
    MainApp().run()


MainApp().run()



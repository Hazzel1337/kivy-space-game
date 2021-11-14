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
from random import randint
from kivy.properties import NumericProperty
from kivy.vector import Vector
from asset_atlas import ships_atlas
from rotabox import Rotabox



from pipe import Pipe



class Floatlayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class arrow(GridLayout):


    def __init__(self, **kwargs):
        super(arrow, self).__init__(**kwargs)




class Projectile(Rotabox):


    def __init__(self, start_pos, target_pos, type, **kwargs):
        super(Projectile, self).__init__(**kwargs)
        self.pos = start_pos
        self.target_pos = target_pos
        self.target_vec = Vector(self.target_pos) - Vector(self.pos)
        self.angle = Vector(1, 0).angle(self.target_vec) *-1
        self.calc_move_me()

        self.max_travel_distance = 100
        self.already_travled = Vector(0, 0)

        self.animcounter = 0
        self.type = type
        self.add_widget(Image(source=ships_atlas[type]["shots"][0]))
        print(ships_atlas[type]["shots-bounds"][0])



        self.custom_bounds = [ships_atlas[type]["shots-bounds"][0]]

        self.draw_bounds = 1

        #for removing it
        self.i_am_done = False

        self.size = ("32dp", "32dp")



    def calc_move_me(self):

        fuss = Vector(self.pos)


        fuss.x = fuss.x + self.size[0] * 0.5
        fuss.y = fuss.y + self.size[1] * 0.5

        spitze = Vector(self.target_pos)
        self.waypoint = spitze
        self.travel_vec = spitze - fuss

    def move_me(self):
        self.pos = Vector(self.pos) + self.travel_vec.normalize()
        self.already_travled += self.travel_vec.normalize()
        if abs(self.already_travled.x) >= abs(self.travel_vec.normalize().x * 300) and abs(self.already_travled.y) >= abs(self.travel_vec.normalize().y * 300):

            if self.parent:
                self.parent.ids["ship"].projectile_list.remove(self)
                self.parent.remove_widget(self)


    def animate_ontime(self, time_passed):

        if self.animcounter < len(ships_atlas[self.type]["shots"]) - 1:
            self.animcounter += 1
            self.children[0].source = ships_atlas[self.type]["shots"][self.animcounter]
            self.custom_bounds = [ships_atlas[self.type]["shots-bounds"][self.animcounter]]





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


        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)



        self.bg0 = Image(source="bg/bg0.png").texture
        self.bg1 = Image(source="bg/bg1.png").texture
        self.bg2 = Image(source="bg/bg2.png").texture
        self.bg3 = Image(source="bg/bg3.png").texture
        self.bg4 = Image(source="bg/bg4.png").texture
        self.bgtextures_avail_list = [self.bg0, self.bg1]


        self.bg0.wrap = "repeat"


        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

        self.bg_list_defaultpos = []
        self.bg_list = self.make_bg()
        self.draw_bg(self.bg_list)

    def on_size(self, *args):

        self.bg_list = self.make_bg()
        self.animate_bg(self.bg_list)
        self.draw_bg(self.bg_list)

        self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (self.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):

        self.cloud_texture.uvpos = (
        (self.cloud_texture.uvpos[0] + time_passed / 2.0) % Window.width, self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = (
        (self.floor_texture.uvpos[0] + time_passed) % Window.width, self.floor_texture.uvpos[1])


        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)

    def make_bg(self):


        bg_l = []

        for w in range(int(Window.width / self.bg0.size[0]) + 2):
            for h in range(int(Window.height / self.bg0.size[1]) + 2):
                bg_l.append(Rectangle(pos=(0 - self.bg0.size[0] + (w * 200), 0 - self.bg0.size[1] + (h * 200)), size=(200, 200), texture=self.bg0))
                self.bg_list_defaultpos.append((0 - self.bg0.size[0] + (w * 200), 0 - self.bg0.size[1] + (h * 200)))
        return bg_l


    def draw_bg(self, bg_l):
        self.canvas.clear()

        with self.canvas.before:
            for rect in bg_l:
                self.canvas.add(rect)


        self.canvas.ask_update()

    def animate_bg(self, bg_list):

        for rect in bg_list:
            if random.randint(0, 10) > 5:
                rect.texture = random.choice(self.bgtextures_avail_list)

    def change_bg_on_time(self, timepassed):
        self.animate_bg(self.bg_list)
        self.draw_bg(self.bg_list)

    def scroll_bg(self, offset):
        for tile in self.bg_list:

            tile.pos = tile.pos[0] + offset[0], tile.pos[1] + offset[1]

        if self.bg_list[0].pos[0] + self.bg0.size[0] > self.bg0.size[0]:
            for idx, tile in enumerate(self.bg_list):
                tile.pos = self.bg_list_defaultpos[idx]
        elif self.bg_list[0].pos[0] + self.bg0.size[0] < self.bg0.size[0] * -1:
            for idx, tile in enumerate(self.bg_list):
                tile.pos = self.bg_list_defaultpos[idx]
        elif self.bg_list[0].pos[1] + self.bg0.size[1] > self.bg0.size[1]:
            for idx, tile in enumerate(self.bg_list):
                tile.pos = self.bg_list_defaultpos[idx]
        elif self.bg_list[0].pos[1] + self.bg0.size[1] < self.bg0.size[1] * -1:
            for idx, tile in enumerate(self.bg_list):
                tile.pos = self.bg_list_defaultpos[idx]




    def _keyboard_closed(self):
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if keycode[1] == 'escape':
            keyboard.release()


        return True



class Ship(Image):
    velocity = NumericProperty(0)
    acceleration = NumericProperty(5)
    waypoint = (0, 0)
    travelvec = (0, 0)
    traveled_already = Vector(0, 0)
    up = NumericProperty(1)

    move_up_boolean = False
    move_down_boolean = False
    move_left_boolean = False
    move_right_boolean = False

    projectile_list =[]


    def __init__(self, **kwargs):
        super(Ship, self).__init__(**kwargs)

        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)


        self.source = "Ship1.png"
        self.allow_stretch = True
        self.size_hint = (None, None)
        self.size = ("64dp", "64dp")




    def on_touch_down(self, touch):

        if len(self.projectile_list) < 100:
            self.projectile_list.append(Projectile(self.center, touch.pos, 5))
            self.parent.add_widget(self.projectile_list[-1])

            Clock.schedule_interval(self.projectile_list[-1].animate_ontime, 0.2)



        self.source = "Ship1.png"
        self.velocity = 150
        super(Ship, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "Ship1.png"
        super(Ship, self).on_touch_up(touch)

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




class Ship2(Rotabox):
    velocity = NumericProperty(0)
    acceleration = NumericProperty(5)


    def __init__(self,startpos,type, **kwargs):
        super(Ship2, self).__init__(**kwargs)

        self.projectile_list =[]
        self.type = type
        self.source = ships_atlas[type]["ship"][0]
        self.add_widget(Image(source=self.source))
        self.custom_bounds = ships_atlas[type]["ship-bounds"]
        self.allow_stretch = True
        self.size = ("64dp", "64dp")

        #self.pos = (Window.width * 1), Window.height * 0.5
        #self.original_pos = (Window.width * 1), Window.height * 0.5
        self.pos = startpos
        self.original_pos = startpos

        #calc travel vec
        self.travel_vec = Vector(self.new_destination()) - Vector(self.pos)
        self.already_travled = Vector(0,0)


    def shoot_target(self, targetpos):
        self.projectile_list.append(Projectile(self.center, targetpos, self.type))
        self.parent.add_widget(self.projectile_list[-1])
        Clock.schedule_interval(self.projectile_list[-1].animate_ontime, 0.5)


    def move_me(self, offset):
        self.original_pos = Vector(self.original_pos) + self.travel_vec.normalize()
        self.already_travled += self.travel_vec.normalize()
        if abs(self.already_travled.x) >= abs(self.travel_vec.x) and abs(self.already_travled.y) >= abs(self.travel_vec.y):
            self.travel_vec = Vector(self.new_destination()) - Vector(self.original_pos)
            self.already_travled = Vector(0, 0)

            # if self.parent:
            #     self.parent.ids["ship"].projectile_list.remove(self)
            #     self.parent.remove_widget(self)


        self.pos = Vector(self.original_pos) - offset

    def new_destination(self):
        # imaginary rect
        x = randint(Window.width, Window.width * 2)
        y = randint(0, Window.height)
        return Vector(x, y)




class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:

            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):

        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):



        if keycode[1] == 'escape':
            keyboard.release()


        return True



class MainApp(App):
    pipes = []
    GRAVITY = 300
    was_colliding = False

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.offset = Vector(0, 0)



    def check_collision(self):
        bird = self.root.ids.bird

        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True

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
        #self.root.ids.background.scroll_textures(time_passed)
        self.ship_moveme()

        self.npc_test.move_me(self.offset)
        #print(self.npc_test.pos, self.npc_test.original_pos)
        #print(Vector(self.root.ids.ship.pos).distance(Vector(self.npc_test.pos)),self.offset)


        for p in self.root.ids.ship.projectile_list:
            p.move_me()

            if p.collide_widget(self.npc_test):
                print("au au au")

            if p.collide_widget(self.root.ids.ship):

                with self.root.ids.background.canvas:
                    Color(1, 0, 0, 1, mode='rgba')


            with self.root.ids.background.canvas:
                Color(1, 0, 0, 1, mode='rgba')
                Line(pos=self.root.ids.ship.p1, points=(self.root.ids.ship.p1,self.root.ids.ship.p2,self.root.ids.ship.p3,self.root.ids.ship.p4,self.root.ids.ship.p1), width=1)

                Rectangle(pos=self.root.ids.ship.pos, size=self.root.ids.ship.size)


            self.root.ids.background.canvas.ask_update()








    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        self.npc_test = Ship2((Window.width * 1, Window.height * 0.5),6)
        self.root.add_widget(self.npc_test)

        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

        Clock.schedule_interval(self.root.ids.background.change_bg_on_time, 1)



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




    def move_pipes(self, time_passed):

        for pipe in self.pipes:
            pipe.x -= time_passed * 100


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
            if ship.center_y < Window.height:
                ship.center_y += 1
            else:
                self.root.ids.background.scroll_bg((0, -1))
                self.offset.y += 1

        elif ship.move_down_boolean:
            if ship.center_y > 0:
                ship.center_y -= 1
            else:
                self.root.ids.background.scroll_bg((0, 1))
                self.offset.y -= 1

        if ship.move_left_boolean:
            if ship.center_x > 0:
                ship.center_x -= 1
            else:
                self.root.ids.background.scroll_bg((1, 0))
                self.offset.x -= 1

        elif ship.move_right_boolean:
            if ship.center_x < Window.width:
                ship.center_x += 1
            else:
                self.root.ids.background.scroll_bg((-1, 0))
                self.offset.x += 1




if __name__ == '__main__':
    MainApp().run()


MainApp().run()



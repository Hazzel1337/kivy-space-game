import shapely
from kivy.app import App
from kivy.graphics.context_instructions import Scale, Translate, Color, PushMatrix, Rotate, PopMatrix
from kivy.graphics.fbo import Fbo
from kivy.graphics.gl_instructions import ClearColor, ClearBuffers
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
    # btn1 = Button(text="1")
    # btn2 = Button(text="2")
    #
    # btn3 = Button(text="3")
    # btn4 = Button(text="4")
    # btn5 = Button(text="5")
    # btn6 = Button(text="6")
    # btn7 = Button(text="7")
    # btn8 = Button(text="8")
    # btn9 = Button(text="9")

    def __init__(self, **kwargs):
        super(arrow, self).__init__(**kwargs)


        #btn_l = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9]



        # for i in btn_l:
        #     arrow.add_widget(self, i)
        #for i in range(9):
        #    btn = Button(text=str(i))
        #    arrow.add_widget(self, widget=btn)

    # def move_up(self, root):
    #     print("meow")
    #
    def move_down(self):
        print(MainApp.ids.ship.pos)

    #btn2.bind(on_press=move_down)
    #
    # def move_right(self):
    #     self.center_x += 1
    #
    # def move_left(self):
    #     self.center_x -= 1



class Projectile(Rectangle):

    proj = Image(source="Shot1/shot1_1.png").texture

    max_travel_distance = 100
    already_travled = Vector(0, 0)

    def __init__(self, target_pos, **kwargs):
        super(Projectile, self).__init__(**kwargs)
        self.target_pos = target_pos
        self.calc_move_me()


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


class Projectile2(Scatter):

    def __init__(self, pic ,**kwargs):
        super(Projectile2, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = pic.size
        print(pic.size)
        self.add_widget(pic)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False

        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])


        # with self.canvas:
        #     svg = Projectile2(pic)
        # self.size = svg.width, svg.height

    def update_hitbox(self):
        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])

    def get_widget_pixel_color(self, x_pos, y_pos):

        self.size = (Window.size[0] - self.x, Window.size[1] - self.y)

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=self.size, with_stencilbuffer=True)

        with fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()

        x_pos = int(x_pos)
        y_pos = int(y_pos)

        color = fbo.get_pixel_color(x_pos - self.x, self.height - y_pos + self.y)

        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        # ======fixed but WTH?

        if x_pos - self.x < 0:
            # print color
            color = [0, 0, 0, 0]
        # ====================

        return color

    def my_collide_point(self, x_pos, y_pos):

        color = self.get_widget_pixel_color(x_pos, y_pos)
        alpha = color[-1]
        print(color)

        if alpha > 0:
            return True
        return False

    def on_touch_down(self, touch):

        print(self.my_collide_point(*touch.pos))
        return super(Projectile2, self).on_touch_down(touch)




# class Projectile2(Rotabox):
#
#
#     def __init__(self, pic, **kwargs):
#         super(Projectile2, self).__init__(**kwargs)
#         self.add_widget(pic)



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


        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

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

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def draw_projectiles(self):
        pass


        # for p in self.parent.ids["ship"].projectile_list:
        #     self.parent.add_widget(p)


            # with self.canvas.before:
            #     self.canvas.add(p)


        #self.canvas.ask_update()



class Bird(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)



# class Ship(Image):
#     velocity = NumericProperty(0)
#     acceleration = NumericProperty(5)
#     waypoint = (0, 0)
#     travelvec = (0, 0)
#     traveled_already = Vector(0, 0)
#     up = NumericProperty(1)
#     #movement
#     move_up_boolean = False
#     move_down_boolean = False
#     move_left_boolean = False
#     move_right_boolean = False
#     #projectiles
#     projectile_list =[]
#
#
#
#
#     def __init__(self, **kwargs):
#         super(Ship, self).__init__(**kwargs)
#
#         self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
#         self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
#         self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
#         self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
#         self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])
#
#         self.source = "Ship1.png"
#         self.size_hint = (None, None)
#         self.size = (64, 64)
#         self.pos = self.center
#
#
#         #self.hitbox = sympy.Polygon(self.p1, self.p2, self.p3, self.p4)
#
#
#     def update_hitbox(self):
#         self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
#         self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
#         self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
#         self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
#         self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])
#         self.hitbox = shapely.affinity.rotate(self.hitbox, angle=90)
#
#     def rotate(self):
#         #kivy part
#         with self.canvas.before:
#             PushMatrix()
#             Rotate(origin=self.center, angle=90)
#
#         with self.canvas.after:
#             PopMatrix()
#
#             #self.pos = self.rect_pos
#             #self.size = self.rect_size
#         #shapley
#         self.hitbox = shapely.affinity.rotate(self.hitbox, angle=90)
#         print(self.children)
#
#
#     def on_touch_down(self, touch):
#
#
#         #new pos
#
#         # self.traveled_already = Vector(0, 0)
#         # fuss = Vector(self.pos)
#         #
#         # #to get the middle of the ship, instead of topleft/topright
#         # fuss.x = fuss.x + self.size[0] * 0.5
#         # fuss.y = fuss.y + self.size[1] * 0.5
#         #
#         # spitze = Vector(touch.pos)
#         # self.waypoint = spitze
#         # self.travel_vec = spitze - fuss
#
#
#         #prints the distance
#         #move_me = Vector(Vector(self.pos).distance(touch.pos)).normalize()
#
#         #projectile
#         #self.projectile_list.append(Projectile(touch.pos, pos=self.pos, size=(32, 32), texture=Projectile.proj))
#         if len(self.projectile_list) < 1:
#             self.projectile_list.append(Projectile2(Image(source="Ship1.png", size=(64, 64)), pos=touch.pos))
#             self.parent.add_widget(self.projectile_list[-1])
#
#
#
#         self.source = "Ship1.png"
#         self.velocity = 150
#         super().on_touch_down(touch)
#
#     def on_touch_up(self, touch):
#         self.source = "Ship1.png"
#         super().on_touch_up(touch)
#
#     def move_up(self, widget):
#         if widget.state == "down":
#             self.move_up_boolean = True
#         else:
#             self.move_up_boolean = False
#
#
#     def move_down(self, widget):
#         if widget.state == "down":
#             self.move_down_boolean = True
#         else:
#             self.move_down_boolean = False
#
#
#     def move_left(self, widget):
#         if widget.state == "down":
#             self.move_left_boolean = True
#
#         else:
#             self.move_left_boolean = False
#
#
#     def move_right(self, widget):
#         if widget.state == "down":
#             self.move_right_boolean = True
#
#         else:
#             self.move_right_boolean = False
#
#     def move_topleft(self, widget):
#         if widget.state == "down":
#             self.move_left_boolean = True
#             self.move_up_boolean = True
#
#         else:
#             self.move_left_boolean = False
#             self.move_up_boolean = False
#
#     def move_downleft(self, widget):
#         if widget.state == "down":
#             self.move_left_boolean = True
#             self.move_down_boolean = True
#
#         else:
#             self.move_left_boolean = False
#             self.move_down_boolean = False
#
#     def move_topright(self,widget):
#         if widget.state == "down":
#             self.move_right_boolean = True
#             self.move_up_boolean = True
#
#         else:
#             self.move_right_boolean = False
#             self.move_up_boolean = False
#
#     def move_downright(self,widget):
#         if widget.state == "down":
#             self.move_right_boolean = True
#             self.move_down_boolean = True
#
#         else:
#             self.move_right_boolean = False
#             self.move_down_boolean = False


        #self.projectile_list.append(Projectile(pos=self.pos, size=(32, 32), texture=Projectile.proj, target_pos=))

        #for p in self.projectile_list:
        #
        # with self.parent.ids["background"].canvas.before:
        #     self.parent.ids["background"].canvas.add(Projectile(pos=self.pos, size=(32, 32), texture=Projectile.proj))


class Ship(Scatter):
    velocity = NumericProperty(0)
    acceleration = NumericProperty(5)
    waypoint = (0, 0)
    travelvec = (0, 0)
    traveled_already = Vector(0, 0)
    up = NumericProperty(1)
    # movement
    move_up_boolean = False
    move_down_boolean = False
    move_left_boolean = False
    move_right_boolean = False
    # projectiles
    projectile_list = []

    def __init__(self, **kwargs):
        super(Ship, self).__init__(**kwargs)
        pic = Image(source="Ship1.png")
        self.size_hint = (None, None)
        self.size = pic.size
        print(pic.size)
        self.add_widget(pic)
        self.do_rotation = False
        self.do_scale = False
        self.do_translation = False
        self.children[0].pos = self.pos




        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])


        # with self.canvas:
        #     svg = Projectile2(pic)
        # self.size = svg.width, svg.height

    def update_hitbox(self):
        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])

    def get_widget_pixel_color(self, x_pos, y_pos):

        self.size = (Window.size[0] - self.x, Window.size[1] - self.y)

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=self.size, with_stencilbuffer=True)

        with fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()

        x_pos = int(x_pos)
        y_pos = int(y_pos)

        color = fbo.get_pixel_color(x_pos - self.x, self.height - y_pos + self.y)

        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        # ======fixed but WTH?

        if x_pos - self.x < 0:
            # print color
            color = [0, 0, 0, 0]
        # ====================

        return color

    def my_collide_point(self, x_pos, y_pos):

        color = self.get_widget_pixel_color(x_pos, y_pos)
        alpha = color[-1]
        print(color)

        if alpha > 0:
            return True
        return False

    def on_touch_down(self, touch):

        print(self.my_collide_point(*touch.pos))
        return super(Ship, self).on_touch_down(touch)

    def update_hitbox(self):
        self.p1 = (self.pos[0] + 2, self.pos[1] + 16)
        self.p2 = (self.pos[0] + 60, self.pos[1] + 16)
        self.p3 = (self.pos[0] + 60, self.pos[1] + 44)
        self.p4 = (self.pos[0] + 2, self.pos[1] + 44)
        self.hitbox = Polygon([self.p1, self.p2, self.p3, self.p4])
        self.hitbox = shapely.affinity.rotate(self.hitbox, angle=90)
        self.children[0].pos = self.center

    def rotate(self):
        #kivy part
        with self.canvas.before:
            PushMatrix()
            Rotate(origin=self.center, angle=90)

        with self.canvas.after:
            PopMatrix()

        self.canvas.ask_update()


        #shapley
        self.hitbox = shapely.affinity.rotate(self.hitbox, angle=90)
        print(self.children)


    def on_touch_down(self, touch):


        #new pos

        # self.traveled_already = Vector(0, 0)
        # fuss = Vector(self.pos)
        #
        # #to get the middle of the ship, instead of topleft/topright
        # fuss.x = fuss.x + self.size[0] * 0.5
        # fuss.y = fuss.y + self.size[1] * 0.5
        #
        # spitze = Vector(touch.pos)
        # self.waypoint = spitze
        # self.travel_vec = spitze - fuss


        #prints the distance
        #move_me = Vector(Vector(self.pos).distance(touch.pos)).normalize()

        #projectile
        #self.projectile_list.append(Projectile(touch.pos, pos=self.pos, size=(32, 32), texture=Projectile.proj))
        if len(self.projectile_list) < 1:
            self.projectile_list.append(Projectile2(Image(source="Ship1.png", size=(64, 64)), pos=touch.pos))
            self.parent.add_widget(self.projectile_list[-1])



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
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True


def compute_offset(obj1, obj2):
    # obj 2 is scrolling player
    offset_x = obj2.pos[0] - obj1.pos[0]
    offset_y = obj2.pos[1] - obj1.pos[1]
    return (offset_x, offset_y)







# def overlap2(rect1, rect2):
#     rect1 = np.array([rect1.size[0], rect1.size[1], rect1.size[0]+rect1.size[0], rect1.size[0]+rect1.size[0]])
#     rect2 = np.array([rect2.size[0], rect2.size[1], rect2.size[0]+rect2.size[0], rect2.size[0]+rect2.size[0]])
#
#     p1 = Polygon([(rect1[0], rect1[1]), (rect1[1], rect1[1]), (rect1[2], rect1[3]), (rect1[2], rect1[1])])
#     p2 = Polygon([(rect2[0], rect2[1]), (rect2[1], rect2[1]), (rect2[2], rect2[3]), (rect2[2], rect2[1])])
#     p1.intersection(p2)
#     return p1.intersects(p2), p1.intersection(p2)


class MainApp(App):
    pipes = []
    GRAVITY = 300
    was_colliding = False

    #keyboard
    #key_board =



    def move_bird(self, time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        #self.check_collision()

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
        self.move_bird(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_textures(time_passed)
        self.ship_moveme()
        #self.move_p()
        self.root.ids.ship.size = ("64dp","64dp")
        self.root.ids.ship.update_hitbox()
        for p in self.root.ids.ship.projectile_list:
            #print(p.collide_widget(self.root.ids.ship))
            p.update_hitbox()
            if p.collide_widget(self.root.ids.ship):
                #print(Intersection(p.hitbox, self.root.ids.ship.hitbox ))
                #overlup = overlap2(self.root.ids.ship, p)
                #overlup2 = list(overlup[1].bounds)
                #print(overlup[0], list(overlup[1].exterior.coords))
                print(p.hitbox.intersects(self.root.ids.ship.hitbox))
                with self.root.ids.background.canvas:
                    Color(1, 0, 0, 1, mode='rgba')
                    #Line(pos=self.root.ids.ship.pos, points=list(overlup[1].exterior.coords), width=1)
                    #Rectangle(pos=(self.root.ids.ship.pos[0] - overlup2[0], self.root.ids.ship.pos[1] - overlup2[1]), size=(overlup2[2] - overlup2[0],overlup2[3]- overlup2[1]))

                pass

            #p.size = (64, 64)



            offset = compute_offset(p, self.root.ids.ship)
            offset2 = compute_offset(self.root.ids.ship, p)

            point_to_check = (p.pos[0] + p.size[0] + offset[0],

            p.pos[1] + p.size[1] + offset[1]) #+ self.root.ids.ship.size[1]

            point_to_check2 = (self.root.ids.ship.pos[0]   + offset2[0],

                              self.root.ids.ship.pos[1]   + offset2[1])

            #print(self.root.ids.ship.size, offset, point_to_check)
            #overlup = overlap2(self.root.ids.ship, p)
            #print(overlup[0], overlup[1])
            #self.root.ids.background.canvas.clear()

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


        print(self.root.walk)
        print(self.root.ids)

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

    def move_p(self):
        player = self.root.ids.ship

        for p in player.projectile_list:
            p.move_me()













# if __name__ == '__main__':
#     from kivy.base import runTouchApp
#     runTouchApp(MyKeyboardListener())

MainApp().run()



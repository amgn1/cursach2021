import os, math

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches
    import matplotlib.path
    from kivy.core.window import Window
    Window.size = (1280, 720)
    Window.minimum_width, Window.minimum_height = Window.size
    import kivy
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    from kivy.uix.widget import Widget
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button

    
except ImportError:
    os.system("pip install matplotlib")
    os.system("pip install numpy")
    os.system("pip install kivy")
    os.system("pip install kivy_garden")
    python_path = '\\'.join(os.path.dirname(kivy.__file__).split('\\')[:-2])
    os.system(f"{python_path}\Scripts\garden install matplotlib")
    
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches
    import matplotlib.path
    from kivy.core.window import Window
    Window.size = (1280, 720)
    Window.minimum_width, Window.minimum_height = Window.size
    import kivy
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    from kivy.uix.widget import Widget
    from kivy.uix.textinput import TextInput

class Line():
    def __init__(self, x1, y1, x2, y2):
        if x2 < x1:
            self._x1 = x2
            self._y1 = y2
            self._x2 = x1
            self._y2 = y1
        else:
            self._x1 = x1
            self._y1 = y1
            self._x2 = x2
            self._y2 = y2

        self.xi = 0.0
        self.yi = 0.0
        self.xj = 0.0
        self.yj = 0.0
        self.xs = 0.0
        self.ys = 0.0

    def get_A(self):
        if abs(self._y2 - self._y1) < 0.000001:
            return 0
        return self._y2 - self._y1

    def get_B(self):
        if abs(self._x1 - self._x2) < 0.000001:
            return 0
        return self._x1 - self._x2

    def get_C(self):
        if abs(self._x2 * self._y1 - self._x1 * self._y2) < 0.000001:
            return 0
        return self._x2 * self._y1 - self._x1 * self._y2

    def show(self):
        x = [self._x1, self._x2]
        y = [self._y1, self._y2]
        plt.plot(x, y, color = "#00eeff")

    def angle(self):
        if abs(self._x2 - self._x1) > 0.000001:
            return math.atan(abs(self._y2 - self._y1) / abs(self._x2 - self._x1))
        else:
            return math.pi / 2

    def check_a(self):
        if abs(self._y2 - self._y1) < 0.000001:
            return "a"
        elif abs(self._x2 - self._x1) < 0.000001:
            return "b"
        elif (self._y2 - self._y1) / (self._x2 - self._x1) > 0:
            return "c"
        else:
            return "d"

    def check_ins(self, circle):
        if (
            (
                self.check_a() == "c"
                and (
                    self._x1 <= circle.xi <= self._x2
                    and self._y1 <= circle.yi <= self._y2
                    or self._x1 <= circle.xj <= self._x2
                    and self._y1 <= circle.yj <= self._y2
                )
            )
            or (
                self.check_a() == "d"
                and (
                    self._x1 <= circle.xi <= self._x2
                    and self._y2 <= circle.yi <= self._y1
                    or self._x1 <= circle.xj <= self._x2
                    and self._y2 <= circle.yj <= self._y1
                )
            )
            or (
                self.check_a() == "b"
                and (
                    min(self._y1, self._y2) <= circle.yi <= max(self._y1, self._y2)
                    or min(self._y1, self._y2) <= circle.yj <= max(self._y1, self._y2)
                )
            )
            or self.check_a == "a"
            and (
                min(self._x1, self._x2) <= circle.xj <= max(self._x1, self._x2)
                or min(self._x1, self._x2) <= circle.xi <= max(self._x1, self._x2)
            )
        ):
            return 1
        else:
            return 0

class Circle():
    def __init__(self, x=0.0, y=0.0, r=0.0):
        self._x = x
        self._y = y
        self._r = r

    def show(self):
        axes = plt.gca()
        axes.set_aspect("equal")
        cc = matplotlib.patches.Circle((self._x, self._y), self._r, fill=0, color = '#ff00e6')
        axes.add_patch(cc)

    def dist(self, line):
        a = line.get_A()
        b = line.get_B()
        c = line.get_C()

        if a == 0:
            return abs(self._y + c / b)
        elif b == 0:
            return abs(self._x + c / a)
        return abs(a * self._x + b * self._y + c) / ((a ** 2 + b ** 2) ** (1 / 2))

    def intersect(self, line):
        A = line.get_A()
        B = line.get_B()
        C = line.get_C()
        l = (self._r ** 2 - self.dist(line) ** 2) ** (1 / 2)

        if A == 0:
            if C:
                self.ys = -(B / C)
            else:
                self.ys = 0.0

            self.xs = self._x
            self.xi = self._x - l
            self.yi = self.ys
            self.xj = self._x + l
            self.yj = self.ys

        elif B == 0:
            self.ys = self._y
            if C:
                self.xs = -(A / C)
            else:
                self.xs = 0.0

            self.xi = self.xs
            self.yi = self._y - l
            self.xj = self.xs
            self.yj = self._y + l

        else:
            a = line.angle()
            lx = l * math.cos(a)
            ly = l * math.sin(a)
            self.ys = (B * C + A * B * self._x - A ** 2 * self._y) / (
                -(A ** 2) - B ** 2
            )
            self.xs = -(B * self.ys + C) / A

        if line.check_a() == "c":
            self.xi = self.xs - lx
            self.yi = self.ys - ly
            self.xj = self.xs + lx
            self.yj = self.ys + ly

        elif line.check_a() == "d":
            self.xi = self.xs - lx
            self.yi = self.ys + ly
            self.xj = self.xs + lx
            self.yj = self.ys - ly

        if line.check_ins(self):
            return 1
        else:
            return 0

    def check(self, line):
        if self.dist(line) > self._r or not self.intersect(line):
            return 0
        else:
            return 1

class Polygon():
    def __init__(self, P):
        self._P = P
        self._L = []

        l = len(self._P)
        for i in range(l):
            if i + 1 < l:
                self._L.append(
                    Line(
                        self._P[i][0],
                        self._P[i][1],
                        self._P[i + 1][0],
                        self._P[i + 1][1],
                    )
                )
            else:
                self._L.append(
                    Line(self._P[i][0], self._P[i][1], self._P[0][0], self._P[0][1])
                )

    def check(self, circle):
        for i in self._L:
            if circle.check(i):
                return 1
        return 0

    def show(self):
        for i in self._L:
            i.show()
    
    def is_convex(self):
        two_pi = 2 * math.pi
        try: 
            if len(self._P) < 3:
                return 0
            x0, y0 = self._P[-2]
            x1, y1 = self._P[-1]
            direct1 = math.atan2(y1 - y0, x1 - x0)
            angle_sum = 0.0

            for ndx, newpoint in enumerate(self._P):
                x0, y0, direct0 = x1, y1, direct1
                x1, y1 = newpoint
                direct1 = math.atan2(y1 - y0, x1 - x0)

                if x0 == x1 and y0 == y1:
                    return 0

                angle = direct1 - direct0

                if angle <= -math.pi:
                    angle += two_pi  
                elif angle > math.pi:
                    angle -= two_pi
                if ndx == 0:  
                    if angle == 0.0:
                        return 0
                    orientation = 1.0 if angle > 0.0 else -1.0
                else:
                    if orientation * angle <= 0.0:
                        return 0

                angle_sum += angle
            return abs(round(angle_sum / two_pi)) == 1
        except (ArithmeticError, TypeError, ValueError):
            return 0   
        

class Render(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.amount = 0
        self.count = 0
        self.polygon_points = []
        self.polygon = None

        x = [0, 0]
        y = [0, 0]
        plt.plot(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')

        graph = FigureCanvasKivyAgg(plt.gcf())
        self.ids['graph'] = graph
        self.ids.box.add_widget(graph)
    
    def press(self, *args):
        try:
            if self.count == 0:
                self.amount = int(self.ids.x.text)

                if self.amount < 3:
                    self.ids.stat.text = '[color=#db1304]Status: Error\nShape is not polygon[/color]'
                    self.count = 0
                    return 0
                else:
                    textinput = TextInput(multiline = False, font_size = 24, padding = 10)
                    self.ids['y'] = textinput
                    self.ids.input_box.add_widget(textinput)

                    self.ids.mainlabel.text = '[font=Roboto][b]Enter point (1) [x, y][b][/font]'
                    self.ids.x.text = ''
                    self.ids.stat.text = 'Status: Waiting for data'

            elif self.count < self.amount:
                temp = [float(self.ids.x.text), float(self.ids.y.text)]
                self.polygon_points.append(temp)
                self.ids.mainlabel.text = f'[font=Roboto][b]Enter point ({len(self.polygon_points) + 1}) [x, y][b][/font]'
                self.ids.x.text = ''
                self.ids.y.text = ''
                self.ids.stat.text = 'Status: Waiting for data'

            elif self.count == self.amount:
                temp = [float(self.ids.x.text), float(self.ids.y.text)]
                self.polygon_points.append(temp)
                self.polygon = Polygon(self.polygon_points)

                if self.polygon.is_convex():
                    self.ids.mainlabel.text = f'[font=Roboto][b]Enter circle coords and rad[b][/font]'
                    textinput = TextInput(multiline = False, font_size = 24, padding = 10)
                    self.ids['r'] = textinput
                    self.ids.input_box.add_widget(textinput)
                    self.ids.x.text = ''
                    self.ids.y.text = ''
                    self.ids.stat.text = 'Status: Waiting for data'
                else:
                    self.reset()
                    self.ids.stat.text = '[color=#db1304]Status: Polygon is not convex, try again[/color]'
                    return 0

            elif self.count - 1 == self.amount:
                x0 = float(self.ids.x.text)
                y0 = float(self.ids.y.text)
                r = float(self.ids.r.text)

                circle = Circle(x0, y0, r)

                self.update_graph(self.polygon, circle)

                self.ids.secbox.remove_widget(self.ids.button)
                btn = Button(text='Reset', font_size=24, size_hint=(1, 0.2))
                btn.fbind('on_press', self.reset)
                self.ids['button'] = btn
                self.ids.secbox.add_widget(btn)


                if self.polygon.is_convex():
                    if self.polygon.check(circle) == 1:
                        self.ids.stat.text = 'Status: Found intersection'
                    else:
                        self.ids.stat.text = 'Status: Found no intersections'
                else:
                    self.ids.stat.text = '[color=#db1304]Status: Polygon is not convex, try again[/color]'
            
            self.count += 1
        except ValueError: 
                self.ids.stat.text = '[color=#db1304]Status: Error\nTry using numbers[/color]'

    def update_graph(self, polygon, circle):
        self.ids.box.remove_widget(self.ids.graph)
        plt.cla()
        plt.clf()

        polygon.show()
        circle.show()

        plt.xlabel('X')
        plt.ylabel('Y')

        graph = FigureCanvasKivyAgg(plt.gcf())
        self.ids['graph'] = graph
        self.ids.box.add_widget(graph)

    def reset(self, *args, **kwargs):
        try:
            self.ids.input_box.remove_widget(self.ids.y)
            self.ids.input_box.remove_widget(self.ids.r)
        except AttributeError:
            self.ids.input_box.remove_widget(self.ids.y)
        finally:
            self.ids.mainlabel.text = '[font=Roboto][b]Enter points amount[b][/font]'

            self.ids.secbox.remove_widget(self.ids.button)
            btn = Button(text='Submit', font_size=24, size_hint=(1, 0.2))
            btn.fbind('on_press', self.press)
            self.ids['button'] = btn
            self.ids.secbox.add_widget(btn)

            self.ids.x.text = ''
            self.ids.stat.text = 'Status: Waiting for data'
            self.ids.box.remove_widget(self.ids.graph)
            plt.cla()
            plt.clf()

            x = [0, 0]
            y = [0, 0]
            plt.plot(x, y)
            plt.xlabel('X')
            plt.ylabel('Y')

            graph = FigureCanvasKivyAgg(plt.gcf())
            self.ids['graph'] = graph
            self.ids.box.add_widget(graph)

            self.polygon_points = []
            self.count = 0


class MainApp(App):
    def build(self):
        self.title = 'v0.5'
        Builder.load_file('ui.kv')
        return Render()

if __name__ == '__main__':
    MainApp().run()
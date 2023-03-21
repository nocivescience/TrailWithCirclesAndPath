from manim import *
class ThridIntent2(Scene):
    my_config={
        'radios':[2/2**(i) for i in range(7)],
        'circle_kwargs':{
            'stroke_width':2,
            'stroke_color':YELLOW
        }
    }
    def construct(self):
        my_circles=VGroup(*[Circle(radius=radio,**self.my_config['circle_kwargs'])\
            for radio in self.my_config['radios']])
        self.get_sortment(my_circles)
        for my_circle in my_circles:
            my_circle.copy=my_circle.copy()
        alpha=ValueTracker(0)
        my_freqs=list(map(lambda t: 2/t,self.my_config['radios']))
        def get_update_circle(sub_circles):
            for daughter_circle,mother_circle,my_freq in zip(sub_circles[1:],sub_circles[:-1],my_freqs[1:]):
                daughter_circle.become(daughter_circle.copy)
                daughter_circle.move_to(mother_circle.points[0])           
                daughter_circle.rotate(
                    my_freq*alpha.get_value()*TAU,about_point=mother_circle.get_center()
                )
        my_dot=self.get_dot(my_circles[-1])
        my_path=self.my_path(my_dot)
        my_circles.add_updater(get_update_circle)
        self.play(Create(my_circles))
        self.play(Create(my_dot))
        self.add(my_path)
        self.play(alpha.animate.set_value(1),rate_func=smooth,run_time=30)
        self.wait()
    def get_circle(self,radio):
        circle=Circle(radius=radio)
        return circle
    def get_sortment(self,circles):
        circles[0].move_to(3*LEFT)
        for i in range(len(circles)):
            if i == len(circles)-1: #porque aca toma el limite superior inclusive
                break
            circles[i+1].move_to(circles[i].points[0])
    def get_dot(self,circle):
        dot=Dot(radius=0.02,color=RED)
        dot.move_to(circle.points[0])
        dot.add_updater(lambda t: t.move_to(circle.points[0]))
        return dot
    def my_path(self,dot):
        path=VMobject(stroke_width=self.my_config['circle_kwargs']['stroke_width'])
        path.set_points_as_corners([dot.get_center(),dot.get_center()+LEFT*0.001])
        def my_path_update(my_path):
            my_path.append_vectorized_mobject(
                Line(my_path.points[-1],dot.get_center())
            )
            my_path.make_smooth()
        path.add_updater(my_path_update)
        return path
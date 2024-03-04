from hollarek.logging import add_color, Color

abc = add_color(msg='hi', color=Color.RED)
d = ' there'
e =  add_color(msg=' my dude', color=Color.GREEN)
print(abc+d+e)
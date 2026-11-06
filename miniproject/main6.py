import turtle, math

W, H = 167, 385              # room (cm)
WIN_X, WIN_W, WIN_D = 25, 112, 29
OPEN_X, OPEN_W = 55, 112     # whole door opening
RIGHT_SIDE = 4               # right frame side (guess)
LEAF = 100                   # door leaf width (guess)
LEFT_SIDE = OPEN_W - RIGHT_SIDE - LEAF   # left side, longer
DEPTH = 85                   # how deep the open door reaches

def X(x): return x - W/2
def Y(y): return H/2 - y

turtle.setup(W + 200, H + 200)
turtle.tracer(0)
t = turtle.Turtle()
t.hideturtle()
t.speed(0)

def line(x1, y1, x2, y2):
    t.penup(); t.goto(X(x1), Y(y1)); t.pendown(); t.goto(X(x2), Y(y2))

def box(x, y, w, h):
    line(x, y, x + w, y); line(x + w, y, x + w, y + h)
    line(x + w, y + h, x, y + h); line(x, y + h, x, y)

def text(x, y, s, align="center", fs=9):
    t.penup(); t.goto(X(x), Y(y) - 6)
    t.write(s, align=align, font=("Arial", fs, "normal"))

# room
t.pensize(2)
box(0, 0, W, H)

# window
t.pensize(1)
box(WIN_X, -WIN_D, WIN_W, WIN_D)
text(WIN_X + WIN_W/2, -WIN_D/2, "29")
text(WIN_X + WIN_W/2, -WIN_D - 14, "112")
text(WIN_X/2, -12, "25")
text(WIN_X + WIN_W + 16, -12, "32")

# door opening on the bottom wall
hx = OPEN_X + OPEN_W - RIGHT_SIDE        # hinge x
a = math.asin(DEPTH / LEAF)              # open angle
line(OPEN_X, H, OPEN_X + OPEN_W, H)

# swing arc: closed position -> open position
pts = [(hx - LEAF*math.cos(math.radians(d)), H - LEAF*math.sin(math.radians(d)))
       for d in range(0, int(math.degrees(a)) + 1)]
t.penup(); t.goto(X(pts[0][0]), Y(pts[0][1])); t.pendown()
for px, py in pts[1:]:
    t.goto(X(px), Y(py))

# open leaf
ex, ey = hx - LEAF*math.cos(a), H - DEPTH
line(hx, H, ex, ey)

# labels
text(OPEN_X + OPEN_W/2, H + 14, "112")
text(OPEN_X/2, H + 14, "55")
text(OPEN_X + LEFT_SIDE/2, H + 28, str(LEFT_SIDE), fs=8)
text(OPEN_X + LEFT_SIDE + LEAF/2, H + 28, str(LEAF), fs=8)
text(OPEN_X + OPEN_W - RIGHT_SIDE/2, H + 28, str(RIGHT_SIDE), fs=8)
text(ex - 4, H - DEPTH/2, "85", align="right")
text(W/2, H + 46, "167")
text(-22, H/2, "385")

turtle.update()
turtle.done()
from turtle import Turtle, Screen
from time import sleep
from random import randint

WIDTH = 600
HEIGHT = 600

screen = Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("ivory")
screen.title("Snake Game")
screen.tracer(0)

class Food:
	def __init__(self):
		self.food = Turtle('circle')
		self.food.turtlesize(stretch_wid=0.5)
		self.food.color('dark slate blue')
		self.food.penup()
		self.refresh()

	def refresh(self):
		x = randint(-270,270)
		y = randint(-270,270)
		self.food.goto(x, y)

	def get_position(self):
		return self.food.position()

class ScoreBoard():
	align = 'center'
	font = ('Comic Sans Ms', 16, 'normal')
	def __init__(self):
		self.score = 0
		self.score_board = Turtle()
		self.score_board.penup()
		self.score_board.goto(0, 260)
		self.score_board.write(f'Score: {self.score}', align=ScoreBoard.align, font=ScoreBoard.font)
		self.score_board.hideturtle()

	def add_score(self):
		self.score += 1
		self.score_board.clear()
		self.score_board.write(f'Score: {self.score}', align=ScoreBoard.align, font=ScoreBoard.font)

	def game_over(self):
		self.score_board.clear()
		self.score_board.goto(0, 0)
		self.score_board.write('GAME OVER', align=ScoreBoard.align, font=ScoreBoard.font)
		self.score_board.goto(0, -35)
		self.score_board.write(f'Total Score: {self.score}', align=ScoreBoard.align, font=ScoreBoard.font)

class Snake:
	def __init__(self):
		self.body = []
		self.distance = 14
		self.create()

	def create(self):
		starting_positions = [(-self.distance*i,0) for i in range(0, 3)]
		for pos in starting_positions:
			self.add_piece(pos)

	def extend_body(self):
		pos = self.body[-1].position()
		self.add_piece(pos)

	def add_piece(self, pos):
		s = Turtle('square')
		s.turtlesize(stretch_wid=0.6)
		s.color('maroon')
		s.penup()
		s.goto(pos)
		self.body.append(s)

	def move(self):
		for i in range(len(self.body)-1, 0, -1):
			x = self.body[i-1].xcor()
			y = self.body[i-1].ycor()
			self.body[i].goto(x, y)
		self.body[0].forward(self.distance)

	def change_direction(self, heading):
		if abs(int(snake.body[0].heading()) - heading) != 180:
			self.body[0].setheading(heading)

snake = Snake()
food = Food()
score_board = ScoreBoard()

screen.listen()
screen.onkey(lambda: snake.change_direction(90), "Up")
screen.onkey(lambda: snake.change_direction(270), "Down")
screen.onkey(lambda: snake.change_direction(180), "Left")
screen.onkey(lambda: snake.change_direction(0), "Right")

game_over = False

while not game_over:
	screen.update()
	
	# make snake faster
	if len(snake.body) < 15:
		sleep_time = 0.1
	elif len(snake.body) < 22:
		sleep_time = 0.07
	elif len(snake.body) < 30:
		sleep_time = 0.05
	elif len(snake.body) < 35:
		sleep_time = 0.04
	else:
		sleep_time = 0.03

	sleep(sleep_time)
	snake.move()

	# capture food
	if snake.body[0].distance(food.get_position()) < 10:
		food.refresh()
		snake.extend_body()
		score_board.add_score()

	# collusion detection - walls
	boundaries = [WIDTH//2, HEIGHT//2]
	if snake.body[0].xcor() > boundaries[0]-10 or snake.body[0].xcor() < -boundaries[0] or snake.body[0].ycor() > boundaries[1] or snake.body[0].ycor() < -boundaries[1]+10:
		game_over = True
		score_board.game_over()

	# collusion detection - snake body
	for b in snake.body[1:]:
		if snake.body[0].distance(b) < 10:
			game_over = True
			score_board.game_over()

screen.exitonclick()
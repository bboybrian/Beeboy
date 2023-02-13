import random
def get_colour(col):
	r = col >> 16
	g = col & 0xFF00
	g = g >> 8
	b = col & 0xFF
	rgb = [r, g, b]

	diff = random.randint(64, 192)
	choice = random.randint(0,2)

	if rgb[choice] + diff > 255 and rgb[choice]:
		rgb[choice] = max(0, rgb[choice] - diff)
	else:
		rgb[choice] += diff
	
	r = rgb[0]
	g = rgb[1]
	b = rgb[2]
	c = (r << 16) + (g << 8) + b
	print('r:', r, 'g:', g, 'b:', b)
	return c
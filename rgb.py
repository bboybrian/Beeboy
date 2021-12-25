def get_colour(col):
	b = col & 0xFF
	g = col & 0xFF00
	g = g >> 8
	r = col >> 16

	if b == 0 and r > 0:
		if g >= r:
			r -= 8
		else:
			g += 8

	elif g == 0 and b > 0:
		if r >= b:
			b -= 8
		else:
			r += 8

	else:
		if b >= g:
			g -= 8
		else:
			b += 8

	c = (r << 16) + (g << 8) + b
	print('r:', r, 'g:', g, 'b:', b)
	return c
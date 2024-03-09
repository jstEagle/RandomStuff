
#### <u>To solve maximum and minimum problems:</u>
- Write down the equation of the quantity you are asked to find the max/min value of.
- Write down an equation of an "extra" bit of information you are given.
- Rearrange the second equation and substitute into the first, so there is only one variable in the expression to be maximized or minimized. 
- Differentiate and find the stationary point.
- Find the value of the other variable (if necessary) by substitution.
- Check to see if the value(s) is a maximum or minimum using the $2^{nd}$ derivative test.


A Farmer has <mark class="hltr-yellow">300m</mark> of fencing to fence a rectangular paddock for sheep. On one side is a river so he only needs three fences. Find the values of x and y so that the paddock has <mark class="hltr-blue">maximum</mark> area.

$$ P = y + 2x = 300$$
$$ y = 300 -2x$$
Always solve for one variable!

Area = $x*y$
Area = $x(300-2x)$
A = $300x - 2x^2$

$$\frac{dA}{dx} = 300 - 4x$$
$$ 0 = 300 -4x$$
$$ 4x = 300$$
$$x = 75$$
$$\downarrow$$
$$Maximum\ area = 300(75) - 2(75)^2$$
$$ = 11250m^2$$

_______

### Example
![[Pasted image 20230810093917.png]]
The diagram shows a right circular cone with radius 10cm and height 30cm. The cone is initially completely filled with water. Water leaks out of the cone through a small hole at the vertex at a rate of 4cm$^3$s$^{-1}$ 

1) Show that the volume of water in the cone, V cm$^3$, when the height of the water is h cm is given by the formula $V = \frac{\pi h^3}{27}$ 

$$By\ similarity$$
$$ \frac{r}{10} = \frac{h}{30}$$
$$r = \frac{10h}{30}$$
$$r = \frac13h$$
$$\downarrow$$
$$V = \frac13 \pi r^2h$$
$$ = \frac13 \pi (\frac13h)^2 h$$
$$ = \frac{\pi h^3}{27}$$
2) Find the rate of change of h when h = 20

$$ \frac{dV}{dt} = 4cm^3/s$$
$$Find\ \frac{dh}{dt}$$
$$ \frac{dh}{dt} = \frac{dh}{dV} * \frac{dV}{dt}$$
$$ V = \frac{\pi h^3}{27}$$
$$\frac{dV}{dh} = \frac{3\pi}{27}h^2 = \frac{\pi}9 h^2 = \frac{\pi}9(400) = \frac{400\pi}9$$
$$\therefore \frac{dh}{dV} = \frac{9}{400\pi} $$
$$\frac{dh}{dt} = \frac{dh}{dV} * \frac{dV}{dt} = \frac{9}{400\pi} * 4$$
$$ = \frac9{100\pi} $$
______

### Example
A farmer wants to construct 3 pens for his pigs as shown
![[Pasted image 20230810152312.png]]
Each pen has the same width, x. The farmer has 36m of material to make the pens. Find the dimensions of each pen so that the area of each pen is a maximum.

$$ Perimeter = 6x+4y = 36$$
$$ Area = x*y$$
$$\downarrow$$
$$y = \frac{36-6x}{4}$$
$$y = 9-\frac32 x$$
$$\downarrow$$
$$sub\ into\ Area\ equation = x(9-\frac32 x) = 9x-\frac32 x^2$$
$$\frac{dA}{dx} = -3x+9$$
$$\frac{dA}{dx} = 0 = -3x+9$$
$$-9 = -3x$$
$$x = 3$$
$$sub\ into\ Perimeter\ equation = 6(3) + 4y = 36$$
$$  4y = 18$$
$$y = 4.5$$
$$Answer: 3m * 4.5m$$
_______

### Example
The diagram shows a glass window frame consisting of a rectangle of width x m and height y m and equilateral triangle on top of the rectangle. The perimeter of the window is 10m.
![[Pasted image 20230810161914.png]]
1) Show that the height h, of the equilateral triangle is $\frac{\sqrt3}{2}x$
$$h^2 + (\frac{x}2)^2 = x^2$$
$$h^2 = x^2 - \frac{x^2}4$$
$$h = \frac{\sqrt3}2 x$$

2) Show that the area of the window frame, $Am^2$, is given by $A = 5x + \frac{\sqrt3 - 6}{4}x^2$
$$xy + \frac{\sqrt3}2x * \frac{x}2 = A$$
$$x(\frac{10-3x}{2}) + \frac{\sqrt3}{2}x * \frac{x}2 = A$$
$$x(\frac{10-3x}{2}) + \frac{\sqrt3x^2}4 = A$$
$$\frac{10x - 3x^2}2 + \frac{\sqrt3 x^2}4 = A$$
$$\frac{20x - 6x^2}4 + \frac{\sqrt3 x^2}4 = A$$
$$ \frac{(\sqrt3 - 6)x^2 + 20x}4 = A$$
$$\frac{\sqrt3 - 6}4 x^2 + 5x = A$$

3) Given that x can vary. Find the value of x for which A has a stationary value.
$$\frac{\sqrt3 - 6}4 x^2 + 5x = A$$
$$ = \frac14 x^2(\sqrt3 - 6)$$
$$\frac{dA}{dx} = \frac12 x (\sqrt3 - 6)$$
$$\frac{\sqrt3 - 6}2 x + 5 = 0$$
$$x = \frac{-5}{\frac{\sqrt3 - 6}{2}} = 2.34m\ (3sf)$$

4) Determine whether the stationary value is a maximum or a minimum.
$$\frac{d^2A}{dx^2} = \frac {\sqrt3 - 6}2 < 0$$
$$\therefore stationary\ point\ is\ a\ maximum$$
_______

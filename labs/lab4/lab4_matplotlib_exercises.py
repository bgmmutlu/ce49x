import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 100)
y = x**2

plt.plot(x, y)
plt.title('Plot of $y = x^2$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label='sin(x)', linestyle='-', color='blue')
plt.plot(x, y2, label='cos(x)', linestyle='--', color='red')
plt.title('Plot of sin(x) and cos(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
x = np.random.rand(100)
y = np.random.rand(100)
colors = np.random.rand(100)
sizes = 1000 * np.random.rand(100)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='viridis')
plt.title('Random Scatter Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()
x = np.linspace(0, 10, 50)
dy = 0.8
y = np.sin(x) + dy * np.random.randn(50)

plt.errorbar(x, y, yerr=dy, fmt='o', color='black', ecolor='lightgray', elinewidth=3, capsize=0)
plt.title('Errorbar Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X**2 + Y**2)

plt.contourf(X, Y, Z, cmap='viridis')
plt.colorbar()
plt.title('Contour Plot of $z = \sin(x^2 + y^2)$')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
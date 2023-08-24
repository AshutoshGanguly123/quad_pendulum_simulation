import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams
from collections import deque

def derivatives(y, t, L1, L2, L3, L4, m1, m2, m3, m4):
    theta1, omega1, theta2, omega2, theta3, omega3, theta4, omega4 = y
    g = 9.81
    dtheta1_dt = omega1
    domega1_dt = (-g*(2*m1 + m2 + m3 + m4)*np.sin(theta1) - m2*g*np.sin(theta1 - 2*theta2) - 2*np.sin(theta1 - theta2)*m2*(omega2**2*L2 + omega1**2*L1*np.cos(theta1 - theta2)))/(L1*(2*m1 + m2 + m3 + m4 - m2*np.cos(2*theta1 - 2*theta2)))
    dtheta2_dt = omega2
    domega2_dt = (2*np.sin(theta1 - theta2)*(omega1**2*L1*(m1 + m2 + m3 + m4) + g*(m1 + m2 + m3 + m4)*np.cos(theta1) + omega2**2*L2*m2*np.cos(theta1 - theta2)))/(L2*(2*m1 + m2 + m3 + m4 - m2*np.cos(2*theta1 - 2*theta2)))
    dtheta3_dt = omega3
    domega3_dt = (2*np.sin(theta2 - theta3)*(omega2**2*L2*(m2 + m3 + m4) + g*(m2 + m3 + m4)*np.cos(theta2) + omega3**2*L3*m3*np.cos(theta2 - theta3)))/(L3*(2*m2 + m3 + m4 - m3*np.cos(2*theta2 - 2*theta3)))
    dtheta4_dt = omega4
    domega4_dt = (2*np.sin(theta3 - theta4)*(omega3**2*L3*(m3 + m4) + g*(m3 + m4)*np.cos(theta3) + omega4**2*L4*m4*np.cos(theta3 - theta4)))/(L4*(2*m3 + m4 - m4*np.cos(2*theta3 - 2*theta4)))

    return dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt, dtheta3_dt, domega3_dt, dtheta4_dt, domega4_dt

#initial conditions
theta1 = np.radians(60)
theta2 = np.radians(45)
theta3 = np.radians(30)
theta4 = np.radians(0)
omega1 = 0
omega2 = 0
omega3 = 0
omega4 = 0

y0 = [theta1, theta2, omega1, omega2, theta3, theta4, omega3, omega4]

#odient
t = np.linspace(0,5,20)
# parameters for the pendulums
L1 = 0.8  # length of pendulum 1 in meters
L2 = 0.8 # length of pendulum 2 in meters
L3 = 0.8 # length of pendulum 3 in meters
L4 = 0.8 # length of pendulum 4 in meters
m1 = 1  # mass of pendulum 1 in kilograms
m2 = 2  # mass of pendulum 2 in kilograms
m3 = 3  # mass of pendulum 3 in kilograms
m4 = 6  # mass of pendulum 6 in kilograms

# solve the equations of motion
solution = odeint(derivatives, y0, t, args=(L1, L2, L3, L4, m1, m2, m3, m4))
theta1 = solution[:,0]
theta2 = solution[:,2]
theta3 = solution[:,4]
theta4 = solution[:,6]

#x,y coordinates
x1 = L1*np.sin(theta1)
y1 = -L1*np.cos(theta1)
x2 = L1*np.sin(theta1) + L2*np.sin(theta2)
y2 = -(L1*np.cos(theta1) + L2*np.cos(theta2))
x3 = L1*np.sin(theta1) + L2*np.sin(theta2) + L3*np.sin(theta3)
y3 = -(L1*np.cos(theta1) + L2*np.cos(theta2) + L3*np.cos(theta3))
x4 = L1*np.sin(theta1) + L2*np.sin(theta2) + L3*np.sin(theta3) + L4*np.sin(theta4)
y4 = -(L1*np.cos(theta1) + L2*np.cos(theta2) + L3*np.cos(theta3) + L4*np.cos(theta4))

# Create deques for path tracing
path1 = deque(maxlen=10)
path2 = deque(maxlen=10)
path3 = deque(maxlen=8)
path4 = deque(maxlen=2)

#subplot
def init():
    fig, ax = plt.subplots()  # create a figure and a subplot
    ax.set_xlim(-L1 - L2 - L3 - L4, L1 + L2 + L3 + L4)  # set the limits of the x axis
    ax.set_ylim(-0.2, L1 + L2 + L3 + L4)  # set the limits of the y axis
    ax.set_xticks(np.arange(-2, 2, 0.3))  # set the x ticks
    ax.set_yticks(np.arange(-6, 6, 0.3))  # set the y ticks
    ax.grid(True, color='gray', linewidth=0.5)  # add a grid with gray color and thinner lines
    ax.set_facecolor('black')  # set the background color to black
    ax.tick_params(axis='both', colors='white')  # set the color of the tick labels to white
    ax.plot(0, 0, 'ko', markersize = 10, color = 'silver')  # add a black circle at the origin

    # plot the arms of the pendulums with thicker lines and different colors
    line1, = ax.plot([0, x1[0]], [0, y1[0]], color='cyan', lw=2)
    line2, = ax.plot([x1[0], x2[0]], [y1[0], y2[0]], color='yellow', lw=2)
    line3, = ax.plot([x2[0], x3[0]], [y2[0], y3[0]], color='magenta', lw=2)
    line4, = ax.plot([x3[0], x4[0]], [y3[0], y4[0]], color='white', lw=2)

    # Add lines for path tracing
    path_line1, = ax.plot([], [], color='cyan', lw=1)
    path_line2, = ax.plot([], [], color='yellow', lw=1)
    path_line3, = ax.plot([], [], color='magenta', lw=1)
    path_line4, = ax.plot([], [], color='white', lw=1)

    # plot the masses of the pendulums as circles with different colors
    point1, = ax.plot(x1[0], y1[0], 'o', color='cyan')
    point2, = ax.plot(x2[0], y2[0], 'o', color='yellow')
    point3, = ax.plot(x3[0], y3[0], 'o', color='magenta')
    point4, = ax.plot(x4[0], y4[0], 'o', color='white')

    return fig,line1, line2, line3, line4, point1, point2, point3, point4, path_line1, path_line2, path_line3, path_line4

def animate(i):
    line1.set_data([0, x1[i]], [0, y1[i]])
    line2.set_data([x1[i], x2[i]], [y1[i], y2[i]])
    line3.set_data([x2[i], x3[i]], [y2[i], y3[i]])
    line4.set_data([x3[i], x4[i]], [y3[i], y4[i]])
    point1.set_data(x1[i], y1[i])
    point2.set_data(x2[i], y2[i])
    point3.set_data(x3[i], y3[i])
    point4.set_data(x4[i], y4[i])
        # Update path deques
    path1.append((x1[i], y1[i]))
    path2.append((x2[i], y2[i]))
    path3.append((x3[i], y3[i]))
    path4.append((x4[i], y4[i]))

    # Update path lines
    path_line1.set_data(*zip(*path1))
    path_line2.set_data(*zip(*path2))
    path_line3.set_data(*zip(*path3))
    path_line4.set_data(*zip(*path4))
    return line1, line2, line3, line4, point1, point2, point3, point4, path_line1, path_line2, path_line3, path_line4

fig,line1, line2, line3, line4, point1, point2, point3, point4, path_line1,path_line2, path_line3, path_line4 = init() 
ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, interval = 200, blit=True)

ani.save('ml_work/double_pendulum/outputsquad_pendulum123.gif', writer='imagemagick')


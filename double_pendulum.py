import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams


def derivatives(y, t, L1, L2, m1, m2):
    theta1, omega1, theta2, omega2 = y
    g = 9.81
    dtheta1_dt = omega1
    domega1_dt = (-g*(2*m1 + m2)*np.sin(theta1) - m2*g*np.sin(theta1 - 2*theta2) - 2*np.sin(theta1 - theta2)*m2*(omega2**2*L2 + omega1**2*L1*np.cos(theta1 - theta2)))/(L1*(2*m1 + m2 - m2*np.cos(2*theta1 - 2*theta2)))
    dtheta2_dt = omega2
    domega2_dt = (2*np.sin(theta1 - theta2)*(omega1**2*L1*(m1 + m2) + g*(m1 + m2)*np.cos(theta1) + omega2**2*L2*m2*np.cos(theta1 - theta2)))/(L2*(2*m1 + m2 - m2*np.cos(2*theta1 - 2*theta2)))

    return dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt

#initial conditions
theta1 = np.radians(90)
theta2 = np.radians(45)
omega1 = 0
omega2 = 0

y0 = [theta1, theta2, omega1, omega2]

#odient
t = np.linspace(0,5,10*5)
# parameters for the pendulums
L1 = 0.8  # length of pendulum 1 in meters
L2 = 0.8 # length of pendulum 2 in meters
m1 = 2  # mass of pendulum 1 in kilograms
m2 = 1  # mass of pendulum 2 in kilograms

# solve the equations of motion
solution = odeint(derivatives, y0, t, args=(L1, L2, m1, m2))
theta1 = solution[:,0]
theta2 = solution[:,2]

#x,y coordinates
x1 = L1*np.sin(theta1)
y1 = -L1*np.cos(theta1)
x2 = L1*np.sin(theta1) + L2*np.sin(theta2)
y2 = -(L1*np.cos(theta1) + L2*np.cos(theta2))

#subplot
def init():
    fig, ax = plt.subplots()  # create a figure and a subplot
    ax.set_xlim(-L1 - L2, L1 + L2)  # set the limits of the x axis
    ax.set_ylim(-0.2, L1 + L2)  # set the limits of the y axis
    ax.set_xticks(np.arange(-2, 2, 0.3))  # set the x ticks
    ax.set_yticks(np.arange(-2, 2, 0.3))  # set the y ticks
    ax.grid(True, color='gray', linewidth=0.5)  # add a grid with gray color and thinner lines
    ax.set_facecolor('black')  # set the background color to black
    ax.tick_params(axis='both', colors='white')  # set the color of the tick labels to white
    ax.plot(0, 0, 'ko', markersize = 10, color = 'silver')  # add a black circle at the origin

    # plot the arms of the pendulums with thicker lines and different colors
    line1, = ax.plot([0, x1[0]], [0, y1[0]], 'darkblue', linewidth = 2)  # 'darkblue' for the pendulum arm
    line2, = ax.plot([x1[0], x2[0]], [y1[0], y2[0]], 'darkorange', linewidth = 2)  # 'darkorange' for the pendulum arm

    # plot the mass blobs
    blob1, = ax.plot([x1[0]], [y1[0]], 'o', markersize = m1*8 ,color='darkblue')  # 'darkblue' for the blob
    blob2, = ax.plot([x2[0]], [y2[0]], 'o', markersize = m2*10,color='darkorange')  # 'darkorange' for the blob
    #trails
    trail1, = ax.plot([], [], 'c-', linewidth=1)  # cyan trail for bob 1
    trail2, = ax.plot([], [], 'm-', linewidth=1)  # magenta trail for bob 2


    return fig, line1, line2, blob1, blob2, trail1, trail2

def update(frame):
    line1.set_data([0, x1[frame]], [0, y1[frame]])
    line2.set_data([x1[frame], x2[frame]], [y1[frame], y2[frame]])
    blob1.set_data(x1[frame], y1[frame])
    blob2.set_data(x2[frame], y2[frame])
    # update the data for the trails
    # limit the length of the trails
    trail_length = 30  # adjust this to change the length of the trails
    if frame > trail_length:
        trail1.set_data(x1[frame-trail_length:frame], y1[frame-trail_length:frame])
        trail2.set_data(x2[frame-trail_length:frame], y2[frame-trail_length:frame])
    else:
        trail1.set_data(x1[:frame], y1[:frame])
        trail2.set_data(x2[:frame], y2[:frame])

    return line1, line2, blob1, blob2, trail1, trail2

fig, line1, line2, blob1, blob2, trail1, trail2 = init()
animation = FuncAnimation(fig, update, frames=np.arange(len(t)), init_func=init, interval=200, blit=True)
animation.save('ml_work/double_pendulum/outputsdouble_pendulum1323.gif', writer='imagemagick')









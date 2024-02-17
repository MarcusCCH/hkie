# from pyPS4Controller.controller import Controller


# class MyController(Controller):

#     def __init__(self, **kwargs):
#         Controller.__init__(self, **kwargs)

#     def on_x_press(self):
#        print("Hello world")

#     def on_x_release(self):
#        print("Goodbye world")

# controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# # you can start listening before controller is paired, as long as you pair it within the timeout window
# controller.listen(timeout=60)
import pygame

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check and initialize the PS4 controller
if pygame.joystick.get_count() == 0:
    print("No controller found")
    pygame.quit()
    quit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print("hi")
# Main loop
running = True


def axis_parser(axis_dict):
    """
    Returns a dict with the names of the axes as keys and the values scaled properly.
    """
    name_dict = {}
    for key in axis_dict.keys():
        if key == 0:
            name_dict["LEFT_STICK_X"] = int(axis_dict[key] * 127)
        if key == 1:
            name_dict["LEFT_STICK_Y"] = int(axis_dict[key] * 127)
        if key == 3:
            name_dict["RIGHT_STICK_X"] = int(axis_dict[key] * 127)
        if key == 4:
            name_dict["RIGHT_STICK_Y"] = int(axis_dict[key] * 127)
    return name_dict


while running:
    # # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # # Get controller input
    axes = joystick.get_numaxes()
    for i in range(axes):
        axis = joystick.get_axis(i)
        print(f"Axis {i}: {axis}")

    # buttons = joystick.get_numbuttons()
    # for i in range(buttons):
    #     button = joystick.get_button(i)
    #     print(f"Button {i}: {button}")

    # hats = joystick.get_numhats()
    # for i in range(hats):
    #     hat = joystick.get_hat(i)
    #     print(f"Hat {i}: {hat}")

# Clean up
pygame.quit()

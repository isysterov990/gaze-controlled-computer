import os
import sys
from tkinter import *

from gui.calibration import get_gaze_point
from gui.tracker import track_eyes

script_dir = sys.path[0]
main_menu = Tk()

circle_radius = 50
circle_positions = [(100, 100), (1720, 100), (1720, 880), (100, 880)]


# circle_positions = [(100, 100)]
def open_calibration_window():
    calibration_points = []
    calibration_window = Toplevel(main_menu)
    calibration_window.geometry('1920x1080')
    calibration_window.attributes('-fullscreen', True)
    # Load the calibration button and instruction images
    calibration_button = PhotoImage(file=os.path.join(script_dir, "./images/calibration_button.png"))
    calibration_instructions = PhotoImage(file=os.path.join(script_dir, "./images/calibration_instruction.png"))

    def changeText():
        button_1.config(image=calibration_instructions, command=calibrate)

    cal_canvas = Canvas(
        calibration_window,
        bg="#565656",
        height=1080,
        width=1920
    )

    cal_canvas.pack(fill="both", expand=True)
    cal_canvas.place(x=-2, y=-2)
    # Add the calibration button to the canvas
    button_1 = Button(
        master=calibration_window,
        image=calibration_button,
        borderwidth=0,
        command=changeText,
        highlightthickness=0,
        relief="flat"
    )
    button_1.place(
        x=631.0,
        y=396.0,
        width=657.0,
        height=288.0
    )

    def calibrate():
        # Collect calibration points for each circle
        for circle_position in circle_positions:
            # Draw the circle on the canvas
            cal_canvas.create_oval(circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                                   circle_position[0] + circle_radius, circle_position[1] + circle_radius,
                                   outline="#ffffff", width=2)
            calibration_window.update_idletasks()
            calibration_window.update()
            # Remove the circle from the canvas
            cal_canvas.delete("all")
            # Collect the calibration points for this circle
            circle_calibration_points = get_gaze_point()
            calibration_points.append(circle_calibration_points)
        print(calibration_points)
        calibration_window
        calibration_window.destroy()
        track_eyes(calibration_points)

    calibration_window.resizable(False, False)
    calibration_window.mainloop()


def open_main_menu():
    # Define menu dimensions and center window
    w = 521
    h = 699
    x = (main_menu.winfo_screenwidth() // 2) - (w // 2)
    y = (main_menu.winfo_screenheight() // 2) - (h // 2)
    main_menu.geometry('{}x{}+{}+{}'.format(w, h, x, y))

    canvas = Canvas(
        main_menu,
        bg="#1B2E49",
        height=699,
        width=521,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        34.0,
        43.0,
        anchor="nw",
        text="Gaze Controlled",
        fill="#ECECEC",
        font=("Lato Regular", 64 * -1)
    )

    canvas.create_text(
        34.0,
        120.0,
        anchor="nw",
        text="Computer",
        fill="#ECECEC",
        font=("Lato Regular", 64 * -1)
    )

    image_image_1 = PhotoImage(file=os.path.join(script_dir, "assets/image_1.png"))
    canvas.create_image(
        260.0,
        469.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=os.path.join(script_dir, "./assets/button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=127.0,
        y=337.0,
        width=268.0,
        height=73.0
    )

    button_image_2 = PhotoImage(
        file=os.path.join(script_dir, "./assets/button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=open_calibration_window,
        relief="flat"
    )
    button_2.place(
        x=127.0,
        y=435.0,
        width=268.0,
        height=73.0
    )

    button_image_3 = PhotoImage(
        file=os.path.join(script_dir, "./assets/button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(
        x=127.0,
        y=533.0,
        width=268.0,
        height=73.0
    )

    image_image_2 = PhotoImage(
        file=os.path.join(script_dir, "./assets/image_2.png"))
    image_2 = canvas.create_image(
        394.0,
        165.0,
        image=image_image_2
    )
    main_menu.resizable(False, False)

    main_menu.mainloop()

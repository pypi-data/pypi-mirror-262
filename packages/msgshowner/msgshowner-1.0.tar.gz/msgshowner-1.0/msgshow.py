import customtkinter
import os

def show_info(titler: str, msg: str):
    def on_drag(event):
        si.geometry(f"{event.x_root}+{event.y_root}")
    def close_app(event):
        si.destroy()
        pass
    def okay():
        si.destroy()
        pass

    main_si = customtkinter.CTk()
    main_si.geometry('1x1')
    main_si.attributes('-alpha', 0)

    si = customtkinter.CTk()
    si.configure(master=main_si)
    si.title(titler)
    si.geometry('500x150')
    si.wm_overrideredirect(True)

    title_bar = customtkinter.CTkFrame(si, fg_color="#42047c", corner_radius=10, height=35, width=480)
    title_bar.bind('<B1-Motion>', on_drag)
    title_bar.place(x=10, y=15)

    name_window = customtkinter.CTkLabel(title_bar, text=titler, text_color="white", font=("Rostov", 15))
    name_window.place(x=10, y=2)


    close_window = customtkinter.CTkLabel(title_bar, text="X", font=("Rostov", 12))
    close_window.place(x=455, y=3)
    close_window.bind('<Button-1>', close_app)

    okay_button = customtkinter.CTkButton(si, text="Хорошо", font=("Rostov", 20), fg_color="#42047c", command=okay)
    okay_button.place(x=350, y=105)

    text = customtkinter.CTkLabel(si, text=msg, text_color="white", font=("Rostov", 20))
    text.place(x=50, y=75)

    si.mainloop()

def show_error(titler: str, msg: str):
    def on_drag(event):
        si.geometry(f"{event.x_root}+{event.y_root}")

    def close_app(event):
        si.destroy()
        pass
    def okay():
        si.destroy()
        pass

    main_si = customtkinter.CTk()
    main_si.geometry('1x1')
    main_si.attributes('-alpha', 0)

    si = customtkinter.CTk()
    si.configure(master=main_si)
    si.title(titler)
    si.geometry('500x150')
    si.wm_overrideredirect(True)

    title_bar = customtkinter.CTkFrame(si, fg_color="#42047c", corner_radius=10, height=35, width=480)
    title_bar.bind('<B1-Motion>', on_drag)
    title_bar.place(x=10, y=15)

    name_window = customtkinter.CTkLabel(title_bar, text=titler, text_color="white", font=("Rostov", 20))
    name_window.place(x=10, y=2)

    close_window = customtkinter.CTkLabel(title_bar, text="X", font=("Rostov", 12))
    close_window.place(x=455, y=3)
    close_window.bind('<Button-1>', close_app)

    okay_button = customtkinter.CTkButton(si, text="Закрыть", font=("Rostov", 20), fg_color="#42047c", command=okay)
    okay_button.place(x=350, y=105)

    text = customtkinter.CTkLabel(si, text=msg, text_color="white", font=("Rostov", 20))
    text.place(x=20, y=65)

    si.mainloop()


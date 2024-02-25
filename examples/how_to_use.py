import customtkinter

from ctk_navbar import CTkNavbar

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")

if __name__ == "__main__":

    root = customtkinter.CTk()
    root.geometry("640x480")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    nav = CTkNavbar(master=root,  label_text="CTkNavbar", end_buttons_count=1)
    # test page
    nav.add_page(button_text="First")
    # test page
    nav.add_page(button_text="Second")
    # test page
    nav.add_page(button_text="Third")

    # create custom frame with button
    custom_frame = customtkinter.CTkFrame(master=nav)
    change_appearance_mode_btn = customtkinter.CTkButton(
        master=custom_frame,
        text="Change appearance mode",
        command=lambda: customtkinter.set_appearance_mode("Dark"
                                                          if customtkinter.get_appearance_mode() == "Light"
                                                          else "Light")
    )
    # pack button to new custom frame
    change_appearance_mode_btn.grid(row=0, column=0, sticky="nsew")
    # custom button in navbar
    custom_btn = customtkinter.CTkButton(master=nav.sidebar_frame, text="Settings", bg_color="red")
    # add custom button and frame
    nav.add_page(btn=custom_btn, frame=custom_frame)

    nav.grid(row=0, column=0, sticky="nsew")

    root.mainloop()

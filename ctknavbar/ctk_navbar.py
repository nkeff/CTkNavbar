import random

import customtkinter as ctk

BTN_ACTIVE_COLOR = ("gray75", "gray25")
BTN_TEXT_COLOR = ("gray10", "gray90")
BTN_HOVER_COLOR = ("gray70", "gray30")
SIDEBAR_BTN_PADDINGS = 6


class CTkNavbar(ctk.CTkFrame):
    def __init__(self,
                 master,
                 auto_render: bool = True,
                 end_buttons_count: int = 0,
                 default_page: int = 0,
                 label_text: str = None,
                 label: ctk.CTkLabel = None,
                 **kwargs):
        super().__init__(master, **kwargs)

        self._active_page_id = default_page
        self._auto_render = auto_render
        self._end_buttons_count = end_buttons_count
        self._label_text, self._label = label_text, label

        self._is_it_already_rendered = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)

        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.buttons_list = []
        self.frames_list = []

        if self._get_label() is not None:
            label = self._get_label()
            label.grid(row=0, column=0, padx=SIDEBAR_BTN_PADDINGS, pady=SIDEBAR_BTN_PADDINGS*4, sticky="nsew")

    def add_page(self, button_text: str = "[BUTTON]", btn: ctk.CTkButton = None, frame: ctk.CTkFrame = None)\
            -> ctk.CTkFrame:
        btn_id = len(self.buttons_list)

        if not btn:
            btn = DefaultSidebarButton(master=self.sidebar_frame,
                                       text=button_text,
                                       command=lambda: self._render(btn_id))
        btn.configure(command=lambda: self._render(btn_id))
        if not frame:
            frame = DefaultNavbarFrame(master=self)

        # if self._get_row_index_to_insert_new_button() is not None:
        #     self.buttons_list.insert(self._get_row_index_to_insert_new_button(), btn)
        #     self.frames_list.insert(self._get_row_index_to_insert_new_button(), frame)
        # else:
        self.buttons_list.append(btn)
        self.frames_list.append(frame)

        if self._auto_render and self._is_it_already_rendered:
            self._render()

        return frame

    def grid(self, **kwargs):
        """
        Render everything at the moment when the navigation block is added to the program
        """
        super().grid(**kwargs)
        if self._auto_render:
            self._render(btn_id=self._active_page_id)
            self._is_it_already_rendered = True

    def render(self):
        """
        Render manually
        """
        self._render()

    def _render(self, btn_id=None):
        """
        Render all blocks
        """
        if btn_id is not None:
            self._active_page_id = btn_id

        # draw all buttons
        for i, btn in enumerate(self.buttons_list):
            btn.grid(row=self._i(i),
                     column=0,
                     padx=SIDEBAR_BTN_PADDINGS,
                     pady=SIDEBAR_BTN_PADDINGS if self._i(i) == 0 else (0, SIDEBAR_BTN_PADDINGS), sticky="sew")

            # stick the buttons to the end
            if i == self._get_row_index_for_align_btn_end():
                self.sidebar_frame.grid_rowconfigure(self._i(self._get_row_index_for_align_btn_end()), weight=1)
            else:
                self.sidebar_frame.grid_rowconfigure(self._i(i), weight=0)

        # set button color for selected button
        for i, btn in enumerate(self.buttons_list):
            if i == self._get_active_page_id():
                btn.configure(fg_color=BTN_ACTIVE_COLOR)
            else:
                btn.configure(fg_color="transparent")

        # draw_selected_frame
        for i, frame in enumerate(self.frames_list):
            if i == self._get_active_page_id():
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()
        print("RENDER")

    def _get_row_index_for_align_btn_end(self) -> int:
        return 0 \
            if len(self.buttons_list) - self._end_buttons_count < 0 \
            else len(self.buttons_list) - self._end_buttons_count

    def _get_row_index_to_insert_new_button(self) -> int | None:
        return None \
            if len(self.buttons_list) - self._end_buttons_count < 0 \
            else len(self.buttons_list) - self._end_buttons_count

    def _get_active_page_id(self):
        return self._active_page_id if self._active_page_id in range(len(self.buttons_list)) else 0

    def _get_label(self) -> ctk.CTkLabel | None:
        if self._label is None and self._label_text is None:
            return None

        label = DefaultNavbarLabel(master=self.sidebar_frame, text=self._label_text) \
            if self._label is None \
            else self._label
        return label

    def _i(self, i):
        if self._label is None and self._label_text is None:
            return i
        return i+1


class DefaultSidebarButton(ctk.CTkButton):
    """
    Default sidebar button
    If you want to use custom sidebar button, you can do it
    """

    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            master,
            corner_radius=8,
            height=40,
            border_spacing=5,
            text=text,
            fg_color="transparent",
            text_color=BTN_TEXT_COLOR,
            hover_color=BTN_HOVER_COLOR,
            anchor="center",
            command=command
        )


class DefaultNavbarFrame(ctk.CTkFrame):
    """
    Default sidebar frame
    It's created with corner_radius=0 and random background color
    (Use for prototype your app)
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure(corner_radius=0, fg_color=self._get_random_color())

    @staticmethod
    def _get_random_color() -> str:
        return f"#{''.join([random.choice('123456789ABCDEF') for _ in range(6)])}"


class DefaultNavbarLabel(ctk.CTkLabel):
    """

    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=0,
                       fg_color="transparent",
                       font=ctk.CTkFont(size=20, weight="bold"))
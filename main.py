if __name__ == "__main__":
    from picpy.views.globals.window import Window
    from picpy.views.main_view import MainView
    from picpy.controllers.main_controller import MainController
    from ttkbootstrap import constants as c

    window = Window()
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    main_view = MainView(window)
    main_view.grid(row=0, column=0, sticky=c.NSEW)
    controller = MainController(main_view)
    window.mainloop()

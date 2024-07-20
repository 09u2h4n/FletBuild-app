import flet as ft
import platform

def main(page: ft.Page):
    page.title = "FLETBUILD"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="blue")

    def toggle_dark_mode(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        dark_mode_switch.value = page.theme_mode == ft.ThemeMode.DARK
        page.update()

    def change_theme(e):
        page.theme = ft.Theme(color_scheme_seed=theme_dropdown.value)
        page.update()

    dark_mode_switch = ft.Switch(value=True, on_change=toggle_dark_mode)

    theme_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("blue", "Default"),
            ft.dropdown.Option("red", "Rose"),
            ft.dropdown.Option("orange", "Orange"),
            ft.dropdown.Option("green", "Lime"),
        ],
        value="blue",
        on_change=change_theme,
        width=200,
    )

    include_packages_dialog = ft.AlertDialog(
        title=ft.Text("Include Packages"),
        content=ft.Column([
            ft.Row([ft.Checkbox(label="Video")]),
            ft.Row([ft.Checkbox(label="Audio")]),
            ft.Row([ft.Checkbox(label="Webview")]),
            ft.Row([ft.Checkbox(label="Geolocator")]),
            ft.Row([ft.Checkbox(label="Permission handler")]),
            ft.Row([ft.Checkbox(label="Audio recorder")]),
            ft.Row([ft.Checkbox(label="Map")]),
        ])
    )

    settings_dialog = ft.AlertDialog(
        title=ft.Text("Settings"),
        content=ft.Container(
            content=ft.Column([
                ft.Row([ft.Text("Dark mode", width=100), dark_mode_switch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("App Theme", width=100), theme_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], tight=True),
            width=300,
            padding=10,
        ),
    )

    def open_settings(e):
        page.overlay.append(settings_dialog)
        settings_dialog.open = True
        page.update()

    log_box = ft.Container(
        content=ft.Column([
            ft.Text(f"target_platform={None}")
        ]),
        border=ft.border.all(1),
        padding=10
    )

    route_path = ft.Text("/")

    def update_target_platform(target_platform):
        log_box.content.controls[0].value = f"target_platform={target_platform}"
        route_path.value = "/"+target_platform
        page.update()

    def open_packages(e):
        page.overlay.append(include_packages_dialog)
        include_packages_dialog.open = True
        page.update()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        leading=ft.Image(src="logo-fletbuild.png"),
                        title=ft.Text("FLETBUILD", weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        actions=[
                            ft.IconButton(
                                icon=ft.icons.CODE,
                                tooltip="GitHub",
                                on_click=lambda _: page.launch_url("https://github.com/09u2h4n")
                            ),
                            ft.IconButton(ft.icons.SETTINGS, on_click=open_settings),
                        ]
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Column([
                                ft.Container(
                                    content=ft.Image(src="linux-logo.png", width=150, height=150),
                                    on_click=lambda _: update_target_platform("linux")
                                ),
                                ft.Text("Linux")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                            ft.Column([
                                ft.Container(
                                    content=ft.Image(src="android-logo.png", width=150, height=150),
                                    on_click=lambda _: update_target_platform("android")
                                ),
                                ft.Text("Android")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                            ft.Column([
                                ft.Container(
                                    content=ft.Image(src="web-logo.png", width=150, height=150),
                                    on_click=lambda _: update_target_platform("web")
                                ),
                                ft.Text("Web")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ], alignment=ft.MainAxisAlignment.CENTER),

                        ft.ElevatedButton("Start", on_click=lambda e: page.go(route_path.value)),
                            
                            log_box

                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
                    ])
            )

        if page.route == "/linux":
            page.views.append(
                ft.View(
                    "/linux",
                    [
                    ft.AppBar(
                        leading=ft.Image(src="logo-fletbuild.png"),
                        title=ft.Text("FLETBUILD", weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        actions=[
                            ft.IconButton(
                                icon=ft.icons.CODE,
                                tooltip="GitHub",
                                on_click=lambda _: page.launch_url("https://github.com/09u2h4n")
                            ),
                            ft.IconButton(ft.icons.SETTINGS, on_click=open_settings),
                        ]
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Column([
                                ft.Container(
                                    content=ft.Image(src="linux-logo.png", width=150, height=150),
                                ),
                                ft.Text("Linux")
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([
                                ft.Tooltip(
                                content=ft.TextField(label="Project name"),
                                message="Project name for executable or bundle"
                                ),
                                ft.Tooltip(
                                    content=ft.TextField(label="Description"),
                                    message="The description to use for executable or bundle"
                                ),
                                ft.Tooltip(
                                    content=ft.TextField(label="Product name"),
                                    message="Project display name that is shown in window titles and about app dialogs"
                                ),
                                ft.Tooltip(
                                    content=ft.TextField(label="Organization name"),
                                    message='Organization name in reverse domain name notation, e.g. "com.mycompany" - combined with project name and used as an iOS and Android bundle ID'
                                ),
                            ]),
                            ft.Column([
                                ft.Tooltip(
                                content=ft.TextField(label="Company name"),
                                message="Company name to display in about app dialogs"
                                ),
                                ft.Tooltip(
                                    content=ft.TextField(label="Copyright"),
                                    message="Copyright text to display in about app dialogs"
                                ),
                                #ft.Tooltip(
                                #    content=ft.TextField(label="flutter-build-args"),
                                #    message="Additional arguments for flutter build command"
                                #),
                                ft.Tooltip(
                                    content=ft.Container(content=ft.TextField("Include packages", disabled=True), on_click=open_packages),
                                    message="Include extra Flutter Flet packages, such as flet_video, flet_audio, etc."
                                ),
                                ft.Tooltip(
                                    content=ft.TextField(label="Build number"),
                                    message="Build number - an identifier used as an internal version number"
                                ),
                            ]),
                            ft.Column([
                                ft.Tooltip(
                                    content=ft.TextField(label="Build version"),
                                    message='Build version - a "x.y.z" string used as the version number shown to users'
                                ),
                            ])
                            

                            
                            
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
                    ]
                )
            )
        elif page.route == "/android":
            page.views.append(
                ft.View(
                    "/android",
                    [
                        ft.Text("ANDROID")
                    ]
                )
            )
        elif page.route == "/web":
            page.views.append(
                ft.View(
                    "/web",
                    [
                        ft.Text("WEB")
                    ]
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir=".")

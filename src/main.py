import flet as ft
from typing import Optional, Callable

def main(page: ft.Page):
    # Set the title, theme, and scroll behavior of the page
    page.title = "FLETBUILD"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.scroll = True

    # Function to toggle between dark and light mode
    def toggle_dark_mode(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        dark_mode_switch.value = page.theme_mode == ft.ThemeMode.DARK
        page.update()

    # Function to change the theme based on dropdown selection
    def change_theme(e):
        page.theme = ft.Theme(color_scheme_seed=theme_dropdown.value)
        page.update()

    # Switch to toggle dark mode
    dark_mode_switch = ft.Switch(value=True, on_change=toggle_dark_mode)

    # Dropdown to select theme color
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

    # Container for including extra packages
    include_packages_container = ft.Container(
        content=ft.Column([
            ft.Text("Include Packages"),
            ft.Row([ft.Checkbox(label="Video")]),
            ft.Row([ft.Checkbox(label="Audio")]),
            ft.Row([ft.Checkbox(label="Webview")]),
            ft.Row([ft.Checkbox(label="Geolocator")]),
            ft.Row([ft.Checkbox(label="Permission handler")]),
            ft.Row([ft.Checkbox(label="Audio recorder")]),
            ft.Row([ft.Checkbox(label="Map")]),
        ])
    )

    # Dialog for settings
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

    # Function to open the settings dialog
    def open_settings(e):
        page.overlay.append(settings_dialog)
        settings_dialog.open = True
        page.update()

    # Container for logging platform information
    log_box = ft.Container(
        content=ft.Column([
            ft.Text(f"target_platform={None}")
        ]),
        border=ft.border.all(1),
        padding=10
    )

    # Application bar with title, leading icon, and actions
    app_bar = ft.AppBar(
        leading=ft.Image(src="icon.png"),
        title=ft.Container(content=ft.Text("FLETBUILD", weight=ft.FontWeight.BOLD), on_click=lambda _: page.go("/")),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.icons.CODE,
                tooltip="GitHub",
                on_click=lambda _: page.launch_url("https://github.com/09u2h4n")
            ),
            ft.IconButton(ft.icons.SETTINGS, on_click=open_settings),
        ]
    )

    # Text to display the current route path
    route_path = ft.Text("/")

    # Function to update the target platform and log it
    def update_target_platform(target_platform):
        log_box.content.controls[0].value = f"target_platform={target_platform}"
        route_path.value = "/"+target_platform
        page.update()

    # Function to create a platform selector with optional on-click behavior
    def platform_selector(src: str, platform_name: str, on_click: Optional[Callable[[str], None]] = None):
        image = ft.Image(src=src, width=150, height=150)
        
        if on_click:
            container = ft.Container(
                content=image,
                on_click=lambda _: on_click(platform_name.lower())
            )
        else:
            container = ft.Container(content=image)

        return ft.Column([
            container,
            ft.Text(platform_name)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    # Function to create a tooltip with a text field and message
    def optionw_tooltip(label, message):
        return ft.Tooltip(
            content=ft.TextField(label=label),
            message=message
        )
    
    # Tooltips for various project settings
    project_name = optionw_tooltip("Project name", "Project name for executable or bundle")
    description = optionw_tooltip("Description", "The description to use for executable or bundle")
    product_name = optionw_tooltip("Product name", "Project display name that is shown in window titles and about app dialogs")
    organization_name = optionw_tooltip("Organization name", 'Organization name in reverse domain name notation, e.g. "com.mycompany" - combined with project name and used as an iOS and Android bundle ID')
    company_name = optionw_tooltip("Company name", "Company name to display in about app dialogs")
    copyright_text = optionw_tooltip("Copyright", "Copyright text to display in about app dialogs")
    build_number = optionw_tooltip("Build number", "Build number - an identifier used as an internal version number")
    build_version = optionw_tooltip("Build version", 'Build version - a "x.y.z" string used as the version number shown to users')
    include_packages = ft.Tooltip(content=include_packages_container, message="Include extra Flutter Flet packages, such as flet_video, flet_audio, etc.")

    # Function to handle route changes and update the view accordingly
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    app_bar,
                    ft.Column([
                        ft.Row([
                            platform_selector("linux-logo.png", "linux", update_target_platform),
                            platform_selector("android-logo.png", "android", update_target_platform),
                            platform_selector("web-logo.png", "web", update_target_platform),
                            ], alignment=ft.MainAxisAlignment.CENTER),

                        ft.ElevatedButton("Start", on_click=lambda e: page.go(route_path.value)),
                            
                            log_box

                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
                    ])
            )

        # View for the Linux platform
        if page.route == "/linux":
             page.views.append(
                ft.View(
                    "/linux",
                    [
                    app_bar,
                    ft.Column([
                        ft.Row([
                            platform_selector("linux-logo.png", "linux"),
                            ft.Column([
                                project_name,
                                description,
                                product_name,
                                organization_name,
                            ]),
                            ft.Column([
                                company_name,
                                copyright_text,
                                build_number,
                                build_version,
                            ]),
                            ft.Column([
                                include_packages
                            ]),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.ElevatedButton("Start", on_click=lambda _: print(project_name.content.value))
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
                    ]
                )
            )
        # View for the Android platform
        elif page.route == "/android":
            page.views.append(
                ft.View(
                    "/android",
                    [
                        ft.Text("ANDROID")
                    ]
                )
            )
        # View for the Web platform
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

    # Function to handle view pop (back navigation)
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Set the route change and view pop handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

# Run the Flet application with the main function
ft.app(target=main, view=ft.AppView.FLET_APP, assets_dir=".")

import threading

import customtkinter as ctk
import streamlit as st
import os
from PIL import Image

from toolboxv2.mods.CloudM.UI.backend import get_user


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.token_entry = None
        self.name_entry = None
        self.entry_email = None
        self.user = None
        self.title('Meine Anwendung')
        self.geometry('800x600')
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        os.path.join(image_path, "img.png")
        logo_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "img.png")),
                                  size=(740, 158))

        label = ctk.CTkLabel(self, image=logo_image, text="")
        label.pack(expand=True)

        # Tab Control
        self.tab_control = ctk.CTkTabview(self)
        self.tab_control.pack(fill="both", expand=True, padx=10, pady=10)

        # User Tab
        self.tab_user = self.tab_control.add(name="User")
        self.display_user_info()

        # Mods Tab
        self.tab_mods = self.tab_control.add(name="Mods")
        ctk.CTkLabel(self.tab_mods, text="Mods-Bereich").pack(pady=20)

        # System Tab
        self. tab_system = self.tab_control.add(name="System")
        ctk.CTkLabel(self.tab_system, text="System-Bereich").pack(pady=20)

    #def display_user_info(self):
#
    #    ctk.CTkLabel(self.tab_user, text="User-Bereich").pack(pady=20)
    #    user = get_user("asd")
    #    if user is None:
    #        # Login Formular
    #        ctk.CTkLabel(self.tab_user, text="Name:").pack()
    #        name_entry = ctk.CTkEntry(self.tab_user)
    #        name_entry.pack()
#
    #        ctk.CTkLabel(self.tab_user, text="Token:").pack()
    #        token_entry = ctk.CTkEntry(self.tab_user)
    #        token_entry.pack()
#
    #        login_button = ctk.CTkButton(self.tab_user, text="Log In", command=self.login)
    #        login_button.pack()
#
    #        create_acc_link = ctk.CTkLabel(self.tab_user, text="Create Account", cursor="hand2")
    #        create_acc_link.pack()
    #        create_acc_link.bind("<Button-1>", lambda e: self.open_create_account_page())
    #    else:
    #        # Benutzerdaten anzeigen
    #        ctk.CTkLabel(self.tab_user, text=f"Name: {user.name}").pack()
    #        ctk.CTkLabel(self.tab_user, text=f"Email: {user.email}").pack()
    #        ctk.CTkLabel(self.tab_user, text=f"Level: {user.level}").pack()
#
    #        if user.name == "root":
    #            # Root-Benutzer Optionen
    #            ctk.CTkLabel(self.tab_user, text="Root User").pack()
    #            ctk.CTkButton(self.tab_user, text="Add User", command=self.add_user).pack()
    #            ctk.CTkButton(self.tab_user, text="Remove User", command=self.remove_user).pack()
    #            ctk.CTkButton(self.tab_user, text="Set User Level", command=self.set_user_level).pack()

    def display_user_info(self):
        for widget in self.tab_user.winfo_children():
            widget.destroy()

        if self.user is None:
            # Login Formular
            self.build_login_form()
        else:
            # Benutzerdaten oder Verwaltungsoptionen anzeigen
            if self.user.name == "root":
                self.build_root_user_view()
            else:
                self.build_normal_user_view()

    def build_login_form(self):

        ctk.CTkLabel(self.tab_user, text="Log In").pack(pady=(10, 0))
        self.name_entry = ctk.CTkEntry(self.tab_user, placeholder_text="Name: ")
        self.name_entry.pack(pady=(0, 5))

        self.token_entry = ctk.CTkEntry(self.tab_user, placeholder_text="Token: ")
        self.token_entry.pack(pady=(0, 5))

        login_button = ctk.CTkButton(self.tab_user, text="Log In", command=self.login)
        login_button.pack(pady=10)

        create_acc_link = ctk.CTkLabel(self.tab_user, text="Create Account", cursor="hand2")
        create_acc_link.pack()
        create_acc_link.bind("<Button-1>", lambda e: self.open_create_account_page())

    def build_root_user_view(self):
        # Bereich für Benutzerinformationen und -aktionen
        info_frame = ctk.CTkFrame(self.tab_user)
        info_frame.pack(side="left", fill="both", expand=True)

        label_user_info = ctk.CTkLabel(info_frame, text=f"Name: {self.user.name}\nEmail: {self.user.email}\nLevel: {self.user.level}")
        label_user_info.pack(pady=10)

        if not self.user.is_persona:
            add_persona_button = ctk.CTkButton(info_frame, text="Add Persona Key", command=self.add_persona_action)
            add_persona_button.pack(pady=10)

        # Bereich für die Verwaltung von Benutzern
        manage_frame = ctk.CTkFrame(self.tab_user)
        manage_frame.pack(side="left", fill="both", expand=True)

        search_entry = ctk.CTkEntry(manage_frame, placeholder_text="Search user...")
        search_entry.pack(pady=(10, 20))

        # Beispiel für eine Liste von Benutzernamen
        user_list = self.get_all_users()  # Diese Methode sollte eine Liste von Benutzernamen zurückgeben
        for username in user_list:
            ctk.CTkLabel(manage_frame, text=username).pack()

        # Bereich für das Generieren und Versenden von Einladungsschlüsseln
        invite_frame = ctk.CTkFrame(self.tab_user)
        invite_frame.pack(side="left", fill="both", expand=True)

        generate_invite_button = ctk.CTkButton(invite_frame, text="Generate Invite Key",
                                               command=self.generate_invite_action)
        generate_invite_button.pack(pady=10)

        self.entry_email = ctk.CTkEntry(invite_frame, placeholder_text="Email")
        self.entry_email.pack(pady=(10, 20))

        send_invite_button = ctk.CTkButton(invite_frame, text="Send Invite Email", command=self.send_invite_action)
        send_invite_button.pack()

    def build_normal_user_view(self):
        label_user_info = ctk.CTkLabel(self,
                                       text=f"Name: {self.user.name}\nEmail: {self.user.email}\nLevel: {self.user.level}")
        label_user_info.pack(pady=10)

        # Scrollable Bereich für user_pass_pub_devices
        self.create_scrollable_text_area("Devices", self.user.user_pass_pub_devices)

        # Scrollable Bereich für user_pass_pub_persona
        self.create_scrollable_text_area("Personas", [f"{persona}: {key}" for persona, key in
                                                      self.user.user_pass_pub_persona.items()])

    def create_scrollable_text_area(self, title, items):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, pady=10)

        label = ctk.CTkLabel(frame, text=title)
        label.pack()

        text_area = ctk.CTkTextbox(frame, wrap="word", height=10)
        text_area.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(frame, command=text_area.yview)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        text_area.configure(yscrollcommand=scrollbar.set)

        for item in items:
            text_area.insert(ctk.END, f"{item}\n")
        text_area.configure(state="disabled")

    def generate_invite_action(self):
        pass

    def send_invite_action(self):
        print(self.entry_email)
        pass

    def add_persona_action(self):
        pass

    def login(self):
        # Implementiere Login-Logik hier
        print(self.name_entry.get())
        self.user = get_user(self.name_entry.get())

        self.display_user_info()

    def open_create_account_page(self):
        # Implementiere Logik zum Öffnen der Account-Erstellungsseite
        pass

    def add_user(self):
        # Implementiere Logik zum Hinzufügen eines Benutzers
        pass

    def remove_user(self):
        # Implementiere Logik zum Entfernen eines Benutzers
        pass

    def set_user_level(self):
        # Implementiere Logik zum Setzen des Benutzerlevels
        pass

    def get_all_users(self):
        return ["Tom", "Peter"]


def main():
    # Tab Auswahl
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
    st.image(Image.open(os.path.join(image_path, "img.png")))
    print(os.path.join(image_path, "img.png"))
    User, Mods, System = st.tabs(['User', 'Mods', 'System'])

    with User:
        st.header("User-Bereich")
        user_token = st.text_input("User Token")
        # Hier könnten weitere Widgets für den User-Bereich hinzugefügt werden
        user = get_user(user_token)
        if user is None:
            # Login Formular
            name = st.text_input("Name")
            token = st.text_input("Token")
            if st.button("Log In"):
                # Implementiere Login-Logik hier
                pass
            st.markdown("[Create Account](http://localhost:5000/singin)")
        else:
            # Benutzerdaten anzeigen
            st.write(f"Name: {user.name}")
            st.write(f"Email: {user.email}")
            st.write(f"Level: {user.level}")

            if user.name == "root":
                # Root-Benutzer Optionen
                st.write("Root User")
                if st.button("Add User"):
                    # Implementiere Logik zum Hinzufügen eines Benutzers
                    pass
                if st.button("Remove User"):
                    # Implementiere Logik zum Entfernen eines Benutzers
                    pass
                if st.button("Set User Level"):
                    # Implementiere Logik zum Setzen des Benutzerlevels
                    pass

    with Mods:
        st.header("Mods-Bereich")
        # Hier könnten weitere Widgets für den Mods-Bereich hinzugefügt werden

    with System:
        st.header("System-Bereich")
        # Hier könnten weitere Widgets für den System-Bereich hinzugefügt werden


if __name__ == "__main__":
    main()

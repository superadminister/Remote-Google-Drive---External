# -*- coding: <utf-8> -*-

"""
Experimental program, implement module by contributors accessing google drive service through API
"""

from tkinter import *
from tkinter.messagebox import showerror
from tkinter.font import Font
from tkinter import filedialog
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from threading import Thread
from os.path import basename
from httplib2.error import ServerNotFoundError
import socket


class App(Tk):
    """
    This application or program contains a several operations such managements
    """
    def __init__(self, **kwargs):
        super(App, self).__init__(**kwargs)
        self.upload_button = Button()
        self.newfile_button = Button()
        self.refresh_button = Button()
        self.exit_button = Button()
        self.notif_label = Label()
        self.user_label = Label()
        self.files_list = Listbox()
        self.auth = GoogleAuth()
        self.gdrive = GoogleDrive()
        self.file_query = ''
        self.files = ''
        self.thread_userinfo()
        self.thread_list_files()
        self.widgets_configurations()
        self.window_configurations()

    def authentication(self):
        self.auth.LocalWebserverAuth()

    def thread_userinfo(self):
        """
        Thread needed because nothing crash program, and daemon service needed
        """
        threading = Thread(target=self.get_user_info, args=(self.auth,))
        threading.daemon = True
        threading.start()

    def thread_list_files(self):
        """
        Method used for listing all files in drive google
        """
        threading = Thread(target=self.list_files)
        threading.daemon = True
        threading.start()

    def thread_upload_program(self):
        threading = Thread(target=self.upload_program)
        threading.daemon = True
        threading.start()

    def window_configurations(self):
        self.title(f'''Remote Google Drive(Experimental) - Wait''')
        self.geometry('500x500')
        self.resizable(width=False, height=False)
        self.mainloop()  # simplicity reason

    def widgets_configurations(self):
        self.upload_button.config(text='Upload', font=Font(family='Laksaman', size=10), command=self.thread_upload_program)
        self.upload_button.place(x=20, y=20, width=150, height=30)

        self.newfile_button.config(text='New', font=Font(family='Laksaman', size=10))
        self.newfile_button.place(x=20, y=50, width=150, height=30)

        self.refresh_button.config(text='Refresh', font=Font(family='Laksaman', size=10), command=self.refresh_list)
        self.refresh_button.place(x=20, y=80, width=150, height=30)

        self.exit_button.config(text='Exit', font=Font(family='Laksaman', size=10), command=self.destroy)
        self.exit_button.place(x=20, y=110, width=150, height=30)

        self.files_list.place(x=190, y=20, width=290, height=460)

        self.user_label.config(text=f'''Wait''', font=Font(family='Laksaman', size=10))
        self.user_label.place(x=20, y=400)

    def get_user_info(self, auth):
        """
        Authenticator by OAuth
        """
        self.gdrive.auth = auth
        userInfo = self.gdrive.GetAbout()
        userInfo = userInfo['user']
        userInfo = dict(userInfo)
        userInfo = userInfo['displayName'], userInfo['permissionId']

        self.title(f'''Remote Google Drive(Experimental) - {userInfo[0]}''')
        self.user_label.config(text=f'''{userInfo[0]}, \n {userInfo[1]}''',
                               font=Font(family='Laksaman', size=10))

    def upload_program(self):
        file_query = Upload().save()
        if not file_query:
            showerror(title='Error', message='File is not found')
        else:
            self.gdrive.auth = self.auth
            base_name_file = basename(file_query)
            upload = self.gdrive.CreateFile(metadata={'title': base_name_file})
            upload.SetContentFile(filename=file_query)
            upload.Upload()

    def list_files(self):
        self.files = self.gdrive.ListFile().GetList()  # return dictionary values

        for x in self.files:
            self.files_list.insert('end', f'''{x['title']}''')

    def refresh_list(self):
        self.files_list.delete(1, 'end')
        self.list_files()


class Upload(Tk):
    def __init__(self, **kwargs):
        super(Upload, self).__init__(**kwargs)
        self.find_file = filedialog.askopenfilename(
            defaultextension='',
            filetypes='',
            initialdir='~/',
            initialfile='',
            parent=None,
            title='Choose File',
            typevariable=''
        )

    def save(self):
        return self.find_file


if __name__ == '__main__':
    App()

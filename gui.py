import os
import subprocess as sub
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *


class Gui(Tk):
    def __init__(self):
        super().__init__()
        self.title("Git Walker")
        self.actual_id = StringVar()
        self.git_path = StringVar(value="Select git project to follow:")
        self.num_commits = IntVar(value=0)
        self.commits: list[str] = []
        self.target_id = None
        self.current_index = IntVar()

        self.columnconfigure("all", weight=1)
        self.rowconfigure("all", weight=1)

        Label(self, text="Git Walker", font=("", 14), anchor=CENTER).pack()

        Button(self, textvariable=self.git_path, command=lambda: self.select_path()).pack(anchor=CENTER, expand=True,
                                                                                          fill=X)

        fr = Frame(self)
        fr.pack(anchor=CENTER, expand=True, fill=X)

        self.b_first = Button(fr, text="First", command=lambda: self.first(), state=DISABLED)
        self.b_first.grid(row=0, column=0, sticky=NSEW)

        self.b_prev = Button(fr, text="Previous", command=lambda: self.previous(), state=DISABLED)
        self.b_prev.grid(row=0, column=1, sticky=NSEW)

        self.b_next = Button(fr, text="Next", command=lambda: self.next(), state=DISABLED)
        self.b_next.grid(row=0, column=2, sticky=NSEW)

        self.b_last = Button(fr, text="Last", command=lambda: self.last(), state=DISABLED)
        self.b_last.grid(row=0, column=3, sticky=NSEW)

        Label(self, textvariable=self.actual_id).pack()

        self.configure_columns(fr)

    @staticmethod
    def configure_columns(*frames: Frame):
        for frame in frames:
            for c in range(frame.grid_size()[0]):
                frame.columnconfigure(c, weight=1)

    def first(self):
        self.target_id = self.commits[-1]
        self.current_index.set(self.commits.index(self.target_id))
        self.check()

    def next(self):
        try:
            self.current_index.set(self.current_index.get() - 1)
            self.target_id = self.commits[self.current_index.get()]
        except IndexError:
            self.target_id = self.commits[0]
            self.current_index.set(self.commits.index(self.target_id))
        finally:
            self.check()

    def previous(self):
        try:
            self.current_index.set(self.current_index.get() + 1)
            self.target_id = self.commits[self.current_index.get()]
        except IndexError:
            self.target_id = self.commits[-1]
            self.current_index.set(self.commits.index(self.target_id))
        finally:
            self.check()

    def last(self):
        self.target_id = self.commits[0]
        self.current_index.set(self.commits.index(self.target_id))
        self.check()

    def read_commits_ids(self) -> None:
        out = sub.run("git rev-list --all", capture_output=True)
        self.commits = [line.decode("utf-8").strip() for line in out.stdout.split(b'\n')]
        del self.commits[-1]
        self.num_commits.set(len(self.commits) - 1)
        print(self.commits)

    def read_active_commit_id(self) -> None:
        out = sub.run("git rev-parse HEAD", capture_output=True)
        self.actual_id.set(out.stdout.split()[0].decode("utf-8"))
        self.current_index.set(self.commits.index(self.actual_id.get()))

    def check(self):
        sub.run(f"git checkout {self.target_id} --quiet")
        self.read_active_commit_id()

    def select_path(self):
        path = filedialog.askdirectory()
        if path != "" and os.path.isdir(path + "\.git"):
            self.git_path.set(path)
            os.chdir(path)
            self.read_commits_ids()
            self.read_active_commit_id()
            self.enable_buttons()
        else:
            messagebox.showerror("Error", "Not a git directory!")

    def enable_buttons(self):
        self.b_first.config(state=NORMAL)
        self.b_prev.config(state=NORMAL)
        self.b_next.config(state=NORMAL)
        self.b_last.config(state=NORMAL)


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()

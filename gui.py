import subprocess as sub
from tkinter import *
from tkinter.ttk import *


class Gui(Tk):
    def __init__(self):
        super().__init__()
        self.title("Git Walker")
        self.actual_id = StringVar(value="id: ")
        self.steps = IntVar(value=1)
        self.resizable(False, False)
        self.commits: list[str] = []
        self.target_id = None

        Label(self, text="Git Walker", font=("", 14)).grid(row=0, column=0, columnspan=2, pady=5)
        Button(self, text="First", command=lambda: self.first()).grid(row=1, column=0, pady=5)
        Button(self, text="Previous", command=lambda: self.previous()).grid(row=2, column=0, pady=5)
        Button(self, text="Next", command=lambda: self.next()).grid(row=2, column=1, pady=5)
        Button(self, text="Last", command=lambda: self.last()).grid(row=1, column=1, pady=5)
        Label(self,text="Steps").grid(row=3,column=0,pady=5)
        Spinbox(self,from_=0,to=20,textvariable=self.steps,wrap=True).grid(row=3,column=1,pady=5)
        Label(self, textvariable=self.actual_id).grid(row=4, column=0, columnspan=2, pady=5)

        self.read_commits_ids()
        self.read_active_commit_id()
        self.current_index = self.commits.index(self.actual_id.get())

    def first(self):
        self.target_id = self.commits[-1]
        self.check()
    def next(self):
        try:
            self.target_id = self.commits[self.current_index - self.steps.get() - 1]
        except IndexError:
            self.target_id = self.commits[0]
        finally:
            self.check()

    def previous(self):
        try:
            self.target_id = self.commits[self.current_index + self.steps.get()]
        except IndexError:
            self.target_id = self.commits[-1]
        finally:
            self.check()

    def last(self):
        self.target_id = self.commits[0]
        self.check()

    def read_commits_ids(self) -> None:
        out = sub.run("git rev-list --all", capture_output=True)
        self.commits = [line.decode("utf-8").strip() for line in out.stdout.split(b'\n')]
        print(self.commits)

    def read_active_commit_id(self) -> None:
        out = sub.run("git rev-parse HEAD", capture_output=True)
        self.actual_id.set(out.stdout.split()[0].decode("utf-8"))

    def check(self):
        sub.run(f"git checkout {self.target_id} --quiet")


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()

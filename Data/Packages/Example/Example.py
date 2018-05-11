import sublime
import sublime_plugin
import os
from subprocess import Popen, PIPE

class Git(object):
	"""docstring for Git"""
	def __init__(self):
		settings = sublime.load_settings("Example.sublime-settings")
		self.path=settings.get('path')
		self.log=[]

	def cmd(self,args):
		p=Popen(args=args,shell=True,stdout=PIPE)	
		self.log.append(p.stdout.read().decode('utf-8'))
		p.communicate()	

	def phase(self,args):
		os.chdir(self.path)
		for arg in args:
			self.cmd(arg)


	def gitpush(self,origin='origin',branch='dev'):
		args=['git status','git add .','git commit -m "auto"','git push %s %s'%(origin,branch)]
		self.phase(args)	
	
	def gitlog(self):
		self.phase(['git log'])

	def gitstatus(self):
		self.phase(['git status'])
	
	# def __getattr__(self,item):


def done(edit,str1):
	a=Git()
	if str1=='gitlog':
		a.gitlog()
	elif str1=='gitstatus':
		a.gitstatus()
	elif str1=='gitpush':
		a.gitpush()

	output="".join(a.log)
	syntax="Packages/Python/Python.sublime-syntax"
	window=sublime.active_window()
	v1=window.create_output_panel(str1)
	v1.set_syntax_file(syntax)
	window.run_command("show_panel", {"panel": "output.%s"%str1})

	v1.set_read_only(False)	
	v1.insert(edit, 0, output)
	v1.run_command("move_to", {"to": "eol", "extend": False})	

class ShowStatusCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		done(edit, "gitstatus")

class ShowLogCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		done(edit, "gitlog")
		

class AutoPushGitCommand(sublime_plugin.TextCommand):
	def run(self,edit):	
		done(edit, "gitpush")


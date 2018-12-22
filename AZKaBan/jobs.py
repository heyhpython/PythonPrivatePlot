from azkaban import Job, Project

project = Project('foo')
project.add_file('./jobs.py', 'jobs.py')
project.add_job('bar', Job({'type': 'command', 'command':'cat jobs.py'}))

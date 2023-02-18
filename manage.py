import subprocess

# run all sql files in sql folder
subprocess.run(['python', 'sql/createdb.py'])
subprocess.run(['python', 'sql/insert_data.py'])
subprocess.run(['python', 'sql/get_data.py'])

# run all python files in application folder
subprocess.run(['python', 'application.py'])

print("Auto run all files was triggered successfully")

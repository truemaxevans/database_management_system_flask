# this file is used to run all files

import os

# run all sql files in sql folder
os.system("python sql\createdb.py")
os.system("python sql\insert_sql.py")
os.system("python sql\get_data_sql.py")

# run all python files in application folder
os.system("python application.py")

print("Auto run all files was triggered successfully")

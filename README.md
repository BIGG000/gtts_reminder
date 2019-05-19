# alarmPop #

Simple Alarm/ToDo/Reminder App using native notify-send library and python
libraries!

### Dependencies ###

* Python2 or Python3(if you can fix shelve gdbm error)
* mpg321
* notify-osd (Normally pre-installed on Ubuntu)
* gTTS (Google Text to Speech API) for Python. (optional, if you want to your message to be spoken out loud.)

### How to use? ###
1. Clone the repository.  
2. Change file attribute to executable. `chmod a+x alarmPop.py`
3. To set an alarm:  
    * `~$ ./alarmPop.py 20:05`  
    Just type in the script name followed by the time in 24hrs format(HH:mm).
4. To set a reminder:
    * `~$ ./alarmPop.py 20:05 -m "Hello World!"`  
    Type in the script name followed by time and `-m` stands for message to be shown.
5. To set a speaking reminder:
    * `~$ ./alarmPop.py 20:05 -m "Hello World!" -s`  
    Type the script name followed by time, and message after positional argument `-m` and ending with another positional argument `-s` to set speak flag as `True`
6. To delete alarm/reminder:
    * `~$ ./alarmPop.py -e`  
    It will list all set alarms and will interactively ask to delete alarm by index. 
7. To auto start the script at startup, follow the steps below,
    * Open `Startup Application Preferences` on Ubuntu.  
    * Click on `Add`  
    * Type `alarmPop` in column `Name`  
    * Type `/bin/bash -c "sleep 15 && cd /path/to/dir/alarmPop/; ./alarmPop.py >> /path/to/dir/alarmPop/out.txt"` in column `Command`.
You may also try `cron` or any other tool which run the script at startup.
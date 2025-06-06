The game CDDA allows you to write diaries so you can record the progress of your character.  However they are big ugly text files.
This is an attmept to be able to easily convert those text files into a collection of images.  They are formatted in such a way
that they should be postable to Reddit. (Though there is a max of 20 images at a time.)  It is not remotely perfect.  The 
inconsistant text sizes make images that scale well at Reddit hard.  And breaking those into better sized chunks Runs into the 
issue of only 20 pictures per post on reddit.

But... it works.  more or less

Requires the pillow python library.

It also makes the assumptions that you always start your Diary text with a tag ("Diary:", though that can be modified with a command
line flag).  I was unable to automatically figure out where that text started, largley due to the generally chaotic nature of that
text file, and the more specifically chaotic nature of the quest entries (other entries at least don't seem to add spurious line
breaks).  But just make the first line of every Diary entry:
Diary:
and the script should work.

Usage
./Diary_Script.py -h
shows options, but most likely you will simply run:
./Diary_Script.py <Diary Text File>


Unfortunately, long diary entries get unwieldy.  Especially if the left side data (stats, missions, kills, etc) and the right side
data (the part you type in) are wildly different.  So I created a '--format_style' option.  The default simply leaves the left
and right sides alone.  The value 'trunc_long_side' will truncate (cut off) the longer side at about the length of the shorter side.
The value 'wrap_long_side' will create a 'continued' section, such that both sides end up approximately the same length.

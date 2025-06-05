The game CDDA allows you to write diaries so you can record the progress of your character.  However they are big ugly text files.
This is an attmept to be able to easily convert those text files into a collection of images.  They are formatted in such a way
that they should be postable to Reddit. (Though only 10 entries at a time, as this creates two images per entry due to the ugly
data.)  It is not remotely perfect.  The inconsistant text sizes make images that scale well at Reddit hard.  And breaking those
into better sized chunks Runs into the issue of only 20 pictures per post on reddit.

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

# Dead as Disco: Discord Rich Presence
Installation:

Extract the ZIP file and place it in a folder of your choice.

Usage:

Discord must be open. (I mean why would you want a Discord Rich Presence without having discord active?)

- Option 1:
1. Launch DeadAsDiscoPresence.exe.
2. Launch Dead as Disco. 
That’s it.

- Option 2:
Go to your Dead as Disco Steam properties (Steam library -> right click "Dead as Disco" -> Properties
And add the ENTIRE following line:

cmd /c start "" "YOUR INSTALLATION PATH\DeadAsDiscoPresence.exe" & start "" %command% 


This will add an auto start for the Discord Rich Present to your gamestart.

For both options: Discord rich presence will be active as long as the game remains open.
The program will close itself after closing Dead as Disco.
For more informations, and maybe troubleshooting, there's a presence_log.txt file which contains informations about that.



=== Adding missing/new songs: ===

Custom songs work fine, the problem are the game's own songs and boss fights (which aren't properly named in the log file.
For that you need to open the songs.json file and your Pagoda.log (located in \AppData\Local\Pagoda\Saved\Logs).
There you can search for the "OnSongStartedEvent, song asset" event, the text afterwards should look something like that which is already added in the songs.json file.
This text needs to be added to the songs.json file, from there you follow the same structure by filling out the right artist - songname.

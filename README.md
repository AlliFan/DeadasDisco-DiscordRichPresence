# Dead as Disco: Discord Rich Presence
<img width="260" height="74" alt="ezgif-85d61f7c30e927a4" src="https://github.com/user-attachments/assets/60dcfc0c-e395-4fdf-b4af-f67d499722de" />

## <ins>Installation:</ins>

[Download](https://github.com/AlliFan/DeadasDisco-DiscordRichPresence/releases/tag/Release) the latest ZIP file and extract it in a folder of your choice.

> [!NOTE]
> Windows Defender might briefly report "Trojan:Win32/Wacatac.B!ml". This is a known false positive for Python-based tools (2/71 on VirusTotal, no behavioral hits) – [VirusTotal scan here](https://www.virustotal.com/gui/file/6a89a96e5992fc33ac8cd011332d99d58e192a7139de1ee67d4d4d341a3ec2eb?nocache=1).

This is now fixed after microsoft reviewing the program. You can still get the warning if your Windows Defender isn't updated yet.

## <ins>Usage:</ins>

Discord must be open. (I mean why would you want a Discord Rich Presence without having discord active?)

### **- Option 1:**
1. Launch DeadAsDiscoPresence.exe.
2. Launch Dead as Disco. 
That’s it.

### **- Option 2:**

Go to your Dead as Disco Steam properties (Steam library -> right click "Dead as Disco" -> Properties
And add the ENTIRE following line:

`cmd /c start "" "YOUR INSTALLATION PATH\DeadAsDiscoPresence.exe" & start "" %command%`


This will add an auto start for the Discord Rich Present to your gamestart.
After this you can just start the game via steam.

## <ins>Information for both options:</ins>

There's a short moment where the windows console will appear. This can't really be changed, see it as an check to confirm that the program is successfully running.

Discord rich presence will be active as long as the game remains open.
The program will close itself after closing Dead as Disco.
For more informations, and maybe troubleshooting, there's a presence_log.txt file which contains informations about that.



## <ins>Adding missing/new songs:</ins>

Custom songs work fine, the problem are the game's own songs and boss fights (which aren't properly named in the log file.
For that you need to open the songs.json file and your Pagoda.log (located in \AppData\Local\Pagoda\Saved\Logs).
There you can search for the "OnSongStartedEvent, song asset" event, the text afterwards should look something like that which is already added in the songs.json file.
This text needs to be added to the songs.json file, from there you follow the same structure by filling out the right artist - songname.


 ## <ins>To do, sorta</ins>

- adding tracking for all the base songs from the game
- maybe find out how to add stuff like score, current/full song length or even beats count.

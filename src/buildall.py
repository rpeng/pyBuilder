"""
	Builds everything. 
"""

import os
import shutil
import subprocess as sub

ANTDIR = "C:/ant/bin/"

projects = {
    "canoe":"canoe",
    "24h":"24h",
    "winnipegsun":"winnsun",
    "torontosun":"torsun",
    "ottawasun":"ottsun",
    "journaldemontreal":"jdem",
    "journaldequebec":"jdeq",
    "londonfreepress":"lfp",
    "edmontonsun":"edmsun",
    "calgarysun":"calsun"
}

builds = [
    "hightouch",
    "veryhigh",
    "high",
    "touch",
    "low"
]    

    
for p in projects.keys():
    for b in builds:
        z = sub.Popen(['ant','-lib','build/lib','-Dapplication='+p,'-Ddevice='+b,'manualota'], stdout=sub.PIPE, stderr=sub.STDOUT, shell=True)
        while True:
            line = z.stdout.readline()
            if line != '':
                print line.rstrip()
            else:
                break


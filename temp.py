import json
import sys

from general_elections.views import *
fname= sys.argv[1]#'Barak_room_roll.json'
f=open(fname,'r')
roll_dic = json.load(f)
for roll in roll_dic:
    #print(roll)
    try:
        u = VoterList.objects.get(roll_no=roll)
        if u.hostel=='NA':
            u.hostel = 'Married Scholars'
            u.save()
            print(u.roll_no)
        else:
            print(u.roll_no, u.hostel)
    except: 
        pass

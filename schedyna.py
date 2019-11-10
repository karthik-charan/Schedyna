from django.http import JsonResponse
from django.core import serializers
from hk.model import hk

def reschd(request,task_id=None,reach=0):
	if task_id == None:
		return JsonResponse({"Success":Your code works fine! Select a task},status = 200)
	else:
		id = task_id
		tc = reach
		sdiff=[]
		ind=[]
		avail=[]
		estrt = []
		eend = []
		sstrt = []
		send = []
		#Computing the number of records
		tot = hk.count()
		#initializing
		for i in range(0,tot+1):
			sdiff.append(0)
			ind.append(0)
			avail.append(0)
			estrt.append(0)
			eend.append(0)
			sstrt.append(0)
			send.append(0)

		#assigning the fields as lists
		es = serialize.serialize("json",hk.objects.only('eventstart'))
		ee = serialize.serialize("json",hk.objects.only('eventend'))
		ss = serialize.serialize("json",hk.objects.only('speakerstart'))
		se = serialize.serialize("json",hk.objects.only('speakerend'))
		#fetching start and end of event to be rescheduled
		estr = es[id]
		end = ee[id]
		#converting string time into integer
		for i in range(id+1,tot+1):
			estrt[i] = float(es[i])
			eend [i] = float(ee[i])
			sstrt[i] = float(ss[i])
			send [i] = float(se[i])
		#computing the most busy person
		for i in range(id+1,tot+1):
			sdiff[i] = send[i]-sstrt[i]
		#sorting people according to their free time
		k = 0
		for i in range(0,tot+1):
			for j in range(i+1,tot+1):
				if sdiff[i]>sdiff[j]:
					temp = sdiff[i]
					sdiff[i] = sdiff[j]
					sdiff[j] = temp
					ind[k] = i
					k = k+1
		#checking whether the most busy person is free during the schedule
		k = 0
		for i in range(id+1,tot+1):
			if estr>=sstrt[i] && end<=send[i]:
				avail[k] = i
				k = k+1
		#computing the most efficient scheduling.spl is the most apt person
		for i in range(id+1,tot+1):
			for j in range(i,tot+1):
				if ind[i]==avail[j]:
					spl = avail[j]
					
		#reordering the events list
		prev = hk.objects.get(id=id)
		new = hk.objects.get(id=spl)
		dum = prev
		#updating the reschedule event
		prev.id = new.id
		prev.event = new.event
		prev.speaker = new.speaker
		prev.eventstart = new.eventstart
		prev.eventend = new.eventend
		prev.speakerstart = new.speakerstart
		prev.speakerend = new.speakerend
		prev.save()
		#updating the delayed event
		new.id = dum.id
		new.event = dum.event
		new.speaker = dum.speaker
		new.eventstart = dum.eventstart
		new.eventend = dum.eventend
		new.speakerstart = dum.speakerstart
		new.speakerend = dum.speakerend
		new.save()
		"""reach time verification
		if tc!=None:
			if estrt[spl]<tc:

			else:
				break"""
		#done with the rescheduling.Alert the Event Handler
		return JsonResponse({"success":Updated your event to the most efficient Schedule },status = 200)


import pickle, multiprocessing
from threading import Thread
from general_elections.models import *
import bcrypt
import sys
import os
import time


def get_result_process(start, end):
    
    # start_index , end_index
	# UG VOTES
	temp = dict()
	all_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc', 
						'ugs', 'gs', 'pgs']
	single_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc']
	
	for cat in all_categories:
		temp[cat] = dict()
		conts = Contestants.objects.filter(post=cat.upper())
		for c in conts:
			temp[cat][c.webmail_id] = 0
	
	UGlist = VotesUG.objects.all()
	"""
	n = len(UGlist)
	print(index)
	start = index*int(n/nthreads)
	end = (index+1)*int(n/nthreads)
	if index == nthreads-1:
		end = n
    	"""
	for ii, vote in enumerate(UGlist[start:end],start):
		print('Processing UG vote: ',ii)
		#vote = UGlist[ii]
		# single choice votes
		for cat in single_categories:
			conts = Contestants.objects.filter(post=cat.upper())
			vv = getattr(vote, cat)
			# compare against all contestants
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp[cat][c.webmail_id] += 1
					break
				else:
					continue
		# UGS
		conts = Contestants.objects.filter(post='UGS')
		cols = ['ugs_1', 'ugs_2', 'ugs_3', 'ugs_4', 'ugs_5', 'ugs_6', 'ugs_7']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['ugs'][c.webmail_id] += 1
					break
				else:
					continue

		# GS
		conts = Contestants.objects.filter(post='GS')
		cols = ['gs_1', 'gs_2', 'gs_3']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['gs'][c.webmail_id] += 1
					break
				else:
					continue

	PGlist = VotesPG.objects.all()
	# n = len(PGlist)
	# start = index*int(n/nthreads)
	# end = (index+1)*int(n/nthreads)
	# if index == nthreads-1:
	# 	end = n
	for ii,vote  in enumerate(PGlist[start: end],start):
		print('Processing PG votes :', ii)
		#vote = PGlist[ii]
		# single choice votes
		for cat in single_categories:
			conts = Contestants.objects.filter(post=cat.upper())
			vv = getattr(vote, cat)
			# compare against all contestants
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp[cat][c.webmail_id] += 1
					break
				else:
					continue
		# PGS
		conts = Contestants.objects.filter(post='PGS')
		cols = ['pgs_1', 'pgs_2', 'pgs_3', 'pgs_4', 'pgs_5', 'pgs_6', 'pgs_7']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['pgs'][c.webmail_id] += 1
					break
				else:
					continue

		# GS
		conts = Contestants.objects.filter(post='GS')
		cols = ['gs_1', 'gs_2', 'gs_3']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['gs'][c.webmail_id] += 1
					break
				else:
					continue

	return(temp)


def get_result2(results, index, nthreads):

	# UG VOTES
	temp = dict()
	all_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc', 
						'ugs', 'gs', 'pgs']
	single_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc']
	
	for cat in all_categories:
		temp[cat] = dict()
		conts = Contestants.objects.filter(post=cat.upper())
		for c in conts:
			temp[cat][c.webmail_id] = 0
	
	UGlist = VotesUG.objects.all()
	n = len(UGlist)
	print(index)
	start = index*int(n/nthreads)
	end = (index+1)*int(n/nthreads)
	if index == nthreads-1:
		end = n

	for ii in range(start, end):
		vote = UGlist[ii]
		# single choice votes
		for cat in single_categories:
			conts = Contestants.objects.filter(post=cat.upper())
			vv = getattr(vote, cat)
			# compare against all contestants
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp[cat][c.webmail_id] += 1
					break
				else:
					continue
		# UGS
		conts = Contestants.objects.filter(post='UGS')
		cols = ['ugs_1', 'ugs_2', 'ugs_3', 'ugs_4', 'ugs_5', 'ugs_6', 'ugs_7']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['ugs'][c.webmail_id] += 1
					break
				else:
					continue

		# GS
		conts = Contestants.objects.filter(post='GS')
		cols = ['gs_1', 'gs_2', 'gs_3']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['gs'][c.webmail_id] += 1
					break
				else:
					continue

	PGlist = VotesPG.objects.all()
	n = len(PGlist)
	start = index*int(n/nthreads)
	end = (index+1)*int(n/nthreads)
	if index == nthreads-1:
		end = n
	for ii in range(start, end):
		vote = PGlist[ii]
		# single choice votes
		for cat in single_categories:
			conts = Contestants.objects.filter(post=cat.upper())
			vv = getattr(vote, cat)
			# compare against all contestants
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp[cat][c.webmail_id] += 1
					break
				else:
					continue
		# PGS
		conts = Contestants.objects.filter(post='PGS')
		cols = ['pgs_1', 'pgs_2', 'pgs_3', 'pgs_4', 'pgs_5', 'pgs_6', 'pgs_7']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['pgs'][c.webmail_id] += 1
					break
				else:
					continue

		# GS
		conts = Contestants.objects.filter(post='GS')
		cols = ['gs_1', 'gs_2', 'gs_3']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['gs'][c.webmail_id] += 1
					break
				else:
					continue
	print(index)
	results[index] = temp


t1 = time.time()
result_dir = 'temp_results'
start = int(sys.argv[1])
end = int(sys.argv[2])
try:
	os.makedirs(result_dir)
except:
	pass

results_dict = get_result_process(start, end)
name = 'temp_results/results_{0}_{1}.pkl'.format(start,end)
output = open(name, 'wb')
pickle.dump(results_dict, output)
output.close()
print('Result saved')
t2= time.time()
print('time taken : ' , (t2-t1))

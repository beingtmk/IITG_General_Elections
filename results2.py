import pickle, multiprocessing
from threading import Thread
from general_elections.models import *
import bcrypt
import time



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
		print(' Process no {0}, UG vote : {1}'.format(index,ii))
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
		print(' Process no {0}, PG vote : {1}'.format(index,ii))
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
	results.put(temp)

def combine_results(results):
	results_dict = dict()
	all_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc', 
						'ugs', 'gs', 'pgs']
	single_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc']
	
	for cat in all_categories:
		results_dict[cat] = dict()
		conts = Contestants.objects.filter(post=cat.upper())
		for c in conts:
			results_dict[cat][c.webmail_id] = 0
			for temp in results:
				results_dict[cat][c.webmail_id] += temp[cat][c.webmail_id]
	return results_dict

try:
	pkl_file = open('results.pkl', 'rb')
	results_dict = pickle.load(pkl_file)
	print('Read pickle')
except:
	t1 = time.time()
	results = multiprocessing.Queue()
	n_processes = 30
	processes = [multiprocessing.Process(target=get_result2, args=(results, x, n_processes)) for x in range(n_processes)]
	for p in processes:
		p.start()
	for p in processes:
		p.join()

	results = [results.get() for p in processes]
	results_dict = combine_results(results)
	t2 = time.time()
	print('time taken :' ,(t2-t1))
	try:
		output = open('results.pkl', 'wb')
		pickle.dump(results_dict, output)
		output.close()
		print('Result saved')
	except:
		pass


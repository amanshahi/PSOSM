import json

pre_final = json.load(open('pre_final.json'))
final = json.load(open('final.json'))
data = json.load(open('data.json'))
order = json.load(open('order_profile.json'))
names = open('names').read().split('\n')

def get_response(input_name):
	if input_name in names:
		for i in data:
			if data[i][0][0] == input_name:
				temp = data[i]
		profile = temp[0][0]
		fb = temp[2]
		linkedin = temp[1]
		if len(fb) > 1:
			ind, mx, g = -1, -1, 0
			for i in pre_final[profile]:
				cum = sum(i)
				if cum > mx:
					mx = cum
					ind = g
				g+=1
			jobs = open('./Privacy Data/Linkedin_data/' + profile).read().split('\n')
			temp = []
			for i in xrange(len(jobs)):
				if len(jobs[i]) == 0: continue
				temp.append((jobs[i], final[profile][ind][i]))
			return profile, linkedin[0], fb[order[profile][ind]], temp
		else:
			jobs = open('./Privacy Data/Linkedin_data/' + profile).read().split('\n')
			temp = []
			for i in xrange(len(jobs)):
				if len(jobs[i]) == 0: continue
				temp.append((jobs[i], final[profile][0][i]))
			return profile, linkedin[0], fb[0], temp
	else:
		return 'Not a valid name, please refer the name file and select a valid name.'
		#Raise an error in this case

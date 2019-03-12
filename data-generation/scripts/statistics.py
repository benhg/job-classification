from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

a2014_male_sample=[['6.05', '6:28', '10:07', '9:36', '6:50', '7:55', '7:31', '6.03', '8:25', '10:22'] , ['6:32', '6:40', '6:14', '7:32', '8:49', '7:54', '8:13', '6:21', '6:40', '7:53'], ['5:20', '8.08', '12:47', '8:42', '6:39', '6:03', '8:42', '6:02', '6.54' , '6:22']]
a2014_female_sample=[['9.57', '6.57', '8.58', '10:29', '9:30', '9.57', '8:45', '11.11', '9:13', '10:55'], ['9:02', '9:02', '7:38', '6:13', '6:03', '9:02', '8:14', '8:50', '8:50', '8:50'], ['8:57', '10:20', '8:20', '10:58', '13:07', '8:28', '7:20', '7:30', '7:10', '11:27']]
a2015_male_sample=[['7:25', '7:33', '6:30', '6:35', '6:35', '6:59', '7:42', '9:43', '7:18', '8:26'], ['7:50', '6.49', '6.12', '6.4', '6.45', '7:50', '7.32', '6:00', '8:10', '5:44'], ['6:22', '7:27', '8:02', '12.5', '6.34', '8:23', '7:53', '6.26', '7:53', '8:23']]
a2015_female_sample=[['9:28', '8:36', '9:28', '9:40', '7:36', '10:22', '7:48', '7:40', '10:22', '10:31'], ['9:05', '11:40', '8.38', '9.15', '7:35', '6.58', '9:10', '7:35', '9:35', '10.45'], ['10:30', '8:26', '8:50', '7:30', '9:16', '7:09', '9:12', '10:00', '8:35', '8:35']]
dirtysamplelist=[]
dirtysamplelist.append(a2014_male_sample)
dirtysamplelist.append(a2014_female_sample)
dirtysamplelist.append(a2015_male_sample)
dirtysamplelist.append(a2015_female_sample)

cleansamplelist=[]
for sample in dirtysamplelist:
	list=[]
	print list
	for subsample in sample:
		for run in subsample:
			print run
			if ":" in run:
				list.append((int(run.split(":")[0])*60)+(int(run.split(":")[1])))
				print int(run.split(":")[1])
			elif "." in run:
				list.append((int(run.split(".")[0])*60)+(int(run.split(".")[1])))
	cleansamplelist.append(list)

a2014_male_sample=cleansamplelist[0]
a2014_female_sample=cleansamplelist[1]
a2015_male_sample=cleansamplelist[2]
a2015_female_sample=cleansamplelist[3]
all_2014_sample=a2014_male_sample+a2014_female_sample
all_2015_sample=a2015_male_sample+a2015_female_sample
all_female=a2015_female_sample+a2014_female_sample
all_male=a2014_male_sample+a2015_male_sample
all_sample=all_female+all_male



#do some plots a lot of them please
plots_to_be_made=[a2014_male_sample,a2014_female_sample,a2015_male_sample,a2015_female_sample,all_2014_sample,all_2015_sample, all_female, all_male, all_sample]
plot_titles=["2014 Males","2014 Females","2015 Males","2015 Females","All 2014","All 2015", "All Females", "All Males", "All Runners"]

for index, plot in enumerate(plots_to_be_made):
	plt.hist(plot)
	plt.title(plot_titles[index])
	plt.show()


#95% confidence intervals for all of the means
file=open("conf_interval_out.txt","w")
i=0
for dataset in plots_to_be_made:
	mean,sigma=np.mean(dataset), np.std(dataset)
	t_bounds=stats.t.interval(0.95, len(dataset)-1)
	ci=[mean + critval * (sigma/sqrt(len(dataset))) for critval in t_bounds]
	print ci
	file.write("%s:%s-%s. Sampmean:%s StdDev:%s"%(plot_titles[i],ci[0],ci[1], mean, sigma)+"\n")
	i+=1
file.close()

#do some statistics please(t tests)
file=open("statistcs_out.txt", "w")
i=0
for dataset in plots_to_be_made:
	j=0
	for dataset2 in plots_to_be_made: 
		tteststat=stats.ttest_ind(dataset,dataset2)
		file.write("%s>%s:%s"%(plot_titles[i],plot_titles[j],tteststat)+"\n")
		j+=1
	i+=1
file.close()

plots_to_be_made_male=[a2014_male_sample, a2015_male_sample, all_male, all_2014_sample, all_2015_sample, all_female, all_sample]
plots_to_be_made_female=[a2014_female_sample, a2015_female_sample, all_female, all_2014_sample, all_2015_sample, all_male, all_sample]
#Now 1 sample t tests:
male_national_average=(430)
female_national_average=(631)
plot_titles_male=["Males in 2014", "Males in 2015", "All Males", "All 2014 Runners", "All 2015 Runners", "All Females", "All Runners"]
plot_titles_female=["Females in 2014", "Females in 2015", "All Females", "All 2014 Runners", "All 2015 Runners", "All Males", "All Runners"]

file=open("1samp.txt","w")
i=0
for dataset in plots_to_be_made_male:
	file.write("%s>National Average (male):%s"%(plot_titles_male[i], stats.ttest_1samp(np.array(dataset),male_national_average))+"\n")
	i+=1
i=0
for dataset in plots_to_be_made_female:
	print i
	file.write("%s>National Average (female):%s"%(plot_titles_female[i], stats.ttest_1samp(np.array(dataset),female_national_average))+"\n")
	i+=1
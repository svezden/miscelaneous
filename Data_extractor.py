## This is an script to obtain data from files within a directory with a '.log' extension. It looks for the keyword 'SCF Done'
## and extracts the energy of that line, corresponding to the 4th string in that line.
## FInally the script prints into summary the result sorted by name of file. 

from operator import itemgetter
import os

#This define the directory from where to take the files
directory = "/home/raul/Dropbox/Projects Cambridge/Python games/Fernanda_data_extractor/"

X = []
#This subroutine reads all files in the directory with extension .log
#and looks for the keyword that contains the keyword "SCF Done"
for filename in os.listdir(directory):
    if filename.endswith(".log"): 
        with open (filename,'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.find("SCF Done")!= -1:
                   X.append((filename[:-4],float(line.split()[4])))

#This orders the array with respect to the first element in each subarray
X = sorted(X,key=itemgetter(1))

#Here we print the data in the file Summary.dat
with open ("Summary.dat",'w') as summary:
    for elem in range(0,int(len(X)-1),3): 
        summary.write("%s: %s, %s: %s, %s: %s\n" % (X[elem][0],X[elem][1],X[elem+1][0],X[elem+1][1],X[elem+2][0],X[elem+2][1]))                      

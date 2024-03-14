from vlpi.data.ClinicalDataset import ClinicalDataset,ClinicalDatasetSampler
from vlpi.data.ClinicalDataSimulator import ClinicalDataSimulator
from vlpi.vLPI import vLPI
import torch
import string
import numpy as np

seed=torch.manual_seed(1023)

numberOfSamples=50000
numberOfSymptoms=20

rareDiseaseFrequency=0.001
numLatentPhenotypes=2
simulator = ClinicalDataSimulator(numberOfSymptoms,numLatentPhenotypes,rareDiseaseFrequency,numCatList=[2,3,4])
simulatedData=simulator.GenerateClinicalData(numberOfSamples)
symptomConversionMap=dict(zip(string.ascii_uppercase[0:numberOfSymptoms],range(0,numberOfSymptoms)))
symptomConversionMapInv=dict(zip(range(0,numberOfSymptoms),string.ascii_uppercase[0:numberOfSymptoms]))
simulatedIndex = list([str(i) for i in range(numberOfSamples)])
np.random.shuffle(simulatedIndex)


### write simulated data to file ###
f1=open('SimDxFile_NoCovariates.txt','w')
f2=open('SimDxFile_WithCovariates.txt','w')
f1.write('p_id\tdx\n')
f2.write('p_id\tc1\tc2\tc3\tdx\n')
for i in range(numberOfSamples):
	f1.write('{0:s}\t{1:s}\n'.format(simulatedIndex[i],','.join([symptomConversionMapInv[int(s)] for s in torch.where(simulatedData['incidence_data'][i])[0]])))
	f2.write('{0:s}\t{1:d}\t{2:d}\t{3:d}\t{4:s}\n'.format(simulatedIndex[i],int(simulatedData['covariate_data'][0][i]),int(simulatedData['covariate_data'][1][i]),int(simulatedData['covariate_data'][2][i]),','.join([symptomConversionMapInv[int(s)] for s in torch.where(simulatedData['incidence_data'][i])[0]])))
f1.close()
f2.close()


## load the data into a ClinicalDataset class
clinicalData = ClinicalDataset(symptomConversionMap)
# clinicalData.ReadDatasetFromFile('SimDxFile_NoCovariates.txt',1,indexColumn=0)
clinicalData.ReadDatasetFromFile('SimDxFile_WithCovariates.txt',4,indexColumn=0)
# clinicalData.LoadFromArrays(simulatedData['incidence_data'],subjectIDs=simulatedIndex,covariateArrays=dict(zip(['c1','c2','c3'],simulatedData['covariate_data'])))

# #change the dataset to have only 20 symptoms (defaults to full ICD10-CM codebook), named after the first 20 letters

# # now load into the data structure. Note, when using in this manner, it's the users responsibility to make sure that the input data columns match the data columns of the ClinicalDataset.
# clinicalData.LoadFromArrays(simulatedData['incidence_data'],simulatedData['covariate_data'],[],catCovDicts=None, arrayType = 'Torch')

# ## Now load the ClincalDataset into ClinicalDatasetSampler
training_data_fraction=0.75
sampler = ClinicalDatasetSampler(clinicalData,training_data_fraction,returnArrays='Torch')

# ## Intantation the models
infNumberOfLatentPhenotypes=10
vlpiModel= vLPI(sampler,infNumberOfLatentPhenotypes)

inference_output = vlpiModel.FitModel(batch_size=1000,errorTol=(1.0/numberOfSamples))
# vlpiModel.PackageModel('ExampleModel.pth')

# inferredCrypticPhenotypes=vlpiModel.ComputeEmbeddings((simulatedData['incidence_data'],simulatedData['covariate_data']))
# riskFunction=vlpiModel.ReturnComponents()

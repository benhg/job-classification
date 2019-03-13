"""
genderPredictor.py
"""

from nltk import NaiveBayesClassifier,classify
import USSSALoader
import random

class genderPredictor():
    
    def getFeatures(self):
        maleNames,femaleNames=self._loadNames()
        
        featureset = []
        
        for nameTuple in maleNames:
            features = self._nameFeatures(nameTuple[0])
            male_prob, female_prob = self._getProbDistr(nameTuple)
            features['male_prob'] = male_prob
            features['female_prob'] = female_prob
            featureset.append((features,'M'))
        
        for nameTuple in femaleNames:
            features = self._nameFeatures(nameTuple[0])
            male_prob, female_prob = self._getProbDistr(nameTuple)
            features['male_prob'] = male_prob
            features['female_prob'] = female_prob
            featureset.append((features,'F'))
    
        return featureset
    
    def trainAndTest(self,trainingPercent=0.99):
        featureset = self.getFeatures()
        random.shuffle(featureset)
        
        name_count = len(featureset)
        
        cut_point=int(name_count*trainingPercent)
        
        train_set = featureset[:cut_point]
        test_set  = featureset[cut_point:]
        
        self.train(train_set)
        
        return self.test(test_set)
        
    def classify(self,name):
        feats=self._nameFeatures(name)
        return self.classifier.classify(feats)
        
    def train(self,train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier
        
    def test(self,test_set):
       return classify.accuracy(self.classifier,test_set)
    
    def _getProbDistr(self,nameTuple):
            male_prob = (nameTuple[1] * 1.0) / (nameTuple[1] + nameTuple[2])
            if male_prob == 1.0:
                male_prob = 0.99
            elif male_prob == 0.0:
                male_prob = 0.01
            else:
                pass
            female_prob = 1.0 - male_prob
            return (male_prob, female_prob)
        
    def getMostInformativeFeatures(self,n=10):
        return self.classifier.most_informative_features(n)
        
    def _loadNames(self):
        return USSSALoader.getNameList()
        
    def _nameFeatures(self,name):
        name=name.upper()
        return {
            'last_letter': name[-1],
            'last_two' : name[-2:],
            'last_three': name[-3:],
            'last_is_vowel' : (name[-1] in 'AEIOUY')
        }


gp = genderPredictor()
accuracy=gp.trainAndTest()
print('Accuracy: %f'%accuracy)
print('Most Informative Features')
feats=gp.getMostInformativeFeatures(10)
for feat in feats:
    print('\t%s = %s'%feat)
name = input('Enter name to classify: ')
gender=gp.classify(name)

# file=open('classified', "a")
# for name in failed:
#     name=name.strip()
#     firstName=name.split(' ')[0].strip()
#     gender=gp.classify(firstName)
#     print '\n%s is classified as %s'%(name, gp.classify(firstName))
print(('%s | %s\n'%(name,gender)))

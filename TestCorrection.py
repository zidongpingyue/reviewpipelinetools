from SentenceCorrection import SentenceCorrector
from TestData import testcorrectlongtext
stn_corrector=SentenceCorrector()
result=stn_corrector.sentencecorrect(testcorrectlongtext)
print(result)
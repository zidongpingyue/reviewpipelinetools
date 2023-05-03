from DocCorrection import DocCorrector
from ImgDetection import ImageDetector
from SentenceCorrection import SentenceCorrector
from TextJudge_V0 import TextJudger
class UtilModels:
    def __init__(self) -> None:
        self._DocRectify=None
        self._ImgAchorAndCharaDetection=None
        self._SentenceCorrection=None
        self._SentenceMatch=None
        pass
    @property
    def DocRectify(self)->DocCorrector:
        if self._DocRectify==None:
            self._DocRectify=DocCorrector()
        return self._DocRectify
    @property
    def ImgAchorAndCharaDetection(self)->ImageDetector:
        if self._ImgAchorAndCharaDetection==None:
            self._ImgAchorAndCharaDetection=ImageDetector()
        return self._ImgAchorAndCharaDetection
    @property
    def SentenceCorrection(self)->SentenceCorrector:
        if self._SentenceCorrection==None:
            self._SentenceCorrection=SentenceCorrector()
        return self._SentenceCorrection;
    @property
    def SentenceMatch(self)->TextJudger:
        if self._SentenceMatch==None:
            self._SentenceMatch=TextJudger()
        return self._SentenceMatch

utilmodels=UtilModels()
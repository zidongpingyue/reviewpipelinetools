
import sys
from PyQt5.QtWidgets \
import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel,QLineEdit
from TextJudge_V0 import TextJudger
import TestData 
class SentenceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.textjudger=TextJudger()

    def initUI(self):
        # 创建布局
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox2= QVBoxLayout()

        # 创建两个富文本框并添加到第一个水平布局中
        self.textbox1 = QTextEdit()
        self.textbox2 = QTextEdit()
        self.textbox3 = QTextEdit()
        
        vbox2.addWidget(self.textbox2)
        vbox2.addWidget(self.textbox3)
        vbox2.setStretch(0,3)
        vbox2.setStretch(1,7)
        
        hbox1.addWidget(self.textbox1)
        hbox1.addLayout(vbox2)
        hbox1.setStretch(0, 7) # 设置第一个文本框占比为60%
        hbox1.setStretch(1, 3) # 设置第二个文本框占比为40%

        # 创建三个按钮并添加到第二个水平布局中
        self.button1 = QPushButton('执行')
        self.button2 = QPushButton('Button 2')
        self.button3 = QPushButton('Button 3')
        hbox2.addWidget(self.button1)
        hbox2.addWidget(self.button2)
        hbox2.addWidget(self.button3)

        # 创建一个标签并添加到垂直布局中
        self.label = QLabel('Label')
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.label)

        # 设置窗口布局
        self.setLayout(vbox)
        
        self.textbox1.setHtml(TestData.testlongtext)
        self.textbox2.setHtml(TestData.testmatchyes)
        self.textbox3.setText("\n".join(["#示例",TestData.testmatchyes,TestData.testmatchno,
                                         "鼓励了世界其他受帝国主义压迫人民的抗争"]))
        self.textbox3.setReadOnly(True)
        
        #按钮执行
        self.button1.clicked.connect(self.UseModel)
    def UseModel(self):
        longsentence=self.textbox1.toPlainText()
        short=self.textbox2.toPlainText()
        self.label.setText("执行中......")
        total_,match_= self.textjudger.CalculateScore(longsentence,short)
        text = self.textbox1.toPlainText()
        ranges = match_
        formatted_text = ''
        last_index = 0
        for label,n, k in ranges:
            formatted_text += text[last_index:n] + '<span style="color:red;">' + text[n:n+k] + '</span>'
            last_index = n + k
        formatted_text += text[last_index:]
        self.textbox1.setHtml(formatted_text)
            
        self.label.setText("执行完成......")
#



from SentenceCorrection import SentenceCorrector
class CorrectSentenceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.corrector=SentenceCorrector()

    def initUI(self):
        # 创建布局
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox2= QVBoxLayout()

        # 创建两个富文本框并添加到第一个水平布局中
        self.textbox1 = QTextEdit()
        self.textbox2 = QTextEdit()
        # self.textbox3 = QTextEdit()
        
        # vbox2.addWidget(self.textbox2)
        # vbox2.addWidget(self.textbox3)
        # vbox2.setStretch(0,3)
        # vbox2.setStretch(1,7)
        
        hbox1.addWidget(self.textbox1)
        hbox1.addWidget(self.textbox2)
        # hbox1.addLayout(vbox2)
        hbox1.setStretch(0, 5) # 设置第一个文本框占比为60%
        hbox1.setStretch(1, 5) # 设置第二个文本框占比为40%

        # 创建三个按钮并添加到第二个水平布局中
        self.button1 = QPushButton('执行')
        self.button2 = QPushButton('Button 2')
        self.button3 = QPushButton('Button 3')
        hbox2.addWidget(self.button1)
        hbox2.addWidget(self.button2)
        hbox2.addWidget(self.button3)

        # 创建一个标签并添加到垂直布局中
        self.label = QLabel('Label')
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.label)

        # 设置窗口布局
        self.setLayout(vbox)
        
        self.textbox1.setHtml(TestData.testcorrectlongtext)
        # self.textbox2.setHtml(TestData.testmatchyes)
        # self.textbox3.setText("\n".join(["#示例",TestData.testmatchyes,TestData.testmatchno,
        #                                  "鼓励了世界其他受帝国主义压迫人民的抗争"]))
        # self.textbox3.setReadOnly(True)
        
        #按钮执行
        self.button1.clicked.connect(self.UseModel)
    def UseModel(self):
        longsentence=self.textbox1.toPlainText()
        short=self.textbox2.toPlainText()
        self.label.setText("执行中......")
        
        
        match_= self.corrector.sentencecorrect(longsentence)
        # text = self.textbox1.toPlainText()
        ranges = match_
        formatted_text = ''
        
        for label,poses in ranges:
            if len(poses)>0:
                last_index = 0
                for w_chara,r_chare,oldpos,n in poses:
                    formatted_text += (label[last_index:n-1] +f'<s><span style="color:red;">{w_chara}</span></s>'+ '<span style="color:blue;">' + label[n-1:n] + '</span>')
                    last_index = n
                    formatted_text += label[last_index:]
                formatted_text += " "
            else:
                formatted_text += label
                
        self.textbox2.setHtml(formatted_text)
            
        self.label.setText("执行完成......")
#


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SentenceWindow()
    
    # window = CorrectSentenceWindow()
    window.show()
    sys.exit(app.exec_())


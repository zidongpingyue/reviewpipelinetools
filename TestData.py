testlongtext="""
它推翻了清王朝在中国的统治，沉重打击了中外反动势力，为中国人民革命斗争的发展开辟了道路。
它结束了统治中国两千多年的封建君主专制制度，建立了中国历史上第一个资产阶级共和国，使民主共和的观念开始深入人心。
它开启了思想进步和民族觉醒的大门，是一场思想解放运动。
它推动了民族资本主义经济的发展，促进了社会风气的改变和人们精神的解放。
它推动了亚洲各国民族解放运动的高涨。
"""
testmatchyes="民主共和深入人心"
testmatchno="推翻了明朝政府"
testcorrectlongtext="""
它推翻了清王朝在中国的统治，沉重打击了中外反动势笠，为中国人民革命斗争的发展开臂了道路。
它结束了统治中国两千多年的封建君主专制志度，建立了中国历史上第一个资产阶级供和国，使民主共和的观念开始深入人心。
它开启了思想进步和民族觉醒的大门，是一场思想解放运动。
它推动了民族资本主义经济的发展，促晋了社会风气的改变和人们精神的解放。
它推动了亚洲各国名族解放运动的高涨。
"""
testcardlayout=dict_={
  "questions":[

      {
          "order":1,
          "type":"subjective",
          "maxwords":500
      },
      {
          "order":2,
          "type":"subjective",
          "maxwords":600
      },
      {
          "order":3,
          "type":"subjective",
          "maxwords":500
      },
      {
          "order":4,
          "type":"subjective",
          "maxwords":1000
      }
   
  ]
}

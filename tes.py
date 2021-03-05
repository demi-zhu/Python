sentence=input("Please input one sentence:")
screen_with=180
text_with=len(sentence)
box_with=text_with+6
left_margin=(screen_with-box_with)//2
print()
print(''*left_margin+'+'+'-'*text_with+'+')
print(''*left_margin+'|'+' '*text_with+    '|')
print(''*left_margin+'|'+    sentence+    '|')
print(''*left_margin+'|'+' '*text_with+    '|')
print(''*left_margin+'+'+'-'*text_with+'+')
print("good")

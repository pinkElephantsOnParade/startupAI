# -*- coding: utf-8 -*-

#-----無愛想なchatbot-----
def communication():
  while 1:
    sentence = raw_input("あなた：")
    if sentence == "q":
        break
    else:
      print "さくら：ふ～ん，それで？"

#-----main-----
if __name__ == "__main__":
  print "さくら：メッセージをどうぞ('q'で終了)"
  communication()
  print "さくら：ばいば～い"

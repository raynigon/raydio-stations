import eyed3

data = eyed3.load("stream.mp3")
print(data.info.bit_rate[1])
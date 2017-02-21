class Song(object):
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print line

    def song_length(self):
        return len(reduce(lambda x, y: x + y, self.lyrics, '').split(' '))

    def add(self):
        return self.lyrics + self.lyrics

def random(myself):
        return 3.14159265358979323846264338327950

happy_bday = Song(["Happy birthday to you",
                    "I don't want to get sued",
                    "So I'll stop right there"])

bulls_on_parade = Song(["They rally around tha family",
                        "With pockets full of shell"])

happy_bday.sing_me_a_song()
print happy_bday.song_length()

bulls_on_parade.sing_me_a_song()
print bulls_on_parade.song_length()

print bulls_on_parade.add()

# Pushing a function inside the class
Song.random = random

print happy_bday.random()
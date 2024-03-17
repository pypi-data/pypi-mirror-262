import time
import unittest
from playerFramework import player

class Test_PlayerFramework(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audio_file = __file__.replace('test_player.py', 'overdrive.mp3')
        cls.player = player()

    def test_player_reg(self):
        self.player.play_track(self.audio_file)
        time.sleep(2)
        self.player.pause()
        time.sleep(1)
        self.player.resume()
        time.sleep(1)
        self.player.exit()


if __name__ == '__main__':
    unittest.main()
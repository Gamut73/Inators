import unittest
from file_namer import clean_movie_name

class TestCleanFilename(unittest.TestCase):
    def test_clean_filename(self):
        self.assertEqual(clean_movie_name('2004 - Survive Style 5+.mkv'), 'Survive Style 5+ (2004).mkv')
        self.assertEqual(clean_movie_name('Akira (1988) 2160p HDR 5.1 Eng - Jpn x265 10bit Phun Psyz.mkv'), 'Akira (1988).mkv')
        self.assertEqual(clean_movie_name('Europa.Europa.1990.1080p.BluRay.x264-[YTS.LT].mp4'), 'Europa Europa (1990).mp4')
        self.assertEqual(clean_movie_name('Gatto Nero, Gatto Bianco (1998) ITA sub ENG 1080p by PanzerB.mkv'), 'Gatto Nero, Gatto Bianco (1998).mkv')

if __name__ == '__main__':
    unittest.main()
import LearnSubtitles as ls

subtitle_path='/home/heitor/p/LearnSubtitles/testfiles/Dark.S01E01.WEBRip.x264-STRiFE.German.srt'

Darks01e01= ls.LearnSubtitles(subtitle_path, 'de')
print(Darks01e01.print_dict(level='intermediate'))

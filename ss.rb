require 'pragmatic_segmenter'

lang = ARGV[0]
ARGV.clear
text = ARGF.read
ps = PragmaticSegmenter::Segmenter.new(text: text, language: lang)
puts ps.segment

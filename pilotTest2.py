import gensim
model_path = 'wiki_dmpv_1000_no_taginfo_word2vec_format.bin'
model_path2 = 'wiki_dmpv_100_no_taginfo_user_dic_word2vec_format.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True, unicode_errors='ignore')


print(model.wv.similarity('왕','왕'))
print(model.wv.similarity('왕','여왕'))
print(model.wv.similarity('남자','여자'))
print(model.wv.similarity('왕','남자'))

print(model.wv.most_similar('여자')[0])
print(model.wv.most_similar(positive=['여자','여왕'],negative='왕')[0])
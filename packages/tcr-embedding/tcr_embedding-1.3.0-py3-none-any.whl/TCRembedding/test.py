from TCRGP.embedding import EmbeddingTCRGP

filepath = "data/testdata_TCRGP.csv"
epitope = 'ATDALMTGY' # epitope name in datafile, ignore if balance control is False
embedding = EmbeddingTCRGP(filepath)
embedded_data = embedding.embed(epitope,dimension=1)
print(embedded_data.shape)
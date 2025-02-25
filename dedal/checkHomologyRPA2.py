import tensorflow as tf
import tensorflow_hub as hub
from dedal import infer  # Requires google_research/google-research.

dedal_model = hub.load('https://tfhub.dev/google/dedal/3')

# "Gorilla" and "Mallard" sequences from [1, Figure 3].
protein_a = 'MIGQKTLYSFFSPSPARKRHAPSPEPAVQGTGVAGVPEESGDAAAIPAKKAPAGQEEPGTPPSSPLSAEQLDRIQRNKAAALLRLAARNVPVGFGESWKKHLSGEFGKPYFIKLMGFVAEERKHYTVYPPPHQVFTWTQMCDIKDVKVVILGQDPYHGPNQAHGLCFSVQRPVPPPPSLENIYKELSTDIEDFVHPGHGDLSGWAKQGVLLLNAVLTVRAHQANSHKERGWEQFTDAVVSWLNQNSNGLVFLLWGSYAQKKGSAIDRKRHHVLQTAHPSPLSVYRGFFGCRHFSKTNELLQKSGKKPIDWKEL'
protein_b = 'MSLPLTEEQRKKIEENRQKALARRAEKLLAEQHQRTSSGTSIAGNPFQAKQGPSQNFPRESCKPVSHGVIFKQQNLSSSSNADQRPHDSHSFQAKGIWKKPEEMPTACPGHSPRSQMALTGISPPLAQSPPEVPKQQLLSYELGQGHAQASPEIRFTPFANPTHKPLAKPKSSQETPAHSSGQPPRDAKLEAKTAKASPSGQNISYIHSSSESVTPRTEGRLQQKSGSSVQKGVNSQKGKCVRNGDRFQVLIGYNAELIAVFKTLPSKNYDPDTKTWNFSMNDYSALMKAAQSLPTVNLQPLEWAYGSSESPSTSSEGQAGLPSAPSLSFVKGRCMLISRAYFEADISYSQDLIALFKQMDSRRYDVKTRKWSFLLEEHSKLIAKVRCLPQVQLDPLPTTLTLAFASQLKKTSLSLTPDVPEADLSEVDPKLVSNLMPFQRAGVNFAIAKGGRLLLADDMGLGKTIQAICIAAFYRKEWPLLVVVPSSVRFTWEQAFLRWLPSLSPDCINVVVTGKDRLTAGLINIVSFDLLSKLEKQLKTPFKVVIIDESHFLKNSRTARCRAAMPVLKVAKRVILLSGTPAMSRPAELYTQIIAVKPTFFPQFHAFGLRYCDAKRMPWGWDYSGSSNLGELKLLLEEAVMLRRLKSDVLSQLPAKQRKIVVIAPGRINARTRAALDAAAKEMTTKDKTKQQQKDALILFFNRTAEAKIPSVIEYILDLLESGREKFLVFAHHKVVLDAITQELERKHVQHIRIDGSTSSAEREDLCQQFQLSERHAVAVLSITAANMGLTFSSADLVVFAELFWNPGVLIQAEDRVHRIGQTSSVGIHYLVAKGTADDYLWPLIQEKIKVLAEAGLSETNFSEMTESTDYLYKDPKQQKIYDLFQKSFEKEGSDMELLEAAESFDPGSASGTSGSSSQNMGDTLDESSLTASPQKKRRFEFFDNWDSFTSPL'
# Represents sequences as `tf.Tensor<tf.float32>[2, 512]` batch of tokens.
inputs = infer.preprocess(protein_a, protein_b)

# Aligns `protein_a` to `protein_b`.
align_out = dedal_model(inputs)

# Retrieves per-position embeddings of both sequences.
embeddings = dedal_model.call(inputs, embeddings_only=True)

# Postprocesses output and displays alignment.
output = infer.expand(
    [align_out['sw_scores'], align_out['paths'], align_out['sw_params']])
output = infer.postprocess(output, len(protein_a), len(protein_b))
alignment = infer.Alignment(protein_a, protein_b, *output)
print(alignment)

# Displays the raw Smith-Waterman score and the homology detection logits.
print('Smith-Waterman score (uncorrected):', align_out['sw_scores'].numpy())
print('Homology detection logits:', align_out['homology_logits'].numpy())

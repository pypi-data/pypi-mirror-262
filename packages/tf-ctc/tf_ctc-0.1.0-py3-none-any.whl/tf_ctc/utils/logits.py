import tensorflow as tf
from jaxtyping import Int, Float
from tf_tools import tf_function, pad_dim_to

@tf_function
def onehot_logits_sample(label: Int[tf.Tensor, "maxlen"], value: float = 1e9, vocabsize: int = None, num: int = None) -> Float[tf.Tensor, "2*maxlen vocabsize"]:
  """Logits that approach a CTC loss of 0 as `value` grows"""
  depth = tf.cast(vocabsize, tf.int32) # you'll have to ask tensorflow why the heck int64 indices are not valid for tf.one_hot...
  return value*tf.concat([
    [tf.one_hot(x, depth), tf.one_hot(0, depth)]
    for x in tf.unstack(label, num=num)
  ], axis=0) - value
  
@tf_function
def onehot_logits_tf(label: Int[tf.SparseTensor, "batch maxlen"], value: float = 1e9, *, batch: int, maxlen: int, vocabsize: int = 0) -> Float[tf.Tensor, "batch 2*maxlen vocabsize"]:
  dense = tf.sparse.to_dense(label)
  logits = [onehot_logits_sample(xs, value, vocabsize=vocabsize, num=maxlen)[None, ...] for xs in tf.unstack(dense, num=batch)]
  return tf.concat(logits, axis=0)

def onehot_logits(label: Int[tf.SparseTensor, "batch maxlen"], value: float = 1e9, vocabsize: int = None) -> Float[tf.Tensor, "batch 2*maxlen vocabsize"]:
  """Logits that approach a CTC loss of 0 as `value` grows.
  - `label :: Sparse[batch, maxlen]`: a batched sparse, can be obtained via e.g. `ocr.label('exd4')`
  - `vocabsize`: determines the shape of the logits. Clipped to be greater than `max(label)`
  - Returns `logits :: Tensor[batch, 2*maxlen, vocabsize]`
  """
  batch, maxlen = list(label.dense_shape)
  return onehot_logits_tf(label, value, batch=int(batch), maxlen=int(maxlen), vocabsize=vocabsize or tf.sparse.reduce_max(label)+1)

def mock_logits(top_preds: list[Int[tf.SparseTensor, "batch maxlen"]], vocabsize: int = None) -> Float[tf.Tensor, "batch 2*maxlen vocabsize"]:
  """Logits that, when CTC-decoded, will roughly follow `top_preds`
  
  E.g:
  ```
  top_preds = R.map(ocr.encode, [['e4', 'Nf6'], ['e5', 'Nd6']])
  z = mock_logits(top_preds)
  paths, _ = ctc.beam_decode(logits, top_paths=2)
  [ocr.decode(p) for p in paths] # [[b'e4', b'Nf6'], [b'e5', b'Nd6']]
  ```
  """
  delta = 1e3
  vocabsize = vocabsize or tf.reduce_max([tf.sparse.reduce_max(l)+1 for l in top_preds])
  logits = [onehot_logits(l, value=1e9+delta*i, vocabsize=vocabsize) for i, l in enumerate(reversed(top_preds))]
  maxlen = tf.reduce_max([tf.shape(z)[1] for z in logits])
  padded_logits = [pad_dim_to(z, axis=1, length=maxlen) for z in logits]
  return tf.reduce_sum(padded_logits, axis=0)
from typing import Unpack
from .beam import predict as beam_predict, Params
from .util.predict import prefetched_logprobs, PredictFn

def predict(
  predict: PredictFn, max_moves: int, batch_size: int = 8,
  prefetch: int = 2, **params: Unpack[Params]
):
  """Beam decoding across the forest of moves stemming from `start_fens`
  - Yields predictions as the beams converge (i.e. agree on a single move) or the search stops (because no legal moves have high enough probability)
    - Thus, a bigger `beam_width` can increase accuracy but also prediction time by more than a constant factor
  """
  return beam_predict(prefetched_logprobs(predict, max_moves, batch_size, prefetch), **params)
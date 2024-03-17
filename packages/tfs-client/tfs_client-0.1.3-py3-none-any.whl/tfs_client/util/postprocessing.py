import haskellian as hk
from ..http import SamplePreds, predict, Params

def transpose(sample: SamplePreds) -> list[tuple[str, float]]:
  return list(zip(sample.preds, sample.logprobs))

async def multi_predict(b64_multibatch: list[tuple[str, ...]], **params: Params) -> list[list[list[tuple[str, int]]]]:
    """Returns an array of shape `BATCH x PLAYERS x TOP_PREDS` of `(pred, logprob)`"""
    if len(b64_multibatch) == 0:
        return []
    num_players = len(b64_multibatch[0])
    flatbatch = list(hk.flatten(b64_multibatch))
    flatpreds = await predict(flatbatch, **params)
    return hk.vpipe(
        hk.map(transpose, flatpreds),
        hk.batch(num_players), # players x batch x top_preds
        hk.transpose, # # batch x players x top_preds
        list
    )
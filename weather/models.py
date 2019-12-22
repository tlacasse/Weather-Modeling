from weather.dataset import group 
from pomegranate import DiscreteDistribution, HiddenMarkovModel
import numpy as np

# store as list of incremental unique identifiers
class EncodedList:
    
    def __init__(self, items):
        self.items = items
        self.unique = list(set(items))
        self.encoded = [self.encode(x) for x in items]
    
    def encode(self, x):
        return self.unique.index(x)
    
    def decode(self, i):
        return self.unique[int(i)]
  
def round_to_bin(x, bin_size):
    return str(int(np.floor( x / bin_size ) * bin_size))
    
class WeatherModel:
    
    def __init__(self, hmm, emmissions, states, bin_size):
        self.hmm = hmm
        self.emmissions = emmissions
        self.states = states
        self.bin_size = bin_size
        
    def predict(self, sequence):
        sequence = self._bin_seq(sequence)
        return [self.states.decode(state.name) for i, state in self.hmm.viterbi(sequence)[1][1:]]
        
    def _bin_seq(self, sequence):
        return [round_to_bin(s, self.bin_size) for s in sequence]
    
    @classmethod
    def build_hmm(cls, emmissions, states, name, bin_size=2, pseudocount=1, em_min=0, em_max=255):
        emmissions = EncodedList(emmissions)
        states = EncodedList(states)

        data = group(by=states.encoded, values=emmissions.items)
        state_keys = list(data.keys())
        emmission_dists = []
        
        for s in state_keys:
            counts = {str(e): 1 for e in range(em_min, em_max+1, bin_size)}
            for e in data[s]:
                counts[round_to_bin(e, bin_size)] += 1
            total = len(data[s])
            dist = DiscreteDistribution({k: v / total for k, v in counts.items()})
            emmission_dists.append(dist)
    
        num_states = len(state_keys)
        transition = np.full((num_states, num_states), pseudocount, dtype='int32')
        totals = np.full((num_states,), pseudocount * num_states, dtype='int32')
        
        for i, j in zip(states.encoded, states.encoded[1:]):
            transition[i][j] += 1
            totals[i] += 1
            
        transition = transition.astype('double')
        for i in range(num_states):
            transition[i][:] /= totals[i]
            
        totals = totals.astype('double')
        total = sum(totals)
        for i in range(num_states):
            totals[i] /= total
        
        state_names = [str(n) for n in state_keys]
        hmm = HiddenMarkovModel.from_matrix(transition, emmission_dists, totals, 
                                            state_names=state_names, name=name)
        return cls(hmm, emmissions, states, bin_size)

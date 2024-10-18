import numpy as np

from BCC_Viterbi_decoder import restore_punctured_data, bcc_decoder
from constellation_demapper import constellation_demapper
from constellation_mapper import constellation_mapper
from deinterliver import deinterleaver
from OFDM_demod import ofdm_demod
from OFDM_mod import ofdm_mod
from scrambler import scrambler
from descrambler import descrambler
from BCC_FEC import bcc_fec
from interleaver import interleaver

from tests import benchmarks

def TxRx(size, modulation, r, demapper_method):
    data = np.random.randint(0, 2, size=size)

    # Transmit
    scrambled_bits = scrambler(data)
    encoded_data = bcc_fec(scrambled_bits, r)
    interleavered_data = interleaver(encoded_data)
    constellated_data = constellation_mapper(interleavered_data, modulation)
    modulated_data = ofdm_mod(constellated_data)

    # Receive
    demodulated_data = ofdm_demod(modulated_data)
    deconstellated_data = constellation_demapper(demodulated_data, modulation, demapper_method, 1)
    deinterleavered_data = deinterleaver(deconstellated_data)
    repunctured_data = restore_punctured_data(deinterleavered_data, r)
    decoded_data = bcc_decoder(repunctured_data, 7)
    descrambled_data = descrambler(decoded_data)

    if descrambled_data.all() == data.all():
        print(f"{modulation}\t{r}\t{demapper_method}\t\033[32mSuccess\033[0m")


if __name__ == "__main__":
    for benchmark in benchmarks:
        size = 208
        modulation = benchmark[0]
        r = benchmark[1]
        demapper_method = benchmark[2]

        try:
            TxRx(size, modulation, r, demapper_method)
        except Exception:
            print(f"{modulation}\t{r}\t{demapper_method}\t\033[31mInvalid length of input data\033[0m")

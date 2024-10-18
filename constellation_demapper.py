import numpy as np
from constellation_dicts import *


def constellation_demapper(symbols, constellation_mode, method, sigma=None):
    global constellation
    if constellation_mode == 'bpsk':
        constellation = bpsk_demap_dict
    elif constellation_mode == 'qpsk':
        constellation = qpsk_demap_dict
    elif constellation_mode == 'qam16':
        constellation = qam16_demap_dict
    elif constellation_mode == 'qam64':
        constellation = qam64_demap_dict

    if method == 'hard':
        return hard_demapper(symbols, constellation)
    elif method == 'soft':
        return soft_demapper(symbols, constellation, sigma)
    elif method == 'approx_soft':
        return approx_soft_demapper(symbols, constellation, sigma)


def hard_demapper(symbols, constellation_dict):
    demapped_bits = []
    for symbol in symbols:
        closest_symbol = min(constellation_dict.keys(), key=lambda x: np.abs(symbol - x))
        demapped_bits.extend(constellation_dict[closest_symbol])
    return np.array(demapped_bits)


def llr_to_bits(llrs):
    return np.array([0 if llr > 0 else 1 for llr in llrs])


def approx_soft_demapper(symbols, constellation_dict, sigma):
    LLRs = []

    for symbol in symbols:
        llr_symbol = []
        bit_count = len(next(iter(constellation_dict.values())))

        for bit_pos in range(bit_count):
            minDist0 = np.inf
            minDist1 = np.inf

            for const_symbol, bits in constellation_dict.items():
                distance = np.abs(symbol - const_symbol) ** 2

                if bits[bit_pos] == 0:
                    minDist0 = min(minDist0, distance)
                else:
                    minDist1 = min(minDist1, distance)

            llr_bit = -(1 / (2 * sigma ** 2)) * (minDist0 - minDist1)
            llr_symbol.append(llr_bit)

        LLRs.extend(llr_symbol)
    return llr_to_bits(np.array(LLRs))



def soft_demapper(symbols, constellation_dict, sigma):
    LLRs = []
    sqrt_2pi = np.sqrt(2 * np.pi)

    for symbol in symbols:
        llr_symbol = []

        bit_count = len(next(iter(constellation_dict.values())))

        for bit_pos in range(bit_count):
            num_sum = 0.0
            den_sum = 0.0

            for const_symbol, bits in constellation_dict.items():
                distance = np.abs(symbol - const_symbol) ** 2
                probability = (1 / (sqrt_2pi * sigma)) * np.exp(-distance / (2 * sigma ** 2))

                if bits[bit_pos] == 0:
                    num_sum += probability
                else:
                    den_sum += probability

            if den_sum == 0:
                llr_bit = np.inf
            elif num_sum == 0:
                llr_bit = -np.inf
            else:
                llr_bit = np.log(num_sum / den_sum)

            llr_symbol.append(llr_bit)

        LLRs.extend(llr_symbol)
    return llr_to_bits(np.array(LLRs))

clear;
% Gray code mapping
GRAY_CODE = [0 1 3 2];
STRING = int8('Hiiii_Kevin');
% String bits
STRING_BITS = char2bin(STRING);
% Gray string bits
GRAY_STRING_BITS = graycode(GRAY_CODE, STRING_BITS);
REPITITIONS = 60;
NOISE_SCALE = 0;
IQ_SAMPLE_RATE = 40;
IQ_CARRIER_RATE = 4;
% Reserve space for data
data_bits = zeros(1, length(GRAY_STRING_BITS) * REPITITIONS);
% Copy string bits into the data multiple times
for i = 1:length(GRAY_STRING_BITS):length(data_bits)
    data_bits(1, i:(i - 1) + length(GRAY_STRING_BITS)) = GRAY_STRING_BITS;
end
I_bits = data_bits(1:2:end);
Q_bits = data_bits(2:2:end);
% Convert data into QPSK/BPSK words
I_symbols = I_bits * 2 - 1;
Q_symbols = Q_bits * 2 - 1;
% Upsample to prepare to superimpose on IQ waves
I_symbols = repelem(I_symbols, IQ_SAMPLE_RATE);
Q_symbols = repelem(Q_symbols, IQ_SAMPLE_RATE);
% Generate carrier waves
t = 0:2 * pi * IQ_CARRIER_RATE / IQ_SAMPLE_RATE:(length(data_bits) / 2 - 1 / IQ_SAMPLE_RATE) * 2 * pi * IQ_CARRIER_RATE;
I = cos(t);
Q = sin(t);
I_modulated = I .* I_symbols;
Q_modulated = Q .* Q_symbols;

qpsk_signal = I_modulated + Q_modulated;

% Makecomplex noise by picking a direction uniformly, then a magnitude from
% the standard normal distribution
noise = exp(2 * pi * 1i * rand(1, length(qpsk_signal))) .* randn(1, length(qpsk_signal));
noisy_signal = qpsk_signal + real(noise) * NOISE_SCALE;
% Rescale to [-1, 1] for audiowrite
scaled = rescale(real(noisy_signal), -1 , 1);

audiowrite("three.wav", scaled, IQ_SAMPLE_RATE);
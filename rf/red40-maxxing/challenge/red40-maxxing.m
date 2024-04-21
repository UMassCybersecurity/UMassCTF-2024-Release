STRING = int8('Its_not_just_a_boulder_its_a_rock');
REPITITIONS = 40;
NOISE_SCALE = 0.4;
% Reserve space for data
data_bits = zeros(length(STRING) * 8 * REPITITIONS, 1);
% Copy string bits into the data multiple times
for i = 1:length(STRING) * 8:length(data_bits)
    data_bits(i:(i - 1) + length(STRING) * 8) = char2bin(STRING);
end
% Encode into bpsk symbols
bpsk_symbols = data_bits * 2 - 1;
% Makecomplex noise by picking a direction uniformly, then a magnitude from
% the standard normal distribution
noise = exp(2 * pi * 1i * rand(length(bpsk_symbols), 1)) .* randn(length(bpsk_symbols), 1);
% Add noise with scale factor
bpsk_symbols_with_noise = bpsk_symbols + NOISE_SCALE * noise;
% Rescale to [-1, 1] for audiowrite
scaled = rescale(real(bpsk_symbols_with_noise), -1 , 1);
audiowrite("one.wav", scaled, 1);

clear;

STRING = int8('Krusty_Krab_pizza_is_the_pizza_for_you_and_me');
REPITITIONS = 40;
TAPS = [2 3 4 5];
TRAINING_NOISE_SCALE = 0.5;
DATA_NOISE_SCALE = 1.5;  % Crank that shizz up, should be illegible without correlation
TRAINING_PAIRS = 20;

dsss_seq = lfsr(1, [2 3 4 5], 2 .^ max(TAPS) - 1);

data_bits = zeros((TRAINING_PAIRS * 2 + REPITITIONS * length(STRING) * 8) * length(dsss_seq), 1);

start_bit = 1;
for i = 1:TRAINING_PAIRS
    data_bits(start_bit:start_bit + 30) = ~dsss_seq;
    data_bits(start_bit + 31:start_bit + 61) = dsss_seq;
    start_bit = start_bit + 31 * 2;
end

for i = 1:REPITITIONS
    for j = 1:length(STRING)
        for k = 1:8
            data_bits(start_bit:start_bit + 30) = xor(dsss_seq, bitget(STRING(j), 9 - k));
            start_bit = start_bit + 31;
        end
    end
end

bpsk_symbols = data_bits * 2 - 1;

% Makecomplex noise by picking a direction uniformly, then a magnitude from
% the standard normal distribution
training_length = TRAINING_PAIRS * 2 * length(dsss_seq);
training_noise = exp(2 * pi * 1i * rand(training_length, 1)) .* randn(training_length, 1);
data_length = length(bpsk_symbols) - training_length;
data_noise = exp(2 * pi * 1i * rand(data_length, 1)) .* randn(data_length, 1);
% Add noise with scale factor
bpsk_symbols_with_noise = vertcat(bpsk_symbols(1:training_length) + TRAINING_NOISE_SCALE * training_noise, ...
    bpsk_symbols(training_length + 1:end) + DATA_NOISE_SCALE * data_noise);

% Rescale to [-1, 1] for audiowrite
scaled = rescale(real(bpsk_symbols_with_noise), -1 , 1);

audiowrite("two.wav", scaled, 1);
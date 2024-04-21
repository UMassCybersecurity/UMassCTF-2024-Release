clear;
% Gray code mapping
GRAY_CODE = [0 1 3 2];
STRING = int8('Hiiii_Kevin');
% String bits
STRING_BITS = char2bin(STRING);
% Gray string bits
GRAY_STRING_BITS = graycode(GRAY_CODE, STRING_BITS);
REPITITIONS = 60;
NOISE_SCALE = 1.5;
IQ_SAMPLE_RATE = 40;
IQ_CARRIER_RATE = 4;
% Reserve space for data
data_bits = zeros(1, length(GRAY_STRING_BITS) * REPITITIONS);
% Generate carrier waves
t = 0:2 * pi * IQ_CARRIER_RATE / IQ_SAMPLE_RATE:(length(data_bits) / 2 - 1 / IQ_SAMPLE_RATE) * 2 * pi * IQ_CARRIER_RATE;
I = cos(t);
Q = sin(t);
% Sample solve script
recovered_samples = audioread("../static/yellow6-maxxing.wav");
% Create coefficients for 6 term low pass filter that passes everything
% below 0.1 radians per sample
[b, a] = butter(6, 0.1);
% Recover I/Q samples and then low pass to get the bit streams
recovered_I = filter(b, a, real(recovered_samples.' .* I));
recovered_Q = filter(b, a, real(recovered_samples.' .* Q));
% Reserve space for recovered bits
recovered_I_bits = zeros(1, length(recovered_I) / IQ_SAMPLE_RATE);
recovered_Q_bits = zeros(1, length(recovered_Q) / IQ_SAMPLE_RATE);
% Loop through samples (by looping over I/Q recovered bits) and scaling by
% sample rate
for i = 1:length(recovered_I_bits)
    pos = IQ_SAMPLE_RATE * (i - 1) + IQ_SAMPLE_RATE / 2;
    if recovered_I(pos) > 0
        recovered_I_bits(i) = 1;
    else
        recovered_I_bits(i) = 0;
    end
    if recovered_Q(pos) > 0
        recovered_Q_bits(i) = 1;
    else
        recovered_Q_bits(i) = 0;
    end
end

recovered_bits = reshape([recovered_I_bits; recovered_Q_bits], 1, []);

disp(bin2char(graycode(GRAY_CODE, recovered_bits)));
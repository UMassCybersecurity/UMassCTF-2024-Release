% Sample solve script
recovered_samples = audioread("yellow5-maxxing.wav");
recovered_bits = zeros(length(recovered_samples) / 31, 1);

for i = 1:length(recovered_bits)
    start_bit = (i - 1) * 31 + 1;
    if dot(recovered_samples(start_bit:start_bit + 30), recovered_samples(1:31)) > 0
        recovered_bits(i) = 1;
    else
        recovered_bits(i) = 0;
    end
end

disp("Good: ");
disp(bin2char(recovered_bits(41:end)));

% Sample bad solve script (doesn't use correlation)
recovered_samples = audioread("yellow5-maxxing.wav");
recovered_bits = zeros(length(recovered_samples) / 31, 1);

for i = 1:length(recovered_bits)
    start_bit = (i - 1) * 31 + 1;
    if recovered_samples(start_bit) > 0
        recovered_bits(i) = 0;
    else
        recovered_bits(i) = 1;
    end
end

disp("Bad: ");
disp(bin2char(recovered_bits(41:end)));

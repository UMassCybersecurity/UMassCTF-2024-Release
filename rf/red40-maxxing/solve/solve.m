% Sample solve script
recovered_samples = audioread("red40-maxxing.wav");
recovered_bits = zeros(length(recovered_samples), 1);

for i = 1:length(recovered_bits)
    if recovered_samples((i - 1) + 1) < 0
        recovered_bits(i) = 0;
    else
        recovered_bits(i) = 1;
    end
end

disp(bin2char(recovered_bits));

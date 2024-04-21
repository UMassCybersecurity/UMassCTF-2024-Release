function binvec = graycode(code, input)
    % Gray string bits
    binvec = zeros(1, length(input));
    for i = 1:2:length(input)
        binvec(i:i+1) = bitget(code(2 * input(i + 1) + input(i) + 1), 1:2);
    end
end
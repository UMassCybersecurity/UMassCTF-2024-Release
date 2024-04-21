function binvec = char2bin(charinput)
    binvec = reshape((dec2bin(charinput,8) - '0').',1,[]);
end
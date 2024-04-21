function origchar = bin2char(binvec)
   origchar = char(reshape(bin2dec(reshape(char(binvec + '0'),8,[]).'),1,[]));
end
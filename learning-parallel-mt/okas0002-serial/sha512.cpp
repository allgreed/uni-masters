#include "sha512.hpp"

using SHA512_constants::b64;
using SHA512_constants::b8;


inline static b64 rrot(b64 n, unsigned int d);


b64 * sha512(b8 * message, size_t message_length_bytes, b64 * hash)
{
    int padding_size = (((896 - message_length_bytes * 8 - 1) % 1024 + 1024) % 1024 + 1) / 8;

    size_t payload_size = message_length_bytes + padding_size + 16;
    b8 * payload = new b8[payload_size]; // non initialized by design, since it will be overwritten anyway

    memcpy(payload, message, message_length_bytes);
    payload[message_length_bytes] = 0b10000000;
    memset(payload + message_length_bytes + 1, 0, 15);

    unsigned int size = htonl(message_length_bytes * 8);
    memcpy(payload + (payload_size - sizeof(unsigned int)), &size, sizeof(unsigned int));

    memcpy(hash, SHA512_constants::IV, 8 * 8);

    size_t block_count = (payload_size / 128);
    for(size_t i = 0; i < block_count; ++i)
    {
        b8 * block = payload + (128 * i);
        _sha512_block(hash, block);
    }

    delete[] payload;
    return hash;
}


void _sha512_block(b64 * hash, b8 * block)
{
    b64 w[80]; // non initialized by design, since it will be overwritten anyway

    // fancy way of converting bytes into little-endian u64 integers
    for(int i = 0; i < 16; ++i)
    {
        for(int j = 0; j < 8; ++j)
        {
            ((b8 *) w)[j + (i * 8)] = block[7 - j + (8 * i)];
        }
    } 

    for(int i = 16; i < 80; ++i)
    {
        b64 sigma0 = (rrot(w[i-15], 1)) ^ (rrot(w[i-15], 8)) ^ (w[i-15] >> 7);
        b64 sigma1 = (rrot(w[i-2], 19)) ^ (rrot(w[i-2], 61)) ^ (w[i-2] >> 6);
        w[i] = w[i-16] + sigma0 + w[i-7] + sigma1;
    }


    b64 a = hash[0];
    b64 b = hash[1];
    b64 c = hash[2];
    b64 d = hash[3];
    b64 e = hash[4];
    b64 f = hash[5];
    b64 g = hash[6];
    b64 h = hash[7];

    for(int i = 0; i < 80; ++i)
    {
        b64 Sigma0 = (rrot(a, 28)) ^ (rrot(a, 34)) ^ (rrot(a, 39));
        b64 Sigma1 = (rrot(e, 14)) ^ (rrot(e, 18)) ^ (rrot(e, 41));
        b64 ch = (e & f) ^ ((~ e) & g);
        b64 maj = (a & b) ^ (a & c) ^ (b & c);

        b64 temp1 = h + Sigma1 + ch + SHA512_constants::K[i] + w[i];
        b64 temp2 = Sigma0 + maj;

        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    hash[0] += a;
    hash[1] += b;
    hash[2] += c;
    hash[3] += d;
    hash[4] += e;
    hash[5] += f;
    hash[6] += g;
    hash[7] += h;
}


inline static b64 rrot(b64 n, unsigned int d)
{ 
    // this is redundant as all calls are static and don't require this check
    // however I don't thing c++ provides a way to assert that in a sensible way at compile
    // I could template it for used values, but not sure that the implementation would benefit from monomorphisation
    if (d > 64)
        d = d % 64;

    return (n >> d) | (n << (sizeof(b64) * 8 - d));
}


void dump_digest(b64 * hash)
{
    for(int i = 0; i < 8; ++i) 
    {
        std::cout << std::hex << std::setw(16) << std::setfill('0') << hash[i];
    }
    std::cout << std::endl;
}

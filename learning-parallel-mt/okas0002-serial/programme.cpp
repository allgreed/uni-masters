#include "sha512.hpp"

using SHA512_constants::b64;
using SHA512_constants::b8;


int main()
{
    assertalways(htons(47) != 47); // Little Endian check

    constexpr int seed = 125;
    constexpr int n = 6; // block size factor
    constexpr size_t message_length_bytes = 111 + 128 * n;

    auto rand = jbutil::randgen(seed);

    b8 * message = new b8[message_length_bytes];
    unsigned int * nonce = (unsigned int *)(message);
    for(size_t i = 0; i < message_length_bytes / 8; ++i)
        ((b64 *) message)[i] = rand.ival64();

    *nonce = 0;

    b64* hash = new b64[8];

    double t = jbutil::gettime();
    do
    {
        sha512((b8 *) message, message_length_bytes, hash);
        ++(*nonce);
    }
    while(!(hash[0] > 0xcafdffffffffffff && hash[0] < 0xcaff000000000000));
    //while(!(hash[0] > 0xcafeafffffffffff && hash[0] < 0xcafec00000000000));
    // looking for hash starting with "cafeb"
    t = jbutil::gettime() - t;

    std::cout << "Time taken: " << t << "s" << std::endl
              << "Block size: " << message_length_bytes << " bytes" << std::endl
              << "Nonce: " << std::dec << *nonce << std::endl
              << "MH/s " << std::dec << *nonce / t / 1e+6 << std::endl
              << "MHB[locks]/s " << std::dec << *nonce * 7 / t / 1e+6 << std::endl
              ;
    dump_digest(hash);
}

void dump_payload(b8 * payload, const size_t payload_size)
{
    for(size_t i = 0; i < payload_size; ++i)
    {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << +payload[i];
    }
    std::cout << std::endl;
}

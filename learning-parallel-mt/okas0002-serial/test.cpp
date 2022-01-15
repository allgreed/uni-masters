#include "sha512.hpp"

using SHA512_constants::b64;
using SHA512_constants::b8;


int main()
{
    assertalways(htons(47) != 47); // Little Endian check

    const char * m2 = "abc";
    constexpr int m2_l = 3;
    b64 * hash = new b64[8];
    sha512((b8 *) m2, m2_l, hash);
    dump_digest(hash);
    std::cout << "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f" << std::endl << std::endl;
    delete[] hash;

    const char * m1 = "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu";
    constexpr size_t m1_l = 112;
    hash = new b64[8];
    hash = sha512((b8 *) m1, m1_l, hash);
    dump_digest(hash);
    std::cout << "8e959b75dae313da8cf4f72814fc143f8f7779c6eb9f7fa17299aeadb6889018501d289e4900f7e4331b99dec4b5433ac7d329eeb6dd26545e96e55b874be909" << std::endl;
    delete[] hash;
}

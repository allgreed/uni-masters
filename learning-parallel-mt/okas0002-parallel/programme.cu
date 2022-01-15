#include "sha512.hpp"

using SHA512_constants::b64;
using SHA512_constants::b8;


int main()
{
    validate_runtime();
    auto rand = jbutil::randgen(RANDOM_SEED);
    constexpr size_t message_length_bytes = 111 + SHA512_BLOCK_SIZE * (INPUT_SIZE_BLOCKS - 1);

    b8 * message = new b8[message_length_bytes];
    for(size_t i = 0; i < message_length_bytes / 8; ++i)
        ((b64 *) message)[i] = rand.ival64();

    std::cout << "Running at concurrency factor " << CONCURRENCY
        << " [" << OVERCOMMIT_RATIO << "x overcommited]"
        << " (" << SM_COUNT << "/" << BLOCKS_PER_SM
        << "/" << THREADS_PER_BLOCK
        << ") [multiprocessors / blocks / threads]"
        << std::endl
        ;

    // first cudaMalloc is insanely slow - no point in timing that
    b64 * dhash;
    cudaMalloc((void **) &dhash, 8 * sizeof(b64));

    unsigned int * dresult;
    // this could be squashed into a single cudaMalloc
    // but that would only complicate the code for neglegible performance gain
    cudaMalloc((void **) &dresult, sizeof(unsigned int));
    cudaMemset(dresult, 0, sizeof(unsigned int));

    // ---------- clock starts here --------
    double t = jbutil::gettime();

    int padding_size = (((896 - message_length_bytes * 8 - 1) % 1024 + 1024) % 1024 + 1) / 8;

    size_t payload_size = message_length_bytes + padding_size + 16;
    b8 * payload;
    cudaMallocHost((void **) &payload, payload_size * sizeof(b8));
    // not initialized by design, since it will be overwritten anyway

    memcpy(payload, message, message_length_bytes);
    payload[message_length_bytes] = 0b10000000;
    memset(payload + message_length_bytes + 1, 0, 15);

    unsigned int size = htonl(message_length_bytes * 8);
    memcpy(payload + (payload_size - sizeof(unsigned int)), &size, sizeof(unsigned int));

    unsigned int nonce = 0;
    unsigned int result;


    int cycles = 0;
    load_payload_to_const(payload, payload_size);

    while(true)
    {
        cuda_sha512(payload, payload_size, dhash, nonce, dresult);
        cudaMemcpy(&result, dresult, sizeof(unsigned int), cudaMemcpyDeviceToHost);

        if (result != 0)
        {
            break;
        }

        nonce += CONCURRENCY;
        ++cycles;
    }

    b64* hash;
    cudaMallocHost((void **) &hash, 8 * sizeof(b64));
    unsigned int target_nonce = nonce + result;
    cudaMemcpy(hash, dhash, 8 * sizeof(b64), cudaMemcpyDeviceToHost);

    t = jbutil::gettime() - t;
    // ---------- clock stops here --------
    std::cout << "Time taken: " << t << "s" << std::endl
              << "Block size: " << message_length_bytes << " bytes" << std::endl
              << "Input block count: " << INPUT_SIZE_BLOCKS << std::endl
              << "Nonce: " << std::dec << target_nonce << std::endl
              << "Cycles: " << std::dec << cycles << std::endl
              << "MH/s " << std::dec << (nonce + CONCURRENCY) / t / 1e+6 << std::endl
              << "MHB[locks]/s " << std::dec << (nonce + CONCURRENCY) * INPUT_SIZE_BLOCKS / t / 1e+6 << std::endl
    ;

    dump_digest(hash);

    std::cout << "payload:" << std::endl;

    for (int i = 0; i < 4; ++i)
        message[i] = ((b8 *)&target_nonce)[i];

    dump_payload(message, message_length_bytes);

    // not really needed (since the OS will collect the memory anyway)
    // but here for the sake of completness
    cudaFree(dhash);
    cudaFree(dresult);
    delete[] message;
    cudaFreeHost(payload);
    cudaFreeHost(hash);
}


void dump_digest(b64 * hash)
{
    for(int i = 0; i < 8; ++i) 
    {
        std::cout << std::hex << std::setw(16) << std::setfill('0') << hash[i];
    }
    std::cout << std::endl;
}

void dump_payload(b8 * payload, const size_t payload_size)
{
    for(size_t i = 0; i < payload_size; ++i)
    {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)payload[i];
    }
    std::cout << std::endl;
}

void validate_runtime()
{
    // Little Endian check
    assertalways(htons(47) != 47);
    assertalways(sizeof(unsigned int) == 4);
}

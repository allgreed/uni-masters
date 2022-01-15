#ifndef SHA512_H
#define SHA512_H

#include <cstring>
#include <iomanip>
#include <arpa/inet.h>
#include "gpu.hpp"
#include "jbutil.h"

// experiment parameters
constexpr size_t BLOCKS_PER_SM = 4;
constexpr size_t WARP_COUNT_PER_BLOCK = 6;
constexpr size_t RANDOM_SEED = 126;
constexpr size_t INPUT_SIZE_BLOCKS = 7;


constexpr size_t SHA512_BLOCK_SIZE = 128;
constexpr size_t THREADS_PER_BLOCK = WARP_COUNT_PER_BLOCK * WARP_SIZE;
constexpr size_t BLOCK_COUNT = SM_COUNT * BLOCKS_PER_SM;
constexpr size_t CONCURRENCY = THREADS_PER_BLOCK * BLOCK_COUNT;
constexpr size_t OVERCOMMIT_RATIO = BLOCKS_PER_SM  / (MAX_WARP_COUNT_PER_BLOCK / WARP_COUNT_PER_BLOCK);
static_assert(WARP_COUNT_PER_BLOCK <= MAX_WARP_COUNT_PER_BLOCK, "desired warp count per block is higher than max possible");

#include "constants.hpp"
using SHA512_constants::b64;
using SHA512_constants::b8;

constexpr size_t blocks_in_constant_memory = 128;
constexpr size_t dpayload_constant_size = (SHA512_BLOCK_SIZE / sizeof(b8)) * blocks_in_constant_memory;
__constant__ b8 dpayload[dpayload_constant_size];
static_assert(dpayload_constant_size >= (INPUT_SIZE_BLOCKS * SHA512_BLOCK_SIZE), "payload cannot fit in allocated constant memory");


template <unsigned char D>
__device__ inline static b64 d_rrot(b64 n);
__device__ static void compute_round(b64 * w, b64 * hash);
__device__ inline static unsigned int my_thread_id();
template <typename T>
__device__ inline static T get_local_ptr_item(T ptr, size_t idx);
template <typename T>
__device__ T get_remote_ptr_item(T ptr, size_t idx, unsigned int unique_thread_id);
void cuda_sha512(b8 * payload, size_t payload_size, b64 * dhash, const int starting_nonce, unsigned int * dresult);
void load_payload_to_const(b8 * payload, const size_t payload_size);
void dump_digest(b64 * hash);
void dump_payload(b8 * payload, const size_t payload_size);
void validate_runtime();
#endif

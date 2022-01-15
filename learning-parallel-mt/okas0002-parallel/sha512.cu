#include "sha512.hpp"

using SHA512_constants::b64;
using SHA512_constants::b8;


__global__ void ComputeHashAndCheckResult(b64 * mem_hash, unsigned int * result, const int starting_nonce, const size_t payload_size)
{
    b64 w[80];
    b64 hash[8];

    for(int i = 0; i < 8; ++i)
    {
        hash[i] = SHA512_constants::IV[i];
    }

    // unroll part of the loop and apply nonce
    b8 init[8];
    for(int i = 4; i < 8; ++i)
    {
        init[i] = dpayload[i];
    }
    unsigned int * nonce = (unsigned int *)(init);
    *nonce = starting_nonce + my_thread_id();
    for(int j = 0; j < 8; ++j)
    {
        ( (b8*)get_local_ptr_item(w, 0) )[j] = init[7 - j];
    }

    // convert to LE
    for(int i = 1; i < 16; ++i)
    {
        for(int j = 0; j < 8; ++j)
        {
            ( (b8*)get_local_ptr_item(w, i) )[j] = dpayload[7 - j + (8 * i)];
        }
    } 

    compute_round(w, hash);

    for(size_t block_offset = SHA512_BLOCK_SIZE;  block_offset < payload_size; block_offset += SHA512_BLOCK_SIZE)
    {
        for(int i = 0; i < 16; ++i)
        {
            for(int j = 0; j < 8; ++j)
            {
                ((b8 *) get_local_ptr_item(w, i))[j] = dpayload[block_offset + 7 - j + (8 * i)];
            }
        } 

        compute_round(w, hash);
    }

    //if((hash[0] > 0xcafdffffffffffff && hash[0] < 0xcaff000000000000))
    //if((hash[0] > 0xcafeafffffffffff && hash[0] < 0xcafec00000000000))
    // looking for hash starting with "cafeba"
    if (hash[0] > 0xcafeb9ffffffffff && hash[0] < 0xcafebb0000000000)
    {
        unsigned int old_result = atomicCAS(result, 0, my_thread_id());

        if (old_result == 0)
        {
            for (int i = 0; i < 8; ++i)
                mem_hash[i] = hash[i];
        }

        return;
    }
}


__device__ inline static void compute_round(b64 * w, b64 * hash)
{
    for(int i = 16; i < 80; ++i)
    {
        b64 sigma0 = 
            (d_rrot<1>(*get_local_ptr_item(w, i-15))) ^ 
            (d_rrot<8>(*get_local_ptr_item(w, i-15))) ^
            (*get_local_ptr_item(w, i-15) >> 7);

        b64 sigma1 = 
            (d_rrot<19>(*get_local_ptr_item(w, i-2))) ^
            (d_rrot<61>(*get_local_ptr_item(w, i-2))) ^
            (*get_local_ptr_item(w, i-2) >> 6);

        *get_local_ptr_item(w, i) = *get_local_ptr_item(w, i-16) + sigma0 + *get_local_ptr_item(w, i-7) + sigma1;
    }

    b64 a = *get_local_ptr_item(hash, 0);
    b64 e = *get_local_ptr_item(hash, 4);
    b64 f = *get_local_ptr_item(hash, 5);
    b64 g = *get_local_ptr_item(hash, 6);
    b64 c = *get_local_ptr_item(hash, 2);
    b64 b = *get_local_ptr_item(hash, 1);
    b64 h = *get_local_ptr_item(hash, 7);
    b64 d = *get_local_ptr_item(hash, 3);

    for(int i = 0; i < 80; ++i)
    {
        b64 Sigma0 = (d_rrot<28>(a)) ^ (d_rrot<34>(a)) ^ (d_rrot<39>(a));
        b64 Sigma1 = (d_rrot<14>(e)) ^ (d_rrot<18>(e)) ^ (d_rrot<41>(e));
        b64 ch = (e & f) ^ ((~ e) & g);
        b64 maj = (a & b) ^ (a & c) ^ (b & c);

        b64 temp1 = h + Sigma1 + ch + SHA512_constants::K[i] + *get_local_ptr_item(w, i);
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

    *get_local_ptr_item(hash, 0) += a;
    *get_local_ptr_item(hash, 1) += b;
    *get_local_ptr_item(hash, 2) += c;
    *get_local_ptr_item(hash, 3) += d;
    *get_local_ptr_item(hash, 4) += e;
    *get_local_ptr_item(hash, 5) += f;
    *get_local_ptr_item(hash, 6) += g;
    *get_local_ptr_item(hash, 7) += h;
}


void load_payload_to_const(b8 * payload, const size_t payload_size)
{
    // for reasons foreing and bizzare to me
    // this memcpy has to happen in this file
    // belive me, I tried
    cudaMemcpyToSymbol(dpayload, payload, payload_size);
}


void cuda_sha512(b8 * payload, const size_t payload_size, b64 * dhash, const int starting_nonce, unsigned int * dresult)
{
    ComputeHashAndCheckResult<<<BLOCK_COUNT, THREADS_PER_BLOCK>>>(dhash, dresult, starting_nonce, payload_size);
}


template <unsigned char D>
__device__ inline static b64 d_rrot(b64 n)
{ 
    static_assert(D <= sizeof(b64) * 8, "unsupported value for rotation parameter D, D is too large");

    return (n >> D) | (n << (sizeof(b64) * 8 - D));
}


__device__ inline static unsigned int my_thread_id()
{
    return blockIdx.x*blockDim.x + threadIdx.x;
}

template <typename T>
__device__ inline static T get_local_ptr_item(T ptr, size_t idx)
{
    return get_remote_ptr_item(ptr, idx, my_thread_id());
}

template <typename T>
__device__ T get_remote_ptr_item(T ptr, size_t idx, unsigned int unique_thread_id)
{
    return ptr + idx;
}

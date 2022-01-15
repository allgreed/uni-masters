#ifndef SHA512_H
#define SHA512_H

#include <cstring>
#include <iomanip>
#include <arpa/inet.h>

#include "jbutil.h"
#include "constants.hpp"


using SHA512_constants::b64;
using SHA512_constants::b8;

void dump_digest(b64 *);
void dump_payload(b8 *, const size_t);
b64 * sha512(b8 * message, size_t message_length_bytes, b64 *);
void _sha512_block(b64 * hash, b8 * block);
#endif

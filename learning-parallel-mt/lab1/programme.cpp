#include "../shared/jbutil.h"
#include <thread>
#include <cassert>

const double a = -2.0;
const double b = 2.0;
const double A = 0.0;
const double B = 0.4;
const double mu = 0;
const double sigma = 1;

#ifndef P_SINGLE
#ifndef P_MULTI
# error Invalid control macro, aborting! Must define either P_SINGLE or P_MULTI
#endif
#endif

double the_function(const double x)
{
    return 1.0 / sqrt(2.0 * pi * pow(sigma, 2)) * exp(-(pow(x - mu, 2) / 2 * pow(sigma, 2)));
}

double MonteCarlo(const int N)
{
    std::cerr << "Implementation (" << N << " samples)" << std::endl;
    std::cerr << "Splitting over " << THREADS << " threads" << std::endl << std::endl;
    double t = jbutil::gettime();

#ifdef P_MULTI
    auto f = [](int N, int * result) { 
#endif
        auto rand = jbutil::randgen(pthread_self());
        int M = 0;
        for (int i = 0; i < N; ++i)
        {
            double x = rand.fval(a, b);
            double y = rand.fval(A, B);
            if (y < the_function(x))
                ++M;
        }
#ifdef P_MULTI
        // this is still inside of the heavy computation part
        *result = M;
    }; 

    const int N_split = N / THREADS;
    const int N_remainder = N % THREADS;
    // this needs to be on the heap so that the threads can access it
    int * M_ = new int[THREADS];

    std::thread th[THREADS];
    for (int i = 0; i < THREADS - 1; ++i)
    {
        th[i] = std::thread(f, N_split, M_ + i);
    }
    th[THREADS - 1] = std::thread(f, N_split + N_remainder, M_ + THREADS - 1);

    for (int i = 0; i < THREADS; ++i)
    {
        th[i].join();
    }

    int M = 0;
    for (int i = 0; i < THREADS; ++i)
    {
        M += M_[i];
    }
#endif

    const double result = (double) M / N * (B - A) * (b - a) + A * (b - a);

    t = jbutil::gettime() - t;
    std::cerr << "Time taken: " << t << "s" << std::endl;
    return result;
}

int main()
{
    // THREADS are defined and are an integer
    assert (THREADS + 1);

    std::cerr << "Lab 1: Monte Carlo integration" << std::endl;
    const int N = int(1E8);

    const double mc_result = MonteCarlo(N);
    const double erf_result = erf(sqrt(2.0));

    std::cerr << "Monte Carlo result: " << mc_result << std::endl;
    std::cerr << "ERF result: " << erf_result << std::endl;
    std::cerr << "Difference: " << mc_result - erf_result << std::endl;
}

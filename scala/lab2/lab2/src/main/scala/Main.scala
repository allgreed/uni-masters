import scala.annotation.tailrec


object Main extends App {
  println(is_prime(5))
  println(is_prime(12))

  println(fib(2))
  println(fib(3))
  println(fib(4))

  println(is_sorted(Array(1, 1, 1), (a: Int, b: Int) => { a == b }))
  println(is_sorted(Array(1, 1, 3), (a: Int, b: Int) => { a == b }))

  println(possibru(14))

  def is_prime(n: Int): Boolean = {
    @tailrec
    def is_prime_rec(n: Int, i: Int): Boolean = {
      if (n <= 1) {  
         return false;  
      }

      if (i == 1) {
          return true;
      }

      if(n % i == 0){
          return false;
      }

      is_prime_rec(n, i - 1)
    }
    is_prime_rec(n, n - 1)
  }

  def fib(n: Int): Int = {
    @tailrec
    def fib_rec(a: Int, b: Int, n: Int): Int = {
      if (n <= 1) {
        return a + b;
      }

      fib_rec(b, a + b, n - 1)
    }

    // TODO: edge cases, but I don't feel like them ;d
    fib_rec(1, 1, n)
  }

  def is_sorted(tab: Array[Int], mlr: (Int, Int) => Boolean): Boolean = {
    val tab_l = tab.length - 1

    @tailrec
    def is_sorted_rec(i: Int): Boolean = {
      if (i >= tab_l) { true } else {
        if (mlr(tab(i), tab(i + 1))) { is_sorted_rec(i + 1) } else { false }
      }
    }

    is_sorted_rec(0)
  }

  def possibru(n: Int): Boolean = {
    for(i <- 4 to n by 2) {
      if (heh_factorize(i)) {} else { return false; }
    }

    def heh_factorize(n: Int): Boolean = {
      if (2 + n - 2 == n)
      {
        println(n.toString + " = 2 + " + (n - 2).toString);
        true
      }
      else
      {
        false
      }
    }
    true
  }
}


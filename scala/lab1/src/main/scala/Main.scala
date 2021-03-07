object Main extends App {
  var x = io.StdIn.readInt()
  var y = io.StdIn.readInt()
  println(gcd(x, y))

  def gcd (a: Int, b: Int) : Int = {
    if (b == 0)
    {
      return a
    }
    else
    {
      return gcd(b, a % b)
    }
  }

}

object Ble {
  def main(args: Array[String]) = {
    var n = io.StdIn.readInt()

    if (n < 0)
    {
      println("not a natural number")
    }

    if (n == 1 || n == 0)
    {
      println("it's complicated")
    }

    println((if (! is_prime(n)) { "not " } else { "" }) + "prime")
  }

  // but really Nat -> Boolean
  def is_prime(n: Int) : Boolean = {
    var i = 2
    while ((i * i) < n)
    {
      if (n % i == 0) { return false }
      i = i + 1
    }

    return true
  }
}

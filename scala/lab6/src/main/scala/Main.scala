import scala.math
import scala.language.implicitConversions


class C(val re: Double, val im: Double) {
  override def toString(): String = if (im > 0) { s"$re + ${im}i" }
    else if (im < 0) { s"$re - ${im.abs}i" } 
    else { s"$re" } // im == 0 

  private def plus_minus(that: C, op: (Double, Double) => Double): C = C(op(this.re, that.re),op(this.im, that.im))
  def -(that: C): C = plus_minus(that, _-_)
  def +(that: C): C = plus_minus(that, _+_)
  // ok, this would be applied first
  //def +(that: Double): C = C(-99999, -999999)

  def *(that: C): C = C(this.re * that.re - this.im * that.im, this.im * that.re + this.re * that.im)

  def /(that: C): C = {
    val _re = this.re * that.re + this.im * that.im
    val _im = this.im * that.re - this.re * that.im
    val divisor = math.pow(that.re, 2) + math.pow(that.im, 2)

    require(divisor != 0.0)
    C(_re / divisor, _im / divisor)
  }

  def this(re: Double) = this(re, 0)

  override def equals(that: Any): Boolean =
    that match {
      case that: C => this.re == that.re && this.im == that.im
      case _ => false
   }
}

object C {
  def apply(re: Double, im: Double): C = {
    new C(re, im)
  }

  def apply(re: Double): C = {
    new C(re)
  }
}

object Main extends App {
  implicit def double2Complex(x: Double): C = C(x)

  val c0 = C(0,0)
  val c = new C(1, 2)
  val c1 = new C(3, 0)
  val c2 = C(-1, -5)

  println(c)
  println(c1)
  println(c2)

  println(c1 - c2)
  println(c1 + c2)
  println(c1 * c2)

  println(c1 / c2)

  try {
    println(c / c0)
  }
  catch {
    case ex: IllegalArgumentException => {
      println("Hahah, zero division handled!")
    }
  }

  val c_five = C(5)
  val five = 5.0
  
  println(c1 + c_five == c1 + five)
  println(c_five + c1 == five + c1)
  println(c_five * c1 == five * c1)
}

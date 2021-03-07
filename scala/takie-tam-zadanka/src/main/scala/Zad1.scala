import scala.io.Source

object Zad1 {
  def main(args: Array[String]): Unit = {
    val lines = Source.fromFile("./data/oceny.txt")
      .getLines().toList

	println(lines.map(compute_per_studen_mean).groupMap(_._1)(_._2).map { case (k,v) => (k, (v.foldLeft(0.0)(_ + _)) / v.size)}.maxBy(_._2))
  }

  def compute_per_studen_mean(s: String): (String, Double) = {
    val ls = s.split(";")

    val mean = (ls.slice(3,9).map(x => x.toInt).foldLeft(0)(_ + _)) / 6.0

    return (ls(2), mean)
  }
}

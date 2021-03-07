import scala.io.Source

object Zad2 {
  def main(args: Array[String]): Unit = {
    val lines = Source.fromFile("./data/oceny.txt")
      .getLines().toList

    val students = lines.map(compute_mean).filter(x => x._1.endsWith("a")).groupBy(_._3).map { case (k,v) => (k, v.maxBy(_._4))}
    println(students)
  }

  def compute_mean(s: String): (String, String, String, Double) = {
    val ls = s.split(";")
    (ls(0), ls(1), ls(2), (ls.slice(3,9).map(x => x.toInt).foldLeft(0)(_ + _)) / 6.0)
  }
}

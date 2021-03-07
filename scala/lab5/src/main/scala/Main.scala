import scala.language.postfixOps
import scala.io.Source
import scala.collection.immutable.SortedMap


object Main extends App {
  println(minNotContained(Set(-3, 0, 1, 2, 5, 6)) == 3)
  println(minNotContained(Set(-3, 0, 1, 2, 5, 6)))

  println(swap(Seq(1, 2, 3, 4, 5)) == Seq(2, 1, 4, 3, 5))
  println(swap(Seq(1, 2, 3, 4, 5)))

  val zones: Seq[String] = java.util.TimeZone.getAvailableIDs.toSeq 

  val xd = (zones filter(z => z.startsWith("Europe/")) map(z => z.stripPrefix("Europe/")) map(z => (z.length, z))).sorted map(z => z._2)
  println(xd)

  println(score(Seq(1, 3, 2, 2, 4, 5), Seq(2, 1, 2, 4, 7, 2)) == (1,3))  
  println(score(Seq(1, 3, 2, 2, 4, 5), Seq(2, 1, 2, 4, 7, 2)))  

  histogram(39)

  def minNotContained(set: Set[Int]): Int = {
    (Iterator.from(0) dropWhile(set(_))).next()
  }

  def swap[A](seq: Seq[A]): Seq[A] = {
    (seq grouped(2) map({
      case Seq(x,y) => Seq(y,x)
      case Seq(x) => Seq(x)
    }) flatten) toList
  }

  def count[T](s: Seq[T]) = s.groupBy(x => x).view.mapValues(_.length).toMap

  def score(code: Seq[Int], move: Seq[Int]): (Int, Int) = {
    val black = code zip move map({case (a,b) => if (a == b) {1} else {0}}) sum

    val move_count = count(move)
    val code_count = count(code)
    val _white = ((code_count.keySet & move_count.keySet).toSeq map((k: Int) => code_count(k).min(move_count(k)))).sum
    (black, _white - black)
  }

  def histogram(max: Int): Unit = {
    val lines = Source.fromFile("ogniem_i_mieczem.txt").getLines().toList
    val all_characters = lines map(l => l.toLowerCase() filter(c => c.isLetter)) mkString("")
    val stats = (SortedMap.empty[Char, Int] ++ count(all_characters)).view mapValues('#'.toString * _.min(max))
    for ((k,v) <- stats) printf("%s: %s\n", k, v)
  }
}

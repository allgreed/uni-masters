import Ordering.Implicits._


object Main extends App {
  //println(subSeq(Seq(0,1,2,3,4,5), 2, 4) == Seq(2,3,4))
  //println(subSeq(Seq(0,1,2,3,4,5), 2, 4))

  //println(remElems(Seq(0,9,5), 0) == Seq(9,5))
  //println(remElems(Seq(0,9,5), 0))
  //println(remElems(Seq(0,9,5), 1) == Seq(0,5))
  //println(remElems(Seq(0,9,5), 1))
  //println(remElems(Seq(0,9,5), 2) == Seq(0,9))
  //println(remElems(Seq(0,9,5), 2))

  //println(isOrdered(Seq(1, 2, 2, 4))(_ < _) == false)
  //println(isOrdered(Seq(1, 2, 2, 4))(_ <= _) == true)

  //println(freq(Seq('a','b','a','c','c','a')) == Seq(('a', 3),('b', 1),('c', 2)))
  //println(freq(Seq('a','b','a','c','c','a')))
  
  //println(deStutter(Seq(1, 1, 2, 4, 4, 4, 1, 3)) == Seq(1, 2, 4, 1, 3))
  //println(deStutter(Seq(1, 1, 2, 4, 4, 4, 1, 3)))
  
  println(diff(Seq(1, 2, 3), Seq(2, 2, 1, 3)) == Seq(1, 3))
  println(diff(Seq(1, 2, 3), Seq(2, 2, 1, 3)))

  def subSeq[A](seq: Seq[A], begIdx: Int, endIdx: Int): Seq[A] = {
    seq drop (begIdx) take (endIdx - begIdx + 1)
  }

  def remElems[A](seq: Seq[A], k: Int): Seq[A] = {
    seq.zipWithIndex filter(_._2 != k ) map(x => x._1)
  }

  // TODO: how does it work with skipping parenthesis -> when they're required?
  def isOrdered[A](seq: Seq[A])(leq:(A, A) => Boolean): Boolean = {
    (seq 
      sliding(2)
      map((s: Seq[A]) => leq(s(0), s(1)))
    ).fold (true)(_ && _)
  }

  def freq[A : Ordering](seq: Seq[A]): Seq[(A, Int)] = {
    // TODO: can groupBy preserve ordering?
    seq.groupBy(x => x).map({ case (x, y) => (x, y.length) }).toSeq.sortWith(_._1 < _._1)
  }

  def deStutter[A](seq: Seq[A]): Seq[A] = {
    seq.foldRight(List(): List[A])((cur, acc) => if (acc.isEmpty || acc.head != cur) { cur +: acc } else { acc })
  }

  def diff[A](seq1: Seq[A], seq2: Seq[A]): Seq[A] = {
    seq1 zip seq2 flatMap({ case (x,y) => if (x == y) { Seq() } else { Seq(x) } })
  }
}

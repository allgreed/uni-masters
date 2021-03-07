import scala.annotation.tailrec


object Main extends App {
  //println(sum(List()))
  //println(sum(List(Some(1), Some(2), Some(3), Some(4))))
  //println(sum(List(None, Some(2), None, Some(4))))
  //println(sum(List(None, Some(0))))
  //println(sum(List(None, None, None, None)))
  
  //val ms1 = (x: String) => {
    //x match {
      //case "A" => { 3 }
      //case "B" => { 2 }
      //case _ => { 0 }
    //}
  //}

  //val ms2 = (x: String) => {
    //x match {
      //case "A" => { 1 }
      //case "B" => { 5 }
      //case _ => { 0 }
    //}
  //}

  // TODO: QUESTION: do I need to specialize this?
  //val plus_1 = plus[String](ms1, ms2)
  //println(plus_1("A"))
  //println(plus_1("B"))
  //println(plus_1("C"))

  //println(insertInto(0, List(1,2,3))((a: Int, b: Int) => a <= b))
  //println(insertInto(12, List(1,4,15))((a: Int, b: Int) => a <= b))
  //println(insertInto(12, List(1))((a: Int, b: Int) => a <= b))

  println(divide(List(1, 3, 5, 6, 7)) == (List(1, 5, 7), List(3, 6)))
  
  println(compress(List('a','a','b','c','c','c','d','d','c')) == List( ('a',2), ('b',1), ('c',3), ('d',2), ('c',1) ))
  println(compress(List('a','a','b','c','c','c','d','d','c')))

  def sum(l: List[Option[Int]]): Option[Int] = {
    @tailrec
    def _sum(l: List[Option[Int]], acc: Option[Int] = None): Option[Int] = {
      l.isEmpty match {
        case true => acc
        case false => {
          val new_acc = (l.head, acc) match {
            case (None, _) => { acc }
            case (Some(x), None) => { Some(x) }
            case (Some(x), Some(y)) => { Some(x + y) }
          };

          _sum(l.tail, new_acc)
        }
      }
    }

    _sum(l)
  }

  def compose[A,B,C](f: A => B)(g: B => C): A => C = {
    (x: A) => g(f(x))
  }

  def prod[A,B,C,D](f: A => C, g: B => D): (A, B) => (C, D) = {
    (x: A, y: B) => (f(x), g(y))
  }

  def lift[A,T](op: (T,T) => T)(f: A => T, g: A => T): A => T = {
    (x: A) => op(f(x), g(x))
  }

  type MSet[A] = A => Int 

  // TODO: QUESTION: do I need to specialize all of those?
  def plus[A](s1: MSet[A], s2: MSet[A]): MSet[A] = {
    lift[A, Int](_ + _)(s1, s2)
  }

  def minus[A](s1: MSet[A], s2: MSet[A]): MSet[A] = {
    lift[A, Int](_ + _)(s1, s2)
  }

  def intersection[A](s1: MSet[A], s2: MSet[A]): MSet[A] = {
    val min_op = (x: Int, y: Int) => x.min(y)
    lift[A, Int](min_op)(s1, s2)
  }

  def insertInto[A](a: A, list: List[A])(leq: (A,A) => Boolean): List[A] = {
    @tailrec
    def _insertInto(idx: Int = 0): List[A] = {
      (if (idx < list.length) { leq(a, list(idx)) } else { true }) match {
        case true => {
          val (head, tail) = list.splitAt(idx);
          head ::: List(a) ::: tail
        }
        case false => { _insertInto( idx + 1) }
      }
    }

    _insertInto()
  }

  def divide[A](list: List[A]): (List[A], List[A]) = {
    @tailrec
    def _divide(a: List[A], b: List[A], remaining: List[A], idx: Int): (List[A], List[A]) = {
      // TODO: warning...
      (remaining.isEmpty, idx % 2) match {
        case (true, _) => (a, b)
        case (false, 0) => _divide(a :+ remaining.head, b, remaining.tail, idx + 1)
        case (false, 1) => _divide(a, b :+ remaining.head, remaining.tail, idx + 1)
      }
    }

    _divide(List(), List(), list, 0)
  }

  def compress[A](list: List[A]): List[(A, Int)] = {
    @tailrec
    def _compress(l: List[A], cur: Option[(A, Int)], acc: List[(A, Int)]): List[(A, Int)] = {
      (l, cur) match {
        case (List(), _) => acc ++ cur 
        case (hd :: tail, None) => _compress(tail, Some((hd, 1)), acc)
        case (hd :: tail, Some(cur)) => {
          hd == cur._1 match {
            case true => { _compress(tail, Some((hd, cur._2 + 1)), acc) }
            case false => { _compress(l, None, acc :+ cur)  }
          }
        }
      }
    }

    _compress(list, None, List())
  }
}

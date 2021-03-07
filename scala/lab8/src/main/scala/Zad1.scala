import scala.io._
import akka.actor.{ActorSystem, Actor, Props, ActorRef}
object Player {
  trait A
  case class Ping(counter: Int, maks: Int) extends A
  case class Pong(counter: Int, maks: Int) extends A
  case class PlayWith(a: ActorRef, maks: Int)
}
class Player extends Actor {
  import Player._

  // TODO: extract handle msg method

  def handle_pingpong(msg: A, counter: Int, maks: Int): Unit = {
    println(s"${self.path.name}: Dostałem Pong")

    if (counter >= maks)
    {
      println("Osiągnięto maksymalną liczbę odbić!")
      context.system.terminate() 
    }

    Thread.sleep(500)

    sender() ! Ping(counter + 1, maks)
  }

  def receive: Receive = {
    case PlayWith(a, maks) =>
      println(s"${self.path.name}: Zaczynam grać z $a")
      a ! Ping(0, maks)
    case Ping(counter, maks) =>
      println(s"${self.path.name}: Dostałem Ping")

      if (counter >= maks)
      {
        println("Osiągnięto maksymalną liczbę odbić!")
        context.system.terminate() 
      }

      Thread.sleep(500)

      sender() ! Pong(counter + 1, maks)
    case Pong(counter,maks) => handle_pingpong(Ping(0,0), counter, maks)
  }
}
object PingPong extends App {
  import Player._
  val sys = ActorSystem("sys")
  val addrOfJohn = sys.actorOf(Props[Player](), "John")
  val addrOfKate = sys.actorOf(Props[Player](), "Kate")

  addrOfJohn ! PlayWith(addrOfKate, 5)

  import scala.concurrent.Await
  import scala.concurrent.duration._
  Await.ready(sys.whenTerminated, 365.days)
}

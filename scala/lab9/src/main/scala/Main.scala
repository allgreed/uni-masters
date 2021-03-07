import akka.actor.{ActorSystem, Actor, ActorRef, Props}

object SupervisorMessages {
  case class Init(workers: Int)
  case class Zlecenie(tekst: List[String])
  case class Wynik(value: Int)
}

class Worker extends Actor {
  import SupervisorMessages._

  def receive: Receive = {
    case msg: String => { 
      sender() ! Wynik(msg.split(" ").size)
    }
  }
}

class Supervisor extends Actor {
  import SupervisorMessages._

  var workers: Seq[ActorRef] = null
  var in_process: Int = 0
  var result: Int = 0

  def receive: Receive = {
    case Init(count) => {
      println(s"Initializing ${count} workers!")
      workers = (1 to count).map { i => context.system.actorOf(Props[Worker](), s"Worker${i}") }
      context.become(initialized)
    }
  }

  def initialized: Receive = {
    case Zlecenie(tekst) => {
      in_process = tekst.size
      result = 0
      context.become(processing)
      for ((string, worker) <- tekst zip (LazyList.continually(workers.to(LazyList)).flatten)) worker ! string
    }
  }

  def processing: Receive = {
    case Wynik(value) => {
      //println("nananan", in_process, value, result)
      in_process -= 1
      result += value

      if (in_process <= 0) {
        context.become(initialized)
        println(s"Policzone ${result} słów!")
      }
    }
  }
}

object Main extends App {
  def dane(): List[String] = {
    scala.io.Source.fromResource("ogniem_i_mieczem.txt").getLines().toList
  }

  val system = ActorSystem("WordCounter")
  val supervisor = system.actorOf(Props[Supervisor](), "Nadzorca")

  supervisor ! SupervisorMessages.Init(5)
  supervisor ! SupervisorMessages.Zlecenie(dane())
  Thread.sleep(500)
  supervisor ! SupervisorMessages.Zlecenie(dane())

  system.terminate() 

  import scala.concurrent.Await
  import scala.concurrent.duration._
  Await.ready(system.whenTerminated, 365.days)
}

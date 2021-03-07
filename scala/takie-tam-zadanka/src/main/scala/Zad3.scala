import akka.actor._
import scala.util.Random

object Zad3 {

  case class Przyjmij(klienci: List[ActorRef])
  case object Rozpocznij
  case class Zakupy(sprzedawcy: Seq[ActorRef])
  case class Wybor(produkty: Seq[Integer])
  case class ZaMało(produkty: Seq[Integer], chosenSalesman: ActorRef)
  case object DoWidzenia
  case class Zarobki(n: Int)

  class Szef extends Actor {
    def receive: Receive = {
      case Przyjmij(klienci) => {
        println("Przyjąłem!") 
        context.become(initialized(klienci))
      }
    }

    def initialized(klienci: List[ActorRef]): Receive = {
      case Rozpocznij => {
        val salesman_count: Integer = (klienci.size / 5.0).ceil.toInt 
        println(salesman_count)
        val salesman = (1 to salesman_count).map { i => context.actorOf(Props[Sprzedawca](), s"Sprzedawca${i}") }

        context.become(zarobiony(0, klienci.size, salesman))
        for (klient <- klienci) klient ! Zakupy(salesman)
      }
    }

    def zarobiony(_n: Integer, _client_remaining: Integer, salesman: Seq[ActorRef]): Receive = {
      case Zarobki(incoming) => {
        val n = _n + incoming
        val client_remaining = _client_remaining - 1

        if (client_remaining <= 0) {
          println(s"Łączne zarobki to: ${n}")
          for (s <- salesman) s ! PoisonPill
          context.system.terminate()
        }

        context.become(zarobiony(n, client_remaining, salesman))
      }
    }
  }

  class Klient extends Actor {
    def receive: Receive = {
      case Zakupy(salesman) => {
        println("kupuję!")

        val productCount = Random.between(0, 40)
        val products: Seq[Integer] = (1 to productCount).map(x => Random.between(1, 50))

        val salesmanIndex = Random.between(0, salesman.size - 1)
        println(s"${self.path.name}: wybieram sprzedawcę nr ${salesmanIndex}!")
        val chosenSalesman = salesman(0)

        chosenSalesman ! Wybor(products)
      }

      case ZaMało(_products, chosenSalesman) => {
        val productCount = Random.between(0, 40)
        val products: Seq[Integer] = _products ++ (1 to productCount).map(x => Random.between(1, 50))
        println(products)

        chosenSalesman ! Wybor(products)
      }

      case DoWidzenia => {
        println(s"${self.path.name}: wychodzę!")
        context.stop(self)
      }
    }
  }

  class Sprzedawca extends Actor {
    def receive: Receive = {
      case Wybor(produkty) => {
        val n = produkty.foldLeft(0)(_ + _)
        if (n >= 100) {
          sender() ! DoWidzenia
          context.parent ! Zarobki(n)
        }
        else {
          sender() ! ZaMało(produkty, self)
        }
      }
    }
  }

  def main(args: Array[String]): Unit = {
    val system = ActorSystem("Sklepix")
    val szef = system.actorOf(Props[Szef](), "Szef")
    val klienci: List[ActorRef] = ((1 to 6).map { i => system.actorOf(Props[Klient](), s"Klient${i}") }).toList

    szef ! Przyjmij(klienci)
    szef ! Rozpocznij

    import scala.concurrent.Await
    import scala.concurrent.duration._
    Await.ready(system.whenTerminated, 365.days)
  }
}

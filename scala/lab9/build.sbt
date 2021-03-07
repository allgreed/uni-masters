name := "akka-counter"
version := "1.0.0"

scalaVersion := "2.13.4"

scalacOptions := Seq("-unchecked", "-deprecation", "-encoding", "utf8")

libraryDependencies ++= {
  val akkaV = "2.6.10"
  Seq(
    "com.typesafe.akka" %% "akka-actor" % akkaV
  )
}

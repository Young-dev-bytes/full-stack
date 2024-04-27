FROM maven As backend-build
WORKDIR /fullstack/backend
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src src
RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-alpine
WORKDIR /young
COPY --from=backend-build /fullstack/backend/target/*.jar /young/app.jar
ENTRYPOINT ["sh","-c","java -jar app.jar"]